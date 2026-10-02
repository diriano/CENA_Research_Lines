#!/usr/bin/env python3
"""Build a Cytoscape network of thematic similarity between curated supervisors.

Usage:
    python scripts/semantic_similarity.py PROJECT_ROOT [--top-k 3]

Inputs (at PROJECT_ROOT or PROJECT_ROOT/data):
    candidates.json, supervisors.json
    data/raw/works_A....json (or raw/works_A....json)

Outputs (at PROJECT_ROOT/data):
    semantic_similarity_edges.csv, semantic_similarity_nodes.csv,
    semantic_similarity_matrix.csv, semantic_similarity.graphml,
    semantic_similarity.md

Requires: pip install numpy sentence-transformers
The first run downloads the selected Sentence Transformers model. Computation
uses the CPU by default; choose --device cuda only when your PyTorch build
supports your GPU architecture.
"""

import argparse
import csv
import datetime
import itertools
import json
import pathlib
import xml.etree.ElementTree as ET

import numpy as np


ROOT = None  # Set from argparse when run directly, or by an importing script.
AREA_ORDER = ("B", "N", "Q")
AREA_LABELS = {
    "B": "Biologia na Agricultura e no Ambiente",
    "N": "Energia Nuclear na Agricultura e no Ambiente",
    "Q": "Química na Agricultura e no Ambiente",
}
DEFAULT_MODEL = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"


def options():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project_root", type=pathlib.Path, metavar="PROJECT_ROOT",
                        help="Directory containing candidates.json and the work files")
    parser.add_argument("--model", default=DEFAULT_MODEL,
                        help="Sentence Transformers model name or local model path")
    parser.add_argument("--start-date", default="2021-01-01")
    parser.add_argument("--end-date", default="2026-12-31")
    parser.add_argument("--top-k", type=int, default=3,
                        help="Nearest neighbors per supervisor (undirected union; default: 3)")
    parser.add_argument("--min-similarity", type=float, default=0.0,
                        help="Minimum cosine similarity for an edge (default: 0)")
    parser.add_argument("--batch-size", type=int, default=32)
    parser.add_argument("--device", default="cpu",
                        help="Embedding device (default: cpu; use cuda only with a compatible GPU)")
    parser.add_argument("--title-weight", type=float, default=0.25)
    parser.add_argument("--abstract-weight", type=float, default=0.60)
    parser.add_argument("--keyword-weight", type=float, default=0.15)
    parser.add_argument("--include-shared", action="store_true",
                        help="Include shared coauthored papers when comparing two supervisors")
    args = parser.parse_args()
    if args.top_k < 1 or args.batch_size < 1:
        parser.error("--top-k and --batch-size must be positive")
    try:
        start = datetime.date.fromisoformat(args.start_date)
        end = datetime.date.fromisoformat(args.end_date)
    except ValueError:
        parser.error("Invalid publication date; use YYYY-MM-DD")
    if start > end:
        parser.error("Invalid publication date range; use YYYY-MM-DD")
    weights = (args.title_weight, args.abstract_weight, args.keyword_weight)
    if any(w < 0 for w in weights) or not any(weights):
        parser.error("Field weights must be nonnegative, with at least one positive weight")
    if not -1 <= args.min_similarity <= 1:
        parser.error("--min-similarity must be between -1 and 1")
    return args


def unique_file(filename):
    matches = [p for p in (ROOT / filename, ROOT / "data" / filename) if p.is_file()]
    if len(matches) != 1:
        raise FileNotFoundError(
            f"Expected exactly one {filename} in {ROOT} or {ROOT / 'data'}; found {matches}"
        )
    return matches[0]


def raw_directory():
    matches = [p for p in (ROOT / "data" / "raw", ROOT / "raw") if p.is_dir()]
    if len(matches) != 1:
        raise FileNotFoundError(f"Expected exactly one raw works directory; found {matches}")
    return matches[0]


