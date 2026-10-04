#!/usr/bin/env python3
"""Build separate P/T/E semantic networks when each supervisor has one area.

Usage:
    python scripts/area_semantic_exclusive.py PROJECT_ROOT \
        --model BAAI/bge-large-en-v1.5 --max-tokens 512 --device cpu

Place this file beside semantic_similarity.py. It does not import area_semantic.py.
Inputs and outputs are in PROJECT_ROOT/data. candidates.json supplies OpenAlex author IDs;
supervisors.json supplies one area (P, T, or E) for each matching name. Works
come from data/raw/works_<OpenAlex author ID>.json. Articles are assigned to
their authors' areas without using semantic similarity to infer an area. A
paper with authors in different areas appears in both authors' area profiles.
"""

import argparse
import csv
import datetime
import hashlib
import itertools
import json
import pathlib

import numpy as np

import semantic_similarity as sem


AREAS = ("P", "T", "E")
PT_STOP = set("""a ao aos as com como da das de dela dele do dos e em entre era eram essa esse esta estar estas estes este foi for foram ha isso isto ja mas mais menos na nas no nos o os ou para pela pelas pelo pelos por porque que se ser seu seus sua suas sobre sob tambem tem ter um uma uns umas durante atraves partir cada todos todas muito muitos muitas entre nosso nossa seus suas este estudo estudos artigo artigos trabalho trabalhos objetivo objetivos resultado resultados analise analises pesquisa pesquisas dados avaliacao avaliacoes observar observados foram sao""".split())
EN_EXTRA_STOP = set("""study studies result results using based show shows showed observed investigate investigated research analysis analyses method methods data paper findings approach approaches different significantly significant compared comparison new could may also among across however therefore conclusion conclusions objective objectives""".split())


def write_csv(path, columns, rows):
    with path.open("w", newline="", encoding="utf-8") as out:
        writer = csv.DictWriter(out, fieldnames=columns)
        writer.writeheader()
        writer.writerows(rows)


def md_cell(value):
    return str(value).replace("|", r"\|").replace("\n", " ")


def document(paper):
    return " ".join([paper["title"]] * 2 + [paper["abstract"]] +
                    [paper["keywords"]] * 3).strip()


def text_profiles(names, articles_by_name, papers, selected_names):
    """Fit TF-IDF only to papers of eligible members of the current area."""
    from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS, TfidfVectorizer
    from sklearn.preprocessing import normalize
    from scipy.sparse import csr_matrix, vstack

    selected_articles = set().union(*(articles_by_name[name] for name in selected_names))
    usable = sorted(wid for wid in selected_articles if document(papers[wid]))
    if not usable:
        raise ValueError("No title, abstract or keywords for the selected supervisors")
    vectorizer = TfidfVectorizer(strip_accents="unicode", lowercase=True,
                                  stop_words=list(ENGLISH_STOP_WORDS | PT_STOP | EN_EXTRA_STOP),
                                  ngram_range=(1, 2), min_df=1,
                                  max_df=0.85 if len(usable) >= 3 else 1.0,
                                  max_features=25000, sublinear_tf=True,
                                  token_pattern=r"(?u)\b[^\W\d_][\w-]{2,}\b")
    try:
        paper_matrix = vectorizer.fit_transform([document(papers[wid]) for wid in usable])
    except ValueError as exc:
        raise ValueError("No thematic terms remained after text filtering") from exc
    row_by_id = {wid: i for i, wid in enumerate(usable)}
    authors = []
    for name in names:
        indices = [row_by_id[wid] for wid in articles_by_name[name] if wid in row_by_id]
        if indices:
            authors.append(normalize(csr_matrix(paper_matrix[indices].mean(axis=0))))
        else:
            authors.append(csr_matrix((1, paper_matrix.shape[1])))
    return (vstack(authors).tocsr(), np.asarray(vectorizer.get_feature_names_out()),
            paper_matrix, row_by_id)


def top_terms(vector, terms, count=8):
    dense = np.asarray(vector.toarray()).ravel()
    if not np.any(dense > 0):
        return []
    indices = np.argsort(-dense, kind="stable")[:count]
    return [str(terms[i]) for i in indices if dense[i] > 0]


