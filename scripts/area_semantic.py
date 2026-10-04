#!/usr/bin/env python3
"""Classify papers into B/N/Q, then build area-specific author networks.

Usage:
    python scripts/area_semantic.py PROJECT_ROOT [--groups 2]

Keep semantic_similarity.py in the same scripts folder.
Requires numpy, scipy, scikit-learn, networkx, sentence-transformers.

The classifier uses papers by supervisors listed in exactly one concentration
area as provisional reference examples. An article may receive several areas
or no area. work_area_curated.csv lists current papers and their supervisors.
Edit its areas column (e.g. B+N, or empty to exclude a work); edited rows
are preserved, even when a paper falls outside the current date/author filter;
outdated automatic suggestions are removed on the next run.
Legacy work_area_curated.csv rows with work_id,areas are kept as manual edits.

Paper vectors are cached with a content/model fingerprint so rerunning after
manual curation does not normally require repeating inference on the CPU.
All inputs and generated files live in PROJECT_ROOT/data.
--max-tokens counts the complete model input, including special tokens.
"""

import argparse
import csv
import datetime
import hashlib
import itertools
import json
import pathlib
import re

import numpy as np

import semantic_similarity as sem


ROOT = None  # Set from argparse in main().
DATA = None  # Set to ROOT/data in main().
AREAS = sem.AREA_ORDER
AREA_NAMES = sem.AREA_LABELS
PT_STOP = set("""a ao aos as com como da das de dela dele do dos e em entre era eram essa esse esta estar estas estes este foi for foram ha isso isto ja mas mais menos na nas no nos o os ou para pela pelas pelo pelos por porque que se ser seu seus sua suas sobre sob tambem tem ter um uma uns umas durante atraves partir cada todos todas muito muitos muitas entre nosso nossa seus suas este estudo estudos artigo artigos trabalho trabalhos objetivo objetivos resultado resultados analise analises pesquisa pesquisas dados avaliacao avaliacoes observar observados foram sao""".split())
EN_EXTRA_STOP = set("""study studies result results using based show shows showed observed investigate investigated research analysis analyses method methods data paper findings approach approaches different significantly significant compared comparison new could may also among across however therefore conclusion conclusions objective objectives""".split())


def document(paper):
    return " ".join([paper["title"]] * 2 + [paper["abstract"]] +
                    [paper["keywords"]] * 3).strip()


def text_profiles(names, articles_by_name, papers, selected_names):
    """Fit TF-IDF to papers assigned to this area's eligible supervisors only."""
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
            average = csr_matrix(paper_matrix[indices].mean(axis=0))
            authors.append(normalize(average))
        else:
            authors.append(csr_matrix((1, paper_matrix.shape[1])))
    return (vstack(authors).tocsr(), np.asarray(vectorizer.get_feature_names_out()),
            set(usable), paper_matrix, row_by_id)


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
    mapping = {names[index]: group_number for group_number, cluster in enumerate(clusters, start=1)
               for index in cluster}
    silhouette = (float(silhouette_score(dist, labels, metric="precomputed"))
                  if len(indices) > k else None)
    return mapping, silhouette


def group_terms(member_indices, peer_indices, profiles, terms, count=8):
    from scipy.sparse import csr_matrix

    mean = np.asarray(profiles[member_indices].mean(axis=0)).ravel()
    other = (np.asarray(profiles[peer_indices].mean(axis=0)).ravel()
             if peer_indices else np.zeros_like(mean))
    distinct = np.maximum(0, mean - 0.5 * other)
    return top_terms(csr_matrix(distinct), terms, count)


def representative_titles(members, index, articles, papers, profiles, paper_matrix,
                          row_by_id, count=3):
    indices = [row_by_id[wid] for wid in set().union(*(articles[name] for name in members))
               if wid in row_by_id and papers[wid]["title"]]
    if not indices:
        return []
    member_indices = [index[name] for name in members]
    centroid = np.asarray(profiles[member_indices].mean(axis=0)).ravel()
    id_by_row = {row: wid for wid, row in row_by_id.items()}
    scored = [(float(paper_matrix[row].dot(centroid)[0]), id_by_row[row]) for row in indices]
    return [papers[wid]["title"] for _, wid in sorted(scored, reverse=True)[:count]]