def short_id(value):
    return str(value).rstrip("/").rsplit("/", 1)[-1]


def load_people():
    curated = json.loads(unique_file("candidates.json").read_text(encoding="utf-8"))
    records = json.loads(unique_file("supervisors.json").read_text(encoding="utf-8"))
    if not isinstance(curated, list) or not isinstance(records, list):
        raise ValueError("Both candidates.json and supervisors.json must contain lists")
    names = [item["name"] for item in curated]
    if len(names) != len(set(names)):
        raise ValueError("Duplicate supervisor names in candidates.json")
    area_by_name = {}
    for item in records:
        name = item["name"]
        if name in area_by_name:
            raise ValueError(f"Duplicate name in supervisors.json: {name}")
        codes = set(item["areas"])
        if codes - set(AREA_ORDER):
            raise ValueError(f"Unknown area code for {name}: {codes - set(AREA_ORDER)}")
        area_by_name[name] = [code for code in AREA_ORDER if code in codes]
    if set(names) != set(area_by_name):
        raise ValueError("Names differ between candidates.json and supervisors.json: "
                         f"missing={sorted(set(names) - set(area_by_name))}, "
                         f"extra={sorted(set(area_by_name) - set(names))}")
    owner_by_id = {}
    ids_by_person = []
    for index, item in enumerate(curated):
        author_ids = list(dict.fromkeys(short_id(candidate["id"])
                                        for candidate in item["candidates"]))
        ids_by_person.append(author_ids)
        for author_id in author_ids:
            if author_id in owner_by_id:
                raise ValueError(f"Author {author_id} assigned to two supervisors")
            owner_by_id[author_id] = index
    return names, area_by_name, ids_by_person


def in_period(work, start_date, end_date):
    date = work.get("publication_date")
    if isinstance(date, str) and len(date) >= 10:
        return start_date <= date[:10] <= end_date
    year = work.get("publication_year")
    return isinstance(year, int) and int(start_date[:4]) <= year <= int(end_date[:4])


def reconstructed_abstract(work):
    abstract = work.get("abstract")
    if isinstance(abstract, str) and abstract.strip():
        return abstract.strip()
    inverted = work.get("abstract_inverted_index")
    if not isinstance(inverted, dict) or not inverted:
        return ""
    words = sorted((pos, word) for word, positions in inverted.items()
                   for pos in positions)
    return " ".join(word for _, word in words)


def keyword_text(work):
    keywords = work.get("keywords") or []
    if not isinstance(keywords, list):
        return ""
    values = []
    for keyword in keywords:
        value = (keyword.get("display_name") or keyword.get("name")
                 if isinstance(keyword, dict) else keyword)
        if isinstance(value, str) and value.strip():
            values.append(value.strip())
    return "; ".join(dict.fromkeys(values))


def fields(work):
    title = work.get("title") or work.get("display_name") or ""
    return {
        "title": title.strip() if isinstance(title, str) else "",
        "abstract": reconstructed_abstract(work),
        "keywords": keyword_text(work),
    }


def load_works(names, ids_by_person, raw_dir, start_date, end_date):
    articles_by_person = []
    fields_by_work = {}
    for name, author_ids in zip(names, ids_by_person):
        article_ids = set()
        for author_id in author_ids:
            path = raw_dir / f"works_{author_id}.json"
            if not path.is_file():
                raise FileNotFoundError(f"Missing works file for {name}: {path}")
            data = json.loads(path.read_text(encoding="utf-8"))
            if not isinstance(data, list):
                raise ValueError(f"Expected list of works: {path}")
            for work in data:
                if work.get("type") != "article" or not in_period(work, start_date, end_date):
                    continue
                if not work.get("id"):
                    raise ValueError(f"Article without OpenAlex ID in {path}")
                wid = short_id(work["id"])
                article_ids.add(wid)
                record = fields(work)
                previous = fields_by_work.setdefault(wid, {"title": "", "abstract": "", "keywords": ""})
                for key in previous:
                    if len(record[key]) > len(previous[key]):
                        previous[key] = record[key]
        articles_by_person.append(article_ids)
    return articles_by_person, fields_by_work