def louvain_labels(graph, resolution, seed):
    import networkx as nx

    if graph.number_of_nodes() == 0:
        return {}
    communities = (nx.community.louvain_communities(
        graph, weight="weight", resolution=resolution, seed=seed)
        if graph.number_of_edges() else [{node} for node in graph.nodes])
    communities = sorted(communities, key=lambda c: (-len(c), sorted(c)[0]))
    return {name: number for number, group in enumerate(communities, start=1)
            for name in group}


def groups_in_area(indices, names, semantic, profiles, k, semantic_share):
    from sklearn.cluster import AgglomerativeClustering
    from sklearn.metrics import silhouette_score

    if len(indices) < k:
        return {}, None
    lexical = (profiles[indices] @ profiles[indices].T).toarray()
    dist = np.zeros((len(indices), len(indices)), dtype=float)
    for x, y in itertools.combinations(range(len(indices)), 2):
        i, j = sorted((indices[x], indices[y]))
        lex = float(np.clip(lexical[x, y], 0, 1))
        score = semantic.get((i, j))
        combined = (semantic_share * max(0, score) + (1 - semantic_share) * lex
                    if score is not None else lex)
        dist[x, y] = dist[y, x] = 1 - float(np.clip(combined, 0, 1))
    labels = AgglomerativeClustering(n_clusters=k, metric="precomputed",
                                    linkage="average").fit_predict(dist)
    clusters = sorted((set(np.array(indices)[labels == cluster]) for cluster in set(labels)),
                      key=lambda group: (-len(group), min(names[i] for i in group)))
    mapping = {names[index]: number for number, cluster in enumerate(clusters, start=1)
               for index in cluster}
    silhouette = (float(silhouette_score(dist, labels, metric="precomputed"))
                  if len(indices) > k else None)
    return mapping, silhouette


def group_terms(member_indices, peer_indices, profiles, terms, count=8):
    from scipy.sparse import csr_matrix

    mean = np.asarray(profiles[member_indices].mean(axis=0)).ravel()
    other = (np.asarray(profiles[peer_indices].mean(axis=0)).ravel()
             if peer_indices else np.zeros_like(mean))
    return top_terms(csr_matrix(np.maximum(0, mean - 0.5 * other)), terms, count)


def representative_titles(members, names, articles, papers, profiles,
                          paper_matrix, row_by_id, count=3):
    indices = [row_by_id[wid] for wid in set().union(*(articles[name] for name in members))
               if wid in row_by_id and papers[wid]["title"]]
    if not indices:
        return []
    index = {name: i for i, name in enumerate(names)}
    centroid = np.asarray(profiles[[index[name] for name in members]].mean(axis=0)).ravel()
    id_by_row = {row: wid for wid, row in row_by_id.items()}
    scored = [(float(paper_matrix[row].dot(centroid)[0]), id_by_row[row]) for row in indices]
    return [papers[wid]["title"] for _, wid in sorted(scored, reverse=True)[:count]]


def options():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project_root", type=pathlib.Path, metavar="PROJECT_ROOT")
    parser.add_argument("--model", default=sem.DEFAULT_MODEL)
    parser.add_argument("--device", default="cpu")
    parser.add_argument("--batch-size", type=int, default=32)
    parser.add_argument("--max-tokens", type=int, default=None,
                        help="Maximum input length including special tokens; "
                             "default: 112 text tokens plus special tokens")
    parser.add_argument("--start-date", default="2021-01-01")
    parser.add_argument("--end-date", default="2026-12-31")
    parser.add_argument("--title-weight", type=float, default=0.25)
    parser.add_argument("--abstract-weight", type=float, default=0.60)
    parser.add_argument("--keyword-weight", type=float, default=0.15)
    parser.add_argument("--min-area-papers", type=int, default=1)
    parser.add_argument("--top-k", type=int, default=3)
    parser.add_argument("--min-similarity", type=float, default=0.0)
    parser.add_argument("--groups", type=int, choices=(2, 3), default=2)
    parser.add_argument("--semantic-share", type=float, default=0.75)
    parser.add_argument("--resolution", type=float, default=1.0)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--include-shared", action="store_true")
    parser.add_argument("--refresh-embeddings", action="store_true")
    args = parser.parse_args()
    try:
        start, end = (datetime.date.fromisoformat(value)
                      for value in (args.start_date, args.end_date))
    except ValueError:
        parser.error("Dates must use YYYY-MM-DD")
    if start > end:
        parser.error("--start-date must not be after --end-date")
    if (args.batch_size < 1 or args.top_k < 1 or args.min_area_papers < 1
            or (args.max_tokens is not None and args.max_tokens < 1)):
        parser.error("Counts and --max-tokens must be positive")
    weights = (args.title_weight, args.abstract_weight, args.keyword_weight)
    if any(weight < 0 for weight in weights) or not any(weights):
        parser.error("Field weights must be nonnegative and at least one positive")
    if not -1 <= args.min_similarity <= 1 or not 0 <= args.semantic_share <= 1:
        parser.error("--min-similarity must be in [-1,1] and --semantic-share in [0,1]")
    if args.resolution <= 0:
        parser.error("--resolution must be positive")
    return args