def md_cell(value):
    return str(value).replace("|", r"\|").replace("\n", " ")


def options():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("project_root", type=pathlib.Path, metavar="PROJECT_ROOT",
                   help="Project directory containing the data folder")
    p.add_argument("--model", default=sem.DEFAULT_MODEL)
    p.add_argument("--device", default="cpu")
    p.add_argument("--batch-size", type=int, default=32)
    p.add_argument("--max-tokens", type=int, default=None,
                   help="Maximum model input length per segment, including special tokens "
                        "(default: 112 text tokens plus special tokens)")
    p.add_argument("--start-date", default="2021-01-01")
    p.add_argument("--end-date", default="2026-12-31")
    p.add_argument("--title-weight", type=float, default=0.25)
    p.add_argument("--abstract-weight", type=float, default=0.60)
    p.add_argument("--keyword-weight", type=float, default=0.15)
    p.add_argument("--min-area-score", type=float, default=0.20,
                   help="Provisional cosine cutoff for assigning an area (default: 0.20)")
    p.add_argument("--area-margin", type=float, default=0.05,
                   help="Also assign areas within this distance of the best score (default: 0.05)")
    p.add_argument("--min-area-papers", type=int, default=1,
                   help="Minimum assigned papers to include a supervisor in an area network")
    p.add_argument("--top-k", type=int, default=3)
    p.add_argument("--min-similarity", type=float, default=0.0)
    p.add_argument("--groups", type=int, choices=(2, 3), default=2)
    p.add_argument("--semantic-share", type=float, default=0.75,
                   help="Fraction of semantic similarity in the fixed-group clustering")
    p.add_argument("--resolution", type=float, default=1.0)
    p.add_argument("--seed", type=int, default=42)
    p.add_argument("--include-shared", action="store_true",
                   help="Keep shared coauthored papers in pairwise profile comparisons")
    p.add_argument("--refresh-embeddings", action="store_true")
    args = p.parse_args()
    try:
        start, end = (datetime.date.fromisoformat(value)
                      for value in (args.start_date, args.end_date))
    except ValueError:
        p.error("Dates must use YYYY-MM-DD")
    if (start > end or args.batch_size < 1 or args.top_k < 1 or args.min_area_papers < 1
            or (args.max_tokens is not None and args.max_tokens < 1)):
        p.error("Invalid date range or a nonpositive count")
    if not -1 <= args.min_area_score <= 1 or not 0 <= args.area_margin <= 2:
        p.error("--min-area-score must be in [-1,1] and --area-margin in [0,2]")
    if not -1 <= args.min_similarity <= 1 or not 0 <= args.semantic_share <= 1:
        p.error("Invalid graph threshold or semantic share")
    if args.resolution <= 0:
        p.error("--resolution must be positive")
    weights = (args.title_weight, args.abstract_weight, args.keyword_weight)
    if any(weight < 0 for weight in weights) or not any(weights):
        p.error("Field weights must be nonnegative and at least one positive")
    return args


def write_csv(path, columns, rows):
    with path.open("w", newline="", encoding="utf-8") as out:
        writer = csv.DictWriter(out, fieldnames=columns)
        writer.writeheader()
        writer.writerows(rows)


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


def embedding_cache(fields, args, weights):
    settings = {
        "version": "area-semantic-v1", "fields": fields, "model": args.model,
        "weights": weights,
    }
    if args.max_tokens is not None:
        settings["max_tokens"] = args.max_tokens
    key = hashlib.sha256(json.dumps(settings, ensure_ascii=False, sort_keys=True,
                                    separators=(",", ":")).encode("utf-8")).hexdigest()
    path = DATA / "area_semantic_embeddings.npz"
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