def unit(vector):
    norm = np.linalg.norm(vector)
    return vector / norm if norm > 1e-12 else None


def embed_works(fields_by_work, model_name, batch_size, weights, device="cpu"):
    from sentence_transformers import SentenceTransformer

    model = SentenceTransformer(model_name, device=device)
    max_tokens = min(112, int(model.max_seq_length) - 2)
    if max_tokens < 1:
        raise ValueError("Model maximum sequence length is too short to encode text")
    tokenizer = model.tokenizer
    texts = []
    locations = {}  # (work ID, field name) -> indices into texts
    for wid in sorted(fields_by_work):
        for field_name in ("title", "abstract", "keywords"):
            value = fields_by_work[wid][field_name]
            if not value or weights[field_name] == 0:
                continue
            # Tokenize without truncation and split *all* fields before model
            # inference. verbose=False suppresses the premature length warning
            # emitted while tokenizing the full text, which is never sent to
            # the model in that form.
            tokens = tokenizer.encode(value, add_special_tokens=False, verbose=False)
            parts = [tokenizer.decode(tokens[i:i + max_tokens], skip_special_tokens=True)
                     for i in range(0, len(tokens), max_tokens)]
            if not parts:
                continue
            locations[(wid, field_name)] = list(range(len(texts), len(texts) + len(parts)))
            texts.extend(parts)

    if not texts:
        raise ValueError("No title, abstract or keyword text with positive weight found in the selected articles")
    print(f"Encoding {len(texts)} text segments from {len(fields_by_work)} unique articles "
          f"on {device}...", flush=True)
    vectors = np.asarray(model.encode(texts, batch_size=batch_size,
                                      device=device,
                                      normalize_embeddings=True,
                                      convert_to_numpy=True,
                                      show_progress_bar=True), dtype=np.float64)
    result = {}
    for wid in fields_by_work:
        combined = np.zeros(vectors.shape[1], dtype=np.float64)
        total_weight = 0.0
        for field_name, weight in weights.items():
            indices = locations.get((wid, field_name), [])
            if not indices:
                continue
            field_vector = unit(vectors[indices].mean(axis=0))
            if field_vector is not None:
                combined += weight * field_vector
                total_weight += weight
        if total_weight:
            normalized = unit(combined / total_weight)
            if normalized is not None:
                result[wid] = normalized
    return result


def compare_people(names, articles_by_person, work_vectors, include_shared):
    vector_ids = set(work_vectors)
    used = [ids & vector_ids for ids in articles_by_person]
    if not work_vectors:
        raise ValueError("No usable articles were embedded")
    dim = len(next(iter(work_vectors.values())))
    sums = [sum((work_vectors[wid] for wid in ids), np.zeros(dim, dtype=np.float64))
            for ids in used]
    pairs = {}
    for i, j in itertools.combinations(range(len(names)), 2):
        shared = used[i] & used[j]
        excluded = shared if not include_shared else set()
        ni, nj = len(used[i]) - len(excluded), len(used[j]) - len(excluded)
        score = None
        if ni and nj:
            common = sum((work_vectors[wid] for wid in excluded),
                         np.zeros(dim, dtype=np.float64))
            vi, vj = unit(sums[i] - common), unit(sums[j] - common)
            if vi is not None and vj is not None:
                score = float(np.clip(np.dot(vi, vj), -1, 1))
        pairs[(i, j)] = (score, len(shared), ni, nj)
    return used, pairs