def load_people(data_dir):
    """Match curated OpenAlex IDs to exactly one area in supervisors.json."""
    candidate_path = data_dir / "candidates.json"
    supervisor_path = data_dir / "supervisors.json"
    candidates = json.loads(candidate_path.read_text(encoding="utf-8"))
    supervisors = json.loads(supervisor_path.read_text(encoding="utf-8"))
    if not isinstance(candidates, list) or not isinstance(supervisors, list):
        raise ValueError("candidates.json and supervisors.json must contain lists")

    area_by_name = {}
    for person in supervisors:
        name = person["name"]
        if name in area_by_name:
            raise ValueError(f"Duplicate supervisor in supervisors.json: {name}")
        codes = person["areas"]
        if not isinstance(codes, list) or len(codes) != 1 or codes[0] not in AREAS:
            raise ValueError(f"{name} must have exactly one area among {AREAS}; got {codes!r}")
        area_by_name[name] = codes

    names = [person["name"] for person in candidates]
    if len(names) != len(set(names)):
        raise ValueError("Duplicate supervisor names in candidates.json")
    if set(names) != set(area_by_name):
        raise ValueError("Names differ between candidates.json and supervisors.json: "
                         f"missing={sorted(set(names) - set(area_by_name))}, "
                         f"extra={sorted(set(area_by_name) - set(names))}")

    owner_by_id = {}
    ids_by_person = []
    for name, person in zip(names, candidates):
        records = person["candidates"]
        if not isinstance(records, list) or not records:
            raise ValueError(f"No curated OpenAlex author candidates for {name}")
        ids = list(dict.fromkeys(sem.short_id(record["id"])
                                 for record in records))
        if not all(ids):
            raise ValueError(f"Blank OpenAlex author ID for {name}")
        for author_id in ids:
            if author_id in owner_by_id:
                raise ValueError(f"OpenAlex author {author_id} assigned to both "
                                 f"{owner_by_id[author_id]} and {name}")
            owner_by_id[author_id] = name
        ids_by_person.append(ids)
    return names, area_by_name, ids_by_person


def metadata_for_works(ids_by_person, raw_dir, work_ids, start, end):
    metadata = {}
    for aid in dict.fromkeys(aid for author_ids in ids_by_person for aid in author_ids):
        path = raw_dir / f"works_{aid}.json"
        for work in json.loads(path.read_text(encoding="utf-8")):
            if work.get("type") != "article" or not sem.in_period(work, start, end):
                continue
            wid = sem.short_id(work["id"])
            if wid not in work_ids:
                continue
            item = metadata.setdefault(wid, {"doi": "", "publication_date": ""})
            item["doi"] = item["doi"] or work.get("doi") or ""
            item["publication_date"] = item["publication_date"] or work.get("publication_date") or ""
    return metadata