def reference_profiles(names, areas, author_ids, vectors):
    """Equal-weight author centroids from unambiguous exclusive-area papers."""
    from collections import defaultdict

    owners = defaultdict(set)
    for name, works in zip(names, author_ids):
        if len(areas[name]) == 1:
            area = areas[name][0]
            for wid in works & vectors.keys():
                owners[wid].add(area)
    unique_seed = {wid: next(iter(codes)) for wid, codes in owners.items()
                   if len(codes) == 1}
    prototypes = {}
    support = {}
    for area in AREAS:
        authors = []
        work_count = set()
        for name, works in zip(names, author_ids):
            if areas[name] != [area]:
                continue
            own = [vectors[wid] for wid in works if unique_seed.get(wid) == area]
            if own:
                authors.append(sem.unit(np.mean(own, axis=0)))
                work_count.update(wid for wid in works if unique_seed.get(wid) == area)
        if not authors:
            raise ValueError(f"No exclusive-area seed authors with usable papers for {area}. "
                             "The automatic classifier needs example papers in each area.")
        prototypes[area] = sem.unit(np.mean(authors, axis=0))
        support[area] = {"exclusive_authors": len(authors), "unique_seed_works": len(work_count)}
    return prototypes, support, unique_seed


def parse_areas(value):
    tokens = set(re.split(r"[+,;/\s]+", value.strip())) - {""}
    unknown = tokens - set(AREAS)
    if unknown:
        raise ValueError(f"Unknown concentration area(s): {sorted(unknown)}")
    return tuple(area for area in AREAS if area in tokens)


def read_overrides(work_ids):
    path = DATA / "work_area_curated.csv"
    if not path.exists():
        return {}, {}, [], set(), 0
    with path.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        if not reader.fieldnames or not {"work_id", "areas"} <= set(reader.fieldnames):
            raise ValueError(f"{path} must have columns work_id,areas")
        columns = list(reader.fieldnames)
        legacy = not {"source", "suggested_areas"} <= set(columns)
        overrides, existing, stale_manual = {}, {}, set()
        stale_automatic = 0
        for line, row in enumerate(reader, start=2):
            wid = sem.short_id(row["work_id"] or "")
            if not wid:
                raise ValueError(f"Empty work ID in {path}, line {line}")
            if wid in existing:
                raise ValueError(f"Repeated work ID in {path}, line {line}: {wid}")
            areas = parse_areas(row["areas"] or "")
            source = (row.get("source") or "").strip().lower()
            if not legacy and source not in ("automatic", "manual", ""):
                raise ValueError(f"Unknown source in {path}, line {line}: {source}")
            suggested = parse_areas(row.get("suggested_areas") or "")
            manual = legacy or source != "automatic" or areas != suggested
            if wid in work_ids:
                if manual:
                    overrides[wid] = areas
            elif manual:
                stale_manual.add(wid)
            else:
                stale_automatic += 1
            existing[wid] = row
    return overrides, existing, columns, stale_manual, stale_automatic


def update_curated(names, author_ids, classification, overrides, existing, columns,
                   stale_manual):
    """Refresh suggestions and author names without losing manual area edits."""
    path = DATA / "work_area_curated.csv"
    supervisors = {}
    for name, works in zip(names, author_ids):
        for wid in works:
            supervisors.setdefault(wid, []).append(name)
    standard = ("work_id", "title", "supervisors", "areas", "suggested_areas", "source")
    fieldnames = list(dict.fromkeys((*standard, *columns)))
    rows = []
    for suggestion in classification:
        wid = suggestion["work_id"]
        current = existing.get(wid, {})
        manual = wid in overrides
        rows.append({**current, "work_id": wid, "title": suggestion["title"],
                     "supervisors": "; ".join(supervisors[wid]),
                     "areas": "+".join(overrides[wid]) if manual else suggestion["suggested_areas"],
                     "suggested_areas": suggestion["suggested_areas"],
                     "source": "manual" if manual else "automatic"})
    # Preserve manual edits outside the current filter so they are available
    # again if the date range or curated candidate list changes.
    by_id = {row["work_id"]: row for row in rows}
    ordered = [by_id[wid] if wid in by_id else existing[wid]
               for wid in existing if wid in by_id or wid in stale_manual]
    ordered += [row for row in rows if row["work_id"] not in existing]
    temp = path.with_name(path.name + ".tmp")
    write_csv(temp, fieldnames, ordered)
    temp.replace(path)