def select_edges(names, pairs, top_k, minimum):
    neighbors = [[] for _ in names]
    for (i, j), (score, _shared, _ni, _nj) in pairs.items():
        if score is not None and score >= minimum:
            neighbors[i].append((j, score))
            neighbors[j].append((i, score))
    chosen = set()
    for i, candidates in enumerate(neighbors):
        for j, _score in sorted(candidates, key=lambda item: (-item[1], names[item[0]]))[:top_k]:
            chosen.add((min(i, j), max(i, j)))
    return sorted(chosen, key=lambda pair: (-pairs[pair][0], names[pair[0]], names[pair[1]]))


def nodes(names, area_by_name, articles_by_person, used, fields_by_work):
    for name, all_ids, text_ids in zip(names, articles_by_person, used):
        areas = area_by_name[name]
        yield {
            "id": name,
            "label": name,
            "area_group": "+".join(areas),
            "area_names": "; ".join(AREA_LABELS[area] for area in areas),
            **{f"in_{area}": int(area in areas) for area in AREA_ORDER},
            "article_count": len(all_ids),
            "text_article_count": len(text_ids),
            "abstract_count": sum(bool(fields_by_work[wid]["abstract"]) for wid in all_ids),
            "keyword_count": sum(bool(fields_by_work[wid]["keywords"]) for wid in all_ids),
        }


def write_csv(path, rows, columns):
    with path.open("w", encoding="utf-8", newline="") as out:
        writer = csv.DictWriter(out, fieldnames=columns)
        writer.writeheader()
        writer.writerows(rows)


def graphml(path, node_rows, edge_rows):
    ns = "http://graphml.graphdrawing.org/xmlns"
    ET.register_namespace("", ns)

    def tag(value):
        return f"{{{ns}}}{value}"

    root = ET.Element(tag("graphml"))
    node_types = {"label": "string", "area_group": "string", "area_names": "string",
                  "in_B": "int", "in_N": "int", "in_Q": "int",
                  "article_count": "int", "text_article_count": "int",
                  "abstract_count": "int", "keyword_count": "int"}
    edge_types = {"weight": "double", "similarity": "double",
                  "shared_article_count": "int", "source_articles_compared": "int",
                  "target_articles_compared": "int"}
    for target, columns in (("node", node_types), ("edge", edge_types)):
        for name, kind in columns.items():
            ET.SubElement(root, tag("key"), {"id": name, "for": target,
                                               "attr.name": name, "attr.type": kind})
    graph = ET.SubElement(root, tag("graph"),
                          {"id": "semantic_similarity", "edgedefault": "undirected"})
    name_to_id = {row["id"]: f"n{i}" for i, row in enumerate(node_rows)}
    for row in node_rows:
        element = ET.SubElement(graph, tag("node"), {"id": name_to_id[row["id"]]})
        for key in node_types:
            ET.SubElement(element, tag("data"), {"key": key}).text = str(row[key])
    for i, row in enumerate(edge_rows):
        element = ET.SubElement(graph, tag("edge"), {
            "id": f"e{i}", "source": name_to_id[row["source"]],
            "target": name_to_id[row["target"]]
        })
        for key in edge_types:
            ET.SubElement(element, tag("data"), {"key": key}).text = str(row[key])
    tree = ET.ElementTree(root)
    ET.indent(tree, space="  ")
    tree.write(path, encoding="utf-8", xml_declaration=True)