def embedding_cache(data_dir, fields, args, weights):
    # Same fingerprint as the earlier two-file version, so existing vectors can
    # be reused when switching to this single area script.
    settings = {"version": "area-semantic-v1", "fields": fields, "model": args.model,
                "weights": weights}
    if args.max_tokens is not None:
        settings["max_tokens"] = args.max_tokens
    key = hashlib.sha256(json.dumps(settings, ensure_ascii=False, sort_keys=True,
                                    separators=(",", ":")).encode("utf-8")).hexdigest()
    path = data_dir / "area_semantic_embeddings.npz"
    if path.is_file() and not args.refresh_embeddings:
        with np.load(path, allow_pickle=False) as cached:
            if str(cached["fingerprint"].item()) == key:
                ids = cached["ids"].tolist()
                vectors = np.asarray(cached["vectors"], dtype=np.float64)
                if vectors.ndim == 2 and len(ids) == len(vectors):
                    print(f"Using {len(ids)} cached article vectors", flush=True)
                    return dict(zip(ids, vectors))
    vectors = sem.embed_works(fields, args.model, args.batch_size, weights,
                              args.device, args.max_tokens)
    ids = sorted(vectors)
    temp = path.with_name(path.name + ".tmp")
    with temp.open("wb") as out:
        np.savez_compressed(out, fingerprint=np.array(key), ids=np.array(ids),
                            vectors=np.stack([vectors[wid] for wid in ids]).astype("float32"))
    temp.replace(path)
    return vectors


def assign_by_author(names, areas, articles_by_person):
    """Union authors' areas for shared papers; profiles stay area-specific."""
    assignments = {}
    owners = {}
    for name, works in zip(names, articles_by_person):
        area = areas[name][0]
        for wid in works:
            assignments.setdefault(wid, set()).add(area)
            owners.setdefault(wid, set()).add((name, area))
    return ({wid: tuple(area for area in AREAS if area in codes)
             for wid, codes in assignments.items()}, owners)


def write_memberships(data_dir, fields, metadata, assignments, owners):
    rows = []
    for wid in sorted(fields):
        people = sorted(owners[wid])
        rows.append({"work_id": wid, "title": fields[wid]["title"],
                     "doi": metadata.get(wid, {}).get("doi", ""),
                     "publication_date": metadata.get(wid, {}).get("publication_date", ""),
                     "supervisors": "; ".join(name for name, _area in people),
                     "supervisor_areas": "; ".join(f"{name} ({area})" for name, area in people),
                     "areas": "+".join(assignments[wid])})
    write_csv(data_dir / "area_semantic_work_membership.csv",
              ("work_id", "title", "doi", "publication_date", "supervisors",
               "supervisor_areas", "areas"), rows)