def classify(fields, metadata, vectors, prototypes, seeds, args, overrides):
    rows = []
    assigned = {}
    for wid in sorted(fields):
        scores = {area: float(np.dot(vectors[wid], prototypes[area]))
                  for area in AREAS} if wid in vectors else {}
        ordered_scores = sorted(scores.values(), reverse=True)
        gap = ordered_scores[0] - ordered_scores[1] if len(ordered_scores) >= 2 else None
        best = max(scores.values(), default=float("-inf"))
        suggestion = tuple(area for area in AREAS if scores.get(area, -2) >= args.min_area_score
                           and scores.get(area, -2) >= best - args.area_margin)
        chosen = overrides.get(wid, suggestion)
        assigned[wid] = chosen
        review_flags = []
        if not suggestion:
            review_flags.append("unclassified")
        elif len(suggestion) > 1:
            review_flags.append("multiple_areas")
        if not fields[wid]["abstract"]:
            review_flags.append("no_abstract")
        rows.append({
            "work_id": wid, "title": fields[wid]["title"],
            "doi": metadata.get(wid, {}).get("doi", ""),
            "publication_date": metadata.get(wid, {}).get("publication_date", ""),
            **{f"score_{area}": f"{scores[area]:.6f}" if scores else "" for area in AREAS},
            "score_gap": f"{gap:.6f}" if gap is not None else "",
            "suggested_areas": "+".join(suggestion),
            "assigned_areas": "+".join(chosen),
            "source": "manual_override" if wid in overrides else "automatic",
            "review_flags": ";".join(review_flags),
            "exclusive_author_seed": seeds.get(wid, ""),
            "has_abstract": int(bool(fields[wid]["abstract"])),
            "has_keywords": int(bool(fields[wid]["keywords"])),
        })
    write_csv(DATA / "work_area_suggestions.csv",
              ("work_id", "title", "doi", "publication_date", "score_P", "score_E",
               "score_T", "score_gap", "suggested_areas", "assigned_areas", "source",
               "review_flags",
               "exclusive_author_seed", "has_abstract", "has_keywords"), rows)
    return assigned, rows


