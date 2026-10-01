#!/usr/bin/env python3
"""Build a coauthorship edge list from curated OpenAlex author work files.

Usage:
    python scripts/coauthorship.py PROJECT_ROOT

Input:
    PROJECT_ROOT/candidates.json or PROJECT_ROOT/data/candidates.json
    PROJECT_ROOT/supervisors.json or PROJECT_ROOT/data/supervisors.json
    PROJECT_ROOT/data/raw/works_<OpenAlex-author-ID>.json
    (PROJECT_ROOT/raw is also supported)

Output:
    PROJECT_ROOT/data/coauthorship_edges.csv
    PROJECT_ROOT/data/coauthorship_nodes.csv
    PROJECT_ROOT/data/coauthorship.graphml
    PROJECT_ROOT/data/coauthorship.md

Only OpenAlex works with type == "article" and publication dates in 2021–2026
are counted. A work is counted once per supervisor, even if the supervisor has
multiple curated OpenAlex author IDs or the work is repeated in a cache file.
Use the nodes CSV as a Cytoscape node table. Its id column matches the names
used in the edge list; area_group is a category suitable for discrete colors.
"""

import collections
import csv
import itertools
import json
import pathlib
import sys
import xml.etree.ElementTree as ET


if len(sys.argv) != 2:
    raise SystemExit(f"Usage: python {sys.argv[0]} PROJECT_ROOT")

ROOT = pathlib.Path(sys.argv[1])
START_DATE = "2021-01-01"
END_DATE = "2026-12-31"
AREA_ORDER = ("B", "N", "Q")
AREA_LABELS = {
    "B": "Biologia na Agricultura e no Ambiente",
    "N": "Energia Nuclear na Agricultura e no Ambiente",
    "Q": "Química na Agricultura e no Ambiente",
}


def find_unique_file(filename):
    possible = [ROOT / filename, ROOT / "data" / filename]
    found = [path for path in possible if path.is_file()]
    if not found:
        raise FileNotFoundError(f"{filename} not found in {ROOT} or {ROOT / 'data'}")
    if len(found) > 1:
        raise ValueError(
            f"Two {filename} files found; keep only the intended one: {found}"
        )
    return found[0]


def find_raw_dir():
    possible = [ROOT / "data" / "raw", ROOT / "raw"]
    for path in possible:
        if path.is_dir():
            return path
    raise FileNotFoundError(f"No works directory found in {possible}")


def load_areas(names):
    records = json.loads(find_unique_file("supervisors.json").read_text(encoding="utf-8"))
    if not isinstance(records, list):
        raise ValueError("supervisors.json must contain a list")
    by_name = {}
    for record in records:
        name = record["name"]
        if name in by_name:
            raise ValueError(f"Duplicate supervisor in supervisors.json: {name}")
        codes = set(record["areas"])
        unknown = codes - set(AREA_ORDER)
        if unknown:
            raise ValueError(f"Unknown area codes for {name}: {sorted(unknown)}")
        by_name[name] = [code for code in AREA_ORDER if code in codes]
    if set(by_name) != set(names):
        missing = sorted(set(names) - set(by_name))
        extra = sorted(set(by_name) - set(names))
        raise ValueError(f"Name mismatch between JSON files; missing={missing}, extra={extra}")
    return by_name


def openalex_short_id(value):
    """Accept either an OpenAlex URL or its short A.../W... ID."""
    return value.rstrip("/").rsplit("/", 1)[-1]


def in_period(work):
    date = work.get("publication_date")
    if isinstance(date, str) and len(date) >= 10:
        return START_DATE <= date[:10] <= END_DATE
    year = work.get("publication_year")
    return isinstance(year, int) and int(START_DATE[:4]) <= year <= int(END_DATE[:4])


def read_article_ids(path):
    works = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(works, list):
        raise ValueError(f"Expected a JSON list of works in {path}")

    article_ids = set()
    for work in works:
        if work.get("type") != "article" or not in_period(work):
            continue
        work_id = work.get("id")
        if not work_id:
            raise ValueError(f"An article in {path} has no OpenAlex work ID")
        article_ids.add(openalex_short_id(work_id))
    return article_ids


def markdown_cell(value):
    return str(value).replace("|", r"\|").replace("\n", " ")