def area_outputs(data_dir, names, areas, author_ids, fields, vectors, args):
    import networkx as nx

    all_nodes, all_edges, coverage, descriptions = [], [], [], []
    combined = nx.Graph()
    index_by_name = {name: i for i, name in enumerate(names)}
    for area in AREAS:
        members = [name for name in names if areas[name] == [area]]
        relevant = [works if areas[name] == [area] else set()
                    for name, works in zip(names, author_ids)]
        articles_by_name = dict(zip(names, relevant))
        used, pairs = sem.compare_people(names, relevant, vectors, args.include_shared)
        eligible = {i for i, name in enumerate(names) if name in members
                    and len(used[i]) >= args.min_area_papers}
        for i, name in enumerate(names):
            if name in members:
                coverage.append({"area": area, "supervisor": name,
                                 "articles_in_period": len(author_ids[i]),
                                 "articles_assigned_to_area": len(relevant[i]),
                                 "articles_with_embedding": len(used[i]),
                                 "eligible": int(i in eligible)})

        valid = {pair: value for pair, value in pairs.items()
                 if pair[0] in eligible and pair[1] in eligible}
        selected = sem.select_edges(names, valid, args.top_k, max(0, args.min_similarity))
        graph = nx.Graph()
        graph.add_nodes_from(names[i] for i in sorted(eligible))
        for i, j in selected:
            score = valid[(i, j)][0]
            if score is not None and score > 0:
                graph.add_edge(names[i], names[j], weight=float(score))
        communities = louvain_labels(graph, args.resolution, args.seed)

        profile = terms = paper_matrix = row_by_id = None
        if eligible:
            try:
                profile, terms, paper_matrix, row_by_id = text_profiles(
                    names, articles_by_name, fields, {names[i] for i in eligible})
            except ValueError as exc:
                print(f"No usable TF-IDF terms for {area}: {exc}", flush=True)
        groups, silhouette = ({}, None)
        if profile is not None:
            pair_scores = {pair: value[0] for pair, value in valid.items()
                           if value[0] is not None}
            groups, silhouette = groups_in_area(
                sorted(eligible), names, pair_scores, profile, args.groups,
                args.semantic_share)

        for i in sorted(eligible):
            name = names[i]
            group_number = groups.get(name)
            row = {"id": f"{area}::{name}", "label": name, "supervisor": name,
                   "area": area, "area_name": area, "original_areas": area,
                   "article_count": len(used[i]),
                   "abstract_count": sum(bool(fields[wid]["abstract"]) for wid in used[i]),
                   "louvain": f"{area}{communities[name]}",
                   "proposed_group": f"{area}{group_number}" if group_number else "",
                   "top_terms": "; ".join(top_terms(profile[i], terms))
                   if profile is not None else ""}
            all_nodes.append(row)
            combined.add_node(row["id"], **{key: val for key, val in row.items()
                                            if key != "id"})
        for i, j in selected:
            score, shared, ni, nj = valid[(i, j)]
            if score is None or score <= 0:
                continue
            source, target = names[i], names[j]
            ga, gb = groups.get(source), groups.get(target)
            row = {"source": f"{area}::{source}", "target": f"{area}::{target}",
                   "area": area, "weight": round(score, 6),
                   "shared_article_count": shared,
                   "source_articles_compared": ni, "target_articles_compared": nj,
                   "same_louvain": int(communities[source] == communities[target]),
                   "same_proposed_group": int(ga == gb) if ga and gb else -1}
            all_edges.append(row)
            combined.add_edge(row["source"], row["target"], **{
                key: val for key, val in row.items() if key not in ("source", "target")})

        with (data_dir / f"area_semantic_matrix_{area}.csv").open(
                "w", encoding="utf-8", newline="") as out:
            writer = csv.writer(out)
            kept = sorted(eligible)
            writer.writerow(["supervisor", *(names[i] for i in kept)])
            for i in kept:
                writer.writerow([names[i], *[
                    "1.000000" if i == j else
                    f"{pairs[(min(i,j), max(i,j))][0]:.6f}"
                    if pairs[(min(i,j), max(i,j))][0] is not None else ""
                    for j in kept]])

        for mapping, kind in ((communities, "louvain"), (groups, "proposed")):
            for number in sorted(set(mapping.values())):
                people = [name for name in members if mapping.get(name) == number]
                indices = [index_by_name[name] for name in people]
                other = [i for i in sorted(eligible) if i not in indices]
                descriptor = (group_terms(indices, other, profile, terms)
                              if profile is not None else [])
                examples = (representative_titles(people, names, articles_by_name,
                            fields, profile, paper_matrix, row_by_id)
                            if profile is not None else [])
                descriptions.append({"area": area, "kind": kind,
                                     "id": f"{area}{number}", "member_count": len(people),
                                     "members": "; ".join(people),
                                     "top_terms": "; ".join(descriptor),
                                     "example_titles": "; ".join(examples),
                                     "silhouette_area": f"{silhouette:.3f}"
                                     if kind == "proposed" and silhouette is not None else ""})
        print(f"{area}: {len(members)} supervisors; {len(eligible)} with articles; "
              f"{graph.number_of_edges()} edges; "
              f"{len(set(communities.values()))} Louvain communities", flush=True)

    write_csv(data_dir / "area_semantic_coverage.csv",
              ("area", "supervisor", "articles_in_period", "articles_assigned_to_area",
               "articles_with_embedding", "eligible"), coverage)
    write_csv(data_dir / "area_semantic_nodes.csv",
              ("id", "label", "supervisor", "area", "area_name", "original_areas",
               "article_count", "abstract_count", "louvain", "proposed_group", "top_terms"),
              all_nodes)
    write_csv(data_dir / "area_semantic_edges.csv",
              ("source", "target", "area", "weight", "shared_article_count",
               "source_articles_compared", "target_articles_compared", "same_louvain",
               "same_proposed_group"), all_edges)
    write_csv(data_dir / "area_semantic_themes.csv",
              ("area", "kind", "id", "member_count", "members", "top_terms",
               "example_titles", "silhouette_area"), descriptions)
    nx.write_graphml(combined, data_dir / "area_semantic.graphml")
    for area in AREAS:
        ids = [row["id"] for row in all_nodes if row["area"] == area]
        nx.write_graphml(combined.subgraph(ids).copy(),
                         data_dir / f"area_semantic_{area}.graphml")
    return coverage, descriptions