def area_outputs(names, areas, author_ids, fields, vectors, assignments, args):
    import networkx as nx

    all_nodes, all_edges, coverage, descriptions = [], [], [], []
    layered = nx.Graph()
    for area in AREAS:
        members = [name for name in names if area in areas[name]]
        relevant = [({wid for wid in works if area in assignments[wid]} if name in members else set())
                    for name, works in zip(names, author_ids)]
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

        profile = None
        terms = None
        paper_matrix = row_by_id = None
        if eligible:
            try:
                profile, terms, _usable, paper_matrix, row_by_id = text_profiles(
                    names, dict(zip(names, relevant)), fields,
                    {names[i] for i in eligible})
            except ValueError as exc:
                print(f"No usable TF-IDF terms for {area}: {exc}", flush=True)
        groups, silhouette = ({}, None)
        if profile is not None:
            pair_scores = {pair: value[0] for pair, value in valid.items()
                           if value[0] is not None}
            groups, silhouette = groups_in_area(
                sorted(eligible), names, pair_scores, profile, args.groups, args.semantic_share)

        for i in sorted(eligible):
            name = names[i]
            group_number = groups.get(name)
            row = {"id": f"{area}::{name}", "label": name, "supervisor": name,
                   "area": area, "area_name": AREA_NAMES[area],
                   "original_areas": "+".join(areas[name]),
                   "article_count": len(used[i]),
                   "abstract_count": sum(bool(fields[wid]["abstract"]) for wid in used[i]),
                   "louvain": f"{area}{communities[name]}",
                   "proposed_group": f"{area}{group_number}" if group_number else "",
                   "top_terms": "; ".join(top_terms(profile[i], terms))
                   if profile is not None else ""}
            all_nodes.append(row)
            layered.add_node(row["id"], **{k: v for k, v in row.items() if k != "id"})
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
                   "same_proposed_group": int(ga == gb) if ga and gb else ""}
            all_edges.append(row)
            layered.add_edge(row["source"], row["target"], **{
                k: v for k, v in row.items() if k not in ("source", "target")})

        with (DATA / f"area_semantic_matrix_{area}.csv").open(
                "w", encoding="utf-8", newline="") as out:
            writer = csv.writer(out)
            kept = [names[i] for i in sorted(eligible)]
            writer.writerow(["supervisor", *kept])
            for i in sorted(eligible):
                writer.writerow([names[i], *[
                    "1.000000" if i == j else
                    f"{pairs[(min(i,j), max(i,j))][0]:.6f}"
                    if pairs[(min(i,j), max(i,j))][0] is not None else ""
                    for j in sorted(eligible)]])

        def describe_partition(mapping, kind):
            for number in sorted(set(mapping.values())):
                people = [name for name in members if mapping.get(name) == number]
                indices = [names.index(name) for name in people]
                other = [i for i in sorted(eligible) if i not in indices]
                descriptor = (group_terms(indices, other, profile, terms)
                              if profile is not None else [])
                examples = (representative_titles(people, {n: i for i, n in enumerate(names)},
                            dict(zip(names, relevant)), fields, profile, paper_matrix, row_by_id)
                            if profile is not None else [])
                descriptions.append({"area": area, "kind": kind,
                                     "id": f"{area}{number}", "member_count": len(people),
                                     "members": "; ".join(people),
                                     "top_terms": "; ".join(descriptor),
                                     "example_titles": "; ".join(examples),
                                     "silhouette_area": f"{silhouette:.3f}" if kind == "proposed" and
                                     silhouette is not None else ""})

        describe_partition(communities, "louvain")
        describe_partition(groups, "proposed")
        print(f"{area}: {len(members)} members; {len(eligible)} with area-specific papers; "
              f"{len(selected)} candidate edges; {len(set(communities.values()))} Louvain communities",
              flush=True)

    write_csv(DATA / "area_semantic_coverage.csv",
              ("area", "supervisor", "articles_in_period", "articles_assigned_to_area",
               "articles_with_embedding", "eligible"), coverage)
    write_csv(DATA / "area_semantic_nodes.csv",
              ("id", "label", "supervisor", "area", "area_name", "original_areas",
               "article_count", "abstract_count", "louvain", "proposed_group", "top_terms"), all_nodes)
    write_csv(DATA / "area_semantic_edges.csv",
              ("source", "target", "area", "weight", "shared_article_count",
               "source_articles_compared", "target_articles_compared", "same_louvain",
               "same_proposed_group"), all_edges)
    write_csv(DATA / "area_semantic_themes.csv",
              ("area", "kind", "id", "member_count", "members", "top_terms",
               "example_titles", "silhouette_area"), descriptions)
    nx.write_graphml(layered, DATA / "area_semantic.graphml")
    for area in AREAS:
        ids = [row["id"] for row in all_nodes if row["area"] == area]
        nx.write_graphml(layered.subgraph(ids).copy(), DATA / f"area_semantic_{area}.graphml")
    return coverage, descriptions