def write_graphml(path, names, areas_by_name, articles_by_supervisor, pair_counts):
    """Write a Cytoscape-ready graph that also retains isolated supervisors."""
    namespace = "http://graphml.graphdrawing.org/xmlns"
    ET.register_namespace("", namespace)

    def tag(local_name):
        return f"{{{namespace}}}{local_name}"

    root = ET.Element(tag("graphml"))
    columns = (
        ("label", "node", "string"),
        ("area_group", "node", "string"),
        ("area_names", "node", "string"),
        ("in_B", "node", "int"),
        ("in_N", "node", "int"),
        ("in_Q", "node", "int"),
        ("article_count", "node", "int"),
        ("weight", "edge", "int"),
    )
    for column, target, kind in columns:
        ET.SubElement(root, tag("key"), {
            "id": column, "for": target, "attr.name": column, "attr.type": kind
        })
    graph = ET.SubElement(root, tag("graph"), {
        "id": "coauthorship", "edgedefault": "undirected"
    })

    for index, (name, articles) in enumerate(zip(names, articles_by_supervisor)):
        codes = areas_by_name[name]
        node = ET.SubElement(graph, tag("node"), {"id": f"n{index}"})
        values = {
            "label": name,
            "area_group": "+".join(codes),
            "area_names": "; ".join(AREA_LABELS[code] for code in codes),
            "article_count": len(articles),
            **{f"in_{code}": int(code in codes) for code in AREA_ORDER},
        }
        for key, value in values.items():
            ET.SubElement(node, tag("data"), {"key": key}).text = str(value)

    for (source, target), weight in sorted(pair_counts.items()):
        edge = ET.SubElement(graph, tag("edge"), {
            "source": f"n{source}", "target": f"n{target}"
        })
        ET.SubElement(edge, tag("data"), {"key": "weight"}).text = str(weight)

    tree = ET.ElementTree(root)
    ET.indent(tree, space="  ")
    tree.write(path, encoding="utf-8", xml_declaration=True)


def main():
    candidates_path = find_unique_file("candidates.json")
    supervisors = json.loads(candidates_path.read_text(encoding="utf-8"))
    if not isinstance(supervisors, list):
        raise ValueError("candidates.json must contain a list of supervisors")

    names = []
    author_ids = []
    seen_names = set()
    owner_by_id = {}

    for index, entry in enumerate(supervisors):
        name = entry["name"]
        if name in seen_names:
            raise ValueError(f"Duplicate supervisor name: {name}")
        seen_names.add(name)
        names.append(name)

        ids = list(dict.fromkeys(
            openalex_short_id(candidate["id"])
            for candidate in entry["candidates"]
        ))
        for author_id in ids:
            if author_id in owner_by_id:
                other = names[owner_by_id[author_id]]
                raise ValueError(
                    f"OpenAlex author {author_id} assigned to both {other} and {name}"
                )
            owner_by_id[author_id] = index
        author_ids.append(ids)

    areas_by_name = load_areas(names)
    raw_dir = find_raw_dir()
    articles_by_supervisor = []
    for name, ids in zip(names, author_ids):
        article_ids = set()
        for author_id in ids:
            path = raw_dir / f"works_{author_id}.json"
            if not path.is_file():
                raise FileNotFoundError(f"Missing works file for {name}: {path}")
            article_ids.update(read_article_ids(path))
        articles_by_supervisor.append(article_ids)

    supervisors_by_article = collections.defaultdict(set)
    for index, article_ids in enumerate(articles_by_supervisor):
        for article_id in article_ids:
            supervisors_by_article[article_id].add(index)

    pair_counts = collections.Counter()
    for indices in supervisors_by_article.values():
        for pair in itertools.combinations(sorted(indices), 2):
            pair_counts[pair] += 1

    edges = sorted(
        ((names[i], names[j], weight) for (i, j), weight in pair_counts.items()),
        key=lambda row: (-row[2], row[0], row[1]),
    )

    edge_path = ROOT / "data" / "coauthorship_edges.csv"
    with edge_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(("source", "target", "weight"))
        writer.writerows(edges)

    node_path = ROOT / "data" / "coauthorship_nodes.csv"
    with node_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(("id", "label", "area_group", "area_names", "in_B", "in_N", "in_Q", "article_count"))
        for name, article_ids in zip(names, articles_by_supervisor):
            codes = areas_by_name[name]
            writer.writerow((
                name, name, "+".join(codes),
                "; ".join(AREA_LABELS[code] for code in codes),
                *(int(code in codes) for code in AREA_ORDER),
                len(article_ids),
            ))

    graphml_path = ROOT / "data" / "coauthorship.graphml"
    write_graphml(graphml_path, names, areas_by_name, articles_by_supervisor, pair_counts)

    md_path = ROOT / "data" / "coauthorship.md"
    lines = [
        f"# Artigos por orientador ({START_DATE[:4]}–{END_DATE[:4]})",
        "",
        "Critério: trabalhos do OpenAlex com `type = article` e data de publicação "
        f"entre {START_DATE} e {END_DATE}. Cada ID de artigo é contado uma vez por "
        "orientador. As coautorias incluem somente os orientadores em `candidates.json`.",
        "",
        "Áreas: B = Biologia; N = Energia Nuclear; Q = Química na Agricultura e no Ambiente.",
        "",
        "| Orientador | Áreas | Número de artigos |",
        "| --- | --- | ---: |",
    ]
    lines.extend(
        f"| {markdown_cell(name)} | {'+'.join(areas_by_name[name])} | {len(article_ids)} |"
        for name, article_ids in zip(names, articles_by_supervisor)
    )
    md_path.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(
        f"{len(names)} supervisors; {len(supervisors_by_article)} distinct articles; "
        f"{len(edges)} coauthorship edges"
    )
    print(edge_path)
    print(node_path)
    print(graphml_path)
    print(md_path)


if __name__ == "__main__":
    main()