def write_report(data_dir, args, fields, assignments, coverage, descriptions):
    cross_area = sum(len(codes) > 1 for codes in assignments.values())
    lines = ["# Redes semânticas por área exclusiva (P/T/E)", "",
             f"Período: {args.start_date} a {args.end_date}. Modelo: `{args.model}`; "
             f"dispositivo: `{args.device}`.",
             (f"Limite de {args.max_tokens} tokens por segmento, incluindo tokens especiais."
              if args.max_tokens is not None else
              "Limite padrão de 112 tokens de texto por segmento, mais tokens especiais."),
             "Cada orientador tem exatamente uma área em `supervisors.json`. Seus artigos "
             "OpenAlex (`type = article`) são usados somente em sua rede de área; não há "
             "classificação semântica de artigos entre P, T e E.",
             f"{len(fields)} artigos distintos; {cross_area} aparecem em mais de uma área "
             "por terem coautores orientadores vinculados a áreas diferentes.",
             ("Por padrão, artigos em coautoria entre dois orientadores são excluídos "
              "apenas da comparação daquele par."
              if not args.include_shared else
              "Artigos em coautoria são mantidos na comparação dos respectivos orientadores."),
             f"Cada rede usa a união dos {args.top_k} vizinhos mais próximos de cada "
             "orientador (similaridade mínima {args.min_similarity:g}); o peso das arestas "
             "e o Louvain usam a similaridade de cosseno. O agrupamento separado de "
             f"até {args.groups} temas combina similaridade semântica "
             f"({args.semantic_share:g}) e TF-IDF ({1-args.semantic_share:g}).", ""]
    for area in AREAS:
        members = [row for row in coverage if row["area"] == area]
        lines += [f"## {area}", "",
                  f"{len(members)} orientadores; {sum(row['eligible'] for row in members)} "
                  "com artigos suficientes para entrar na rede.", "",
                  "| Orientador | Artigos com embedding | Na rede |",
                  "| --- | ---: | --- |"]
        for row in members:
            lines.append(f"| {md_cell(row['supervisor'])} | "
                         f"{row['articles_with_embedding']} | "
                         f"{'sim' if row['eligible'] else 'não'} |")
        for kind, title in (("louvain", "Comunidades Louvain"),
                            ("proposed", f"Proposta de até {args.groups} temas")):
            lines += ["", f"### {title}", "",
                      "| ID | Orientadores | Termos distintivos | Artigos representativos |",
                      "| --- | --- | --- | --- |"]
            for item in descriptions:
                if item["area"] == area and item["kind"] == kind:
                    lines.append(f"| {item['id']} | {md_cell(item['members'])} | "
                                 f"{md_cell(item['top_terms'])} | "
                                 f"{md_cell(item['example_titles'])} |")
        lines.append("")
    (data_dir / "area_semantic.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main():
    args = options()
    root = args.project_root
    data_dir = root / "data"
    if not data_dir.is_dir():
        raise FileNotFoundError(f"Missing data directory: {data_dir}")
    names, areas, ids_by_person = load_people(data_dir)
    raw = data_dir / "raw"
    if not raw.is_dir():
        raise FileNotFoundError(f"Missing raw works directory: {raw}")
    articles, fields = sem.load_works(names, ids_by_person, raw,
                                     args.start_date, args.end_date)
    if not fields:
        raise ValueError("No articles found in the selected period")
    assignments, owners = assign_by_author(names, areas, articles)
    metadata = metadata_for_works(ids_by_person, raw, set(fields),
                                  args.start_date, args.end_date)
    weights = {"title": args.title_weight, "abstract": args.abstract_weight,
               "keywords": args.keyword_weight}
    vectors = embedding_cache(data_dir, fields, args, weights)
    write_memberships(data_dir, fields, metadata, assignments, owners)
    coverage, descriptions = area_outputs(data_dir, names, areas, articles,
                                          fields, vectors, args)
    write_report(data_dir, args, fields, assignments, coverage, descriptions)
    for filename in ("area_semantic_work_membership.csv", "area_semantic.graphml",
                     "area_semantic.md"):
        print(data_dir / filename)


if __name__ == "__main__":
    main()