def write_report(args, support, classification, coverage, descriptions, override_count):
    lines = ["# Redes semânticas por divisão científica", "",
             f"Período: {args.start_date} a {args.end_date}. Modelo: `{args.model}`; dispositivo: `{args.device}`.",
             (f"Limite de {args.max_tokens} tokens por segmento, incluindo tokens especiais."
              if args.max_tokens is not None else
              "Limite padrão de 112 tokens de texto por segmento, mais tokens especiais."),
             "Classificação provisória: comparação dos vetores de título, abstract e keywords "
             "com protótipos de artigos de orientadores vinculados a uma única área. "
             "Os protótipos dão o mesmo peso a cada orientador de referência.",
             "O vínculo exclusivo de um orientador foi usado como referência inicial, "
             "não como validação de que todos os seus artigos pertencem àquela área.",
             f"Área atribuída se cosseno ≥ {args.min_area_score:g} e até "
             f"{args.area_margin:g} abaixo da área mais próxima. Múltiplas áreas são permitidas; "
             f"{override_count} artigos têm correção manual em `work_area_curated.csv`.",
             "Os valores são similaridades de cosseno, não probabilidades calibradas. "
             "Verifique os artigos e a interpretação institucional das áreas antes de "
             "usar a classificação para decisões do programa.",
             f"Artigos sem área atribuída: {sum(not row['assigned_areas'] for row in classification)}; "
             f"atribuídos a mais de uma área: "
             f"{sum('+' in row['assigned_areas'] for row in classification)}. "
             "Use `review_flags` e `score_gap` para priorizar a conferência manual.",
             "Em `work_area_curated.csv`, `supervisors` lista os orientadores do artigo; "
             "edite `areas` para corrigir (vazio exclui). Alterações manuais são preservadas; "
             "linhas automáticas são atualizadas a cada execução.",
             "Os artigos compartilhados entre dois orientadores são excluídos apenas "
             "da comparação daquele par." if not args.include_shared else
             "Os artigos compartilhados permanecem nas comparações entre orientadores.",
             "", "| Área | Orientadores de referência | Artigos de referência | Artigos atribuídos |",
             "| --- | ---: | ---: | ---: |"]
    for area in AREAS:
        lines.append(f"| {area} | {support[area]['exclusive_authors']} | "
                     f"{support[area]['unique_seed_works']} | "
                     f"{sum(area in row['assigned_areas'].split('+') for row in classification)} |")
    lines += ["", "Um artigo pode contar em mais de uma área. Para cada área, "
              "o perfil de um orientador usa apenas os seus artigos atribuídos àquela área.", ""]
    for area in AREAS:
        rows = [row for row in coverage if row["area"] == area]
        lines += [f"## {area} — {AREA_NAMES[area]}", "",
                  f"{len(rows)} orientadores vinculados; "
                  f"{sum(row['eligible'] for row in rows)} com pelo menos "
                  f"{args.min_area_papers} artigo(s) classificado(s).", "",
                  "| Orientador | Artigos da área | Na rede |",
                  "| --- | ---: | --- |"]
        for row in rows:
            lines.append(f"| {md_cell(row['supervisor'])} | "
                         f"{row['articles_with_embedding']} | {'sim' if row['eligible'] else 'não'} |")
        for kind, title in (("louvain", "Comunidades Louvain"),
                            ("proposed", f"Proposta de até {args.groups} temas")):
            lines += ["", f"### {title}", "",
                      "| ID | Orientadores | Termos distintivos | Artigos representativos |",
                      "| --- | --- | --- | --- |"]
            for row in descriptions:
                if row["area"] == area and row["kind"] == kind:
                    lines.append(f"| {row['id']} | {md_cell(row['members'])} | "
                                 f"{md_cell(row['top_terms'])} | "
                                 f"{md_cell(row['example_titles'])} |")
        lines.append("")
    (DATA / "area_semantic.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main():
    global ROOT, DATA
    args = options()
    ROOT = args.project_root
    DATA = ROOT / "data"
    if not DATA.is_dir():
        raise FileNotFoundError(f"Missing data directory: {DATA}")
    sem.ROOT = ROOT
    sem.DATA = DATA
    names, areas, ids_by_person = sem.load_people()
    raw = sem.raw_directory()
    articles, fields = sem.load_works(names, ids_by_person, raw,
                                     args.start_date, args.end_date)
    overrides, existing, columns, stale_manual, stale_automatic = read_overrides(fields)
    if stale_manual or stale_automatic:
        print(f"Outside the current article set: {len(stale_manual)} manual row(s) to retain; "
              f"{stale_automatic} automatic row(s) to remove from work_area_curated.csv. "
              "Check candidate authors, publication dates, and work type if unexpected.",
              flush=True)
    meta = metadata_for_works(ids_by_person, raw, set(fields), args.start_date, args.end_date)
    weights = {"title": args.title_weight, "abstract": args.abstract_weight,
               "keywords": args.keyword_weight}
    vectors = embedding_cache(fields, args, weights)
    prototypes, support, seeds = reference_profiles(names, areas, articles, vectors)
    assignments, classification = classify(fields, meta, vectors, prototypes,
                                           seeds, args, overrides)
    update_curated(names, articles, classification, overrides, existing, columns,
                   stale_manual)
    print(f"Works curated manually: {len(overrides)}", flush=True)
    coverage, descriptions = area_outputs(names, areas, articles, fields, vectors,
                                          assignments, args)
    write_report(args, support, classification, coverage, descriptions, len(overrides))
    print(DATA / "work_area_suggestions.csv")
    print(DATA / "work_area_curated.csv")
    print(DATA / "area_semantic.graphml")
    print(DATA / "area_semantic.md")


if __name__ == "__main__":
    main()