def main():
    global ROOT
    args = options()
    ROOT = args.project_root
    names, area_by_name, ids_by_person = load_people()
    articles, texts = load_works(names, ids_by_person, raw_directory(),
                                 args.start_date, args.end_date)
    weights = {"title": args.title_weight, "abstract": args.abstract_weight,
               "keywords": args.keyword_weight}
    work_vectors = embed_works(texts, args.model, args.batch_size, weights, args.device)
    used, pairs = compare_people(names, articles, work_vectors, args.include_shared)
    chosen = select_edges(names, pairs, args.top_k, args.min_similarity)
    node_rows = list(nodes(names, area_by_name, articles, used, texts))
    node_columns = list(node_rows[0]) if node_rows else []
    write_csv(ROOT / "data" / "semantic_similarity_nodes.csv", node_rows, node_columns)

    edge_rows = []
    for i, j in chosen:
        score, shared, ni, nj = pairs[(i, j)]
        edge_rows.append({"source": names[i], "target": names[j],
                          "weight": f"{score:.6f}", "similarity": f"{score:.6f}",
                          "shared_article_count": shared,
                          "source_articles_compared": ni,
                          "target_articles_compared": nj})
    edge_columns = ("source", "target", "weight", "similarity",
                    "shared_article_count", "source_articles_compared",
                    "target_articles_compared")
    write_csv(ROOT / "data" / "semantic_similarity_edges.csv", edge_rows, edge_columns)

    with (ROOT / "data" / "semantic_similarity_matrix.csv").open("w", encoding="utf-8", newline="") as out:
        writer = csv.writer(out)
        writer.writerow(["supervisor", *names])
        for i, name in enumerate(names):
            row = [name]
            for j in range(len(names)):
                if i == j:
                    row.append("1.000000" if used[i] else "")
                else:
                    score = pairs[(min(i, j), max(i, j))][0]
                    row.append(f"{score:.6f}" if score is not None else "")
            writer.writerow(row)
    graphml(ROOT / "data" / "semantic_similarity.graphml", node_rows, edge_rows)

    lines = ["# Rede de similaridade temática", "",
             f"Período: {args.start_date} a {args.end_date}; apenas trabalhos OpenAlex com `type = article`.",
             f"Modelo: `{args.model}`. Um vetor por artigo a partir de título ({args.title_weight:g}), "
             f"abstract ({args.abstract_weight:g}) e keywords ({args.keyword_weight:g}); "
             "pesos dos campos presentes são renormalizados. Abstracts longos são processados em partes.",
             "Cada orientador é representado pela direção média dos vetores de seus artigos. "
             "O peso da aresta é a similaridade de cosseno entre os perfis de dois orientadores.",
             ("Artigos em coautoria entre o par de orientadores foram incluídos na comparação."
              if args.include_shared else
              "Artigos em coautoria entre o par de orientadores foram excluídos da comparação desse par."),
             f"A rede usa a união dos {args.top_k} vizinhos mais próximos de cada orientador "
             f"(similaridade mínima {args.min_similarity:g}). A matriz CSV contém todos os pares comparáveis.",
             "Células vazias da matriz indicam ausência de artigos com texto para comparar após a exclusão.",
             "", "| Orientador | Áreas | Artigos | Com texto | Com abstract | Com keywords |",
             "| --- | --- | ---: | ---: | ---: | ---: |"]
    for row in node_rows:
        name = row["label"].replace("|", r"\|")
        lines.append(f"| {name} | {row['area_group']} | {row['article_count']} | "
                     f"{row['text_article_count']} | {row['abstract_count']} | "
                     f"{row['keyword_count']} |")
    lines += ["", "## Ligações mais fortes", "",
              "| Orientador 1 | Orientador 2 | Similaridade | Artigos compartilhados |",
              "| --- | --- | ---: | ---: |"]
    for row in edge_rows[:20]:
        source = row["source"].replace("|", r"\|")
        target = row["target"].replace("|", r"\|")
        lines.append(f"| {source} | {target} | {row['weight']} | "
                     f"{row['shared_article_count']} |")
    (ROOT / "data" / "semantic_similarity.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"{len(names)} supervisors; {len(work_vectors)} articles with text; "
          f"{len(edge_rows)} edges; {sum(not ids for ids in used)} nodes without text")
    for filename in ("semantic_similarity_edges.csv", "semantic_similarity_nodes.csv",
                     "semantic_similarity_matrix.csv", "semantic_similarity.graphml",
                     "semantic_similarity.md"):
        print(ROOT / "data" / filename)


if __name__ == "__main__":
    main()
