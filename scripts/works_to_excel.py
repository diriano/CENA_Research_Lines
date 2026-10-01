#!/usr/bin/env python3
"""Export cached OpenAlex works of curated candidates to an Excel workbook.

Usage:
    python scripts/works_to_excel.py PROJECT_ROOT

Reads PROJECT_ROOT/data/candidates.json (or PROJECT_ROOT/data/candidates.json)
and PROJECT_ROOT/data/raw/works_<OpenAlex-author-ID>.json. Creates
PROJECT_ROOT/data/candidate_publications.xlsx. Requires: pip install openpyxl

Each row represents one candidate/work pair. A work shared by two candidates
appears twice, once for each candidate. Multiple OpenAlex IDs for the same
candidate are combined, without duplicating that candidate's work.
"""

import json
import pathlib
import sys

try:
    from openpyxl import Workbook
    from openpyxl.styles import Alignment, Font, PatternFill
    from openpyxl.utils import get_column_letter
except ImportError as exc:
    raise SystemExit("Install the Excel dependency with: python -m pip install openpyxl") from exc


if len(sys.argv) != 2:
    raise SystemExit(f"Usage: python {sys.argv[0]} PROJECT_ROOT")

ROOT = pathlib.Path(sys.argv[1])
RAW = ROOT / "data" / "raw"
OUTPUT = ROOT / "data" / "candidate_publications.xlsx"


def candidates_path():
    paths = [ROOT / "candidates.json", ROOT / "data" / "candidates.json"]
    found = [path for path in paths if path.is_file()]
    if not found:
        raise FileNotFoundError(f"candidates.json not found in {ROOT} or {ROOT / 'data'}")
    if len(found) > 1:
        raise ValueError(
            "Two candidates.json files found; keep only the curated one: "
            + ", ".join(map(str, found))
        )
    return found[0]


def short_id(openalex_id):
    return openalex_id.rstrip("/").rsplit("/", 1)[-1]


def byline(work):
    names = []
    for authorship in work.get("authorships") or []:
        author = authorship.get("author") or {}
        name = author.get("display_name") or authorship.get("raw_author_name")
        if name:
            names.append(name)
    return "; ".join(names)


def read_rows():
    curated = json.loads(candidates_path().read_text(encoding="utf-8"))
    if not isinstance(curated, list):
        raise ValueError("candidates.json must contain a list")

    rows = []
    seen_names = set()
    owner_by_id = {}
    for entry in curated:
        candidate_name = entry["name"]
        if candidate_name in seen_names:
            raise ValueError(f"Duplicate candidate: {candidate_name}")
        seen_names.add(candidate_name)

        author_ids = list(dict.fromkeys(
            short_id(candidate["id"]) for candidate in entry["candidates"]
        ))
        works_by_id = {}
        for author_id in author_ids:
            if author_id in owner_by_id:
                raise ValueError(
                    f"OpenAlex author {author_id} assigned to both "
                    f"{owner_by_id[author_id]} and {candidate_name}"
                )
            owner_by_id[author_id] = candidate_name

            path = RAW / f"works_{author_id}.json"
            if not path.is_file():
                raise FileNotFoundError(f"Missing works file for {candidate_name}: {path}")
            works = json.loads(path.read_text(encoding="utf-8"))
            if not isinstance(works, list):
                raise ValueError(f"Expected a JSON list in {path}")
            for work in works:
                work_id = work.get("id")
                if not work_id:
                    raise ValueError(f"Work without OpenAlex ID in {path}")
                works_by_id[short_id(work_id)] = work

        for work_id, work in works_by_id.items():
            doi = work.get("doi") or (work.get("ids") or {}).get("doi") or ""
            rows.append((
                work.get("title") or work.get("display_name") or "",
                doi,
                byline(work),
                candidate_name,
                work.get("publication_year") or "",
                work.get("type") or "",
                work_id,
            ))

    rows.sort(key=lambda row: (row[3].casefold(), -(row[4] or 0), row[0].casefold()))
    return rows


def write_excel(rows):
    workbook = Workbook()
    sheet = workbook.active
    sheet.title = "Publications"
    headers = ("Paper title", "DOI", "Authors", "Candidate", "Year", "Type", "OpenAlex ID")
    sheet.append(headers)

    for row in rows:
        sheet.append(row)

    header_fill = PatternFill("solid", fgColor="17365D")
    for cell in sheet[1]:
        cell.fill = header_fill
        cell.font = Font(color="FFFFFF", bold=True)
        cell.alignment = Alignment(vertical="center")
    sheet.row_dimensions[1].height = 26

    widths = (62, 42, 80, 37, 12, 20, 19)
    for index, width in enumerate(widths, 1):
        sheet.column_dimensions[get_column_letter(index)].width = width

    for row in sheet.iter_rows(min_row=2):
        for cell in row:
            cell.alignment = Alignment(vertical="top", wrap_text=cell.column in (1, 3))
            if isinstance(cell.value, str):
                # Treat source metadata as text, never as an Excel formula.
                cell.data_type = "s"
        doi_cell = row[1]
        if isinstance(doi_cell.value, str) and doi_cell.value.startswith("https://doi.org/"):
            doi_cell.hyperlink = doi_cell.value
            doi_cell.font = Font(color="0563C1", underline="single")

    sheet.freeze_panes = "A2"
    sheet.auto_filter.ref = sheet.dimensions
    workbook.save(OUTPUT)


def main():
    rows = read_rows()  # Fail before writing if a candidate's works file is missing.
    write_excel(rows)
    print(f"Saved {len(rows)} candidate/work rows to {OUTPUT}")


if __name__ == "__main__":
    main()
