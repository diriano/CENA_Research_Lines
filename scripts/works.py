#!/usr/bin/env python3
"""Retrieve 2021–2025 OpenAlex works for manually curated author candidates.

Usage:
    python scripts/works.py PROJECT_ROOT

The script looks for candidates.json in PROJECT_ROOT or PROJECT_ROOT/data.
"""

import concurrent.futures
import json
import pathlib
import sys
import time
import urllib.parse
import urllib.error
import urllib.request


if len(sys.argv) != 2:
    raise SystemExit(f"Usage: python {sys.argv[0]} PROJECT_ROOT")

ROOT = pathlib.Path(sys.argv[1])
RAW = ROOT / "data" / "raw"


def get(url):
    """Fetch one OpenAlex JSON response."""
    request = urllib.request.Request(
        url,
        headers={"Accept": "application/json", "User-Agent": "PPG-Ciencias-Research-Lines/1.0"},
    )
    for attempt in range(5):
        try:
            with urllib.request.urlopen(request, timeout=60) as response:
                return json.load(response)
        except urllib.error.HTTPError as exc:
            if exc.code not in (429, 500, 502, 503, 504) or attempt == 4:
                raise
            retry_after = exc.headers.get("Retry-After")
            delay = float(retry_after) if retry_after and retry_after.isdigit() else 2 ** attempt
        except urllib.error.URLError:
            if attempt == 4:
                raise
            delay = 2 ** attempt
        time.sleep(delay)


def candidates_path():
    paths = [ROOT / "candidates.json", ROOT / "data" / "candidates.json"]
    matches = [path for path in paths if path.is_file()]
    if not matches:
        raise FileNotFoundError(
            f"candidates.json was not found in {ROOT} or {ROOT / 'data'}"
        )
    if len(matches) > 1:
        raise ValueError(
            "Two candidates.json files were found. Keep only the curated one "
            f"or change candidates_path(): {matches}"
        )
    return matches[0]


def retrieve(spec):
    index, name, aid = spec
    dest = RAW / f"works_{aid}.json"

    if dest.exists():
        data = json.loads(dest.read_text(encoding="utf-8"))
    else:
        data = []
        cursor = "*"
        while cursor:
            params = {
                "filter": (
                    f"author.id:{aid},"
                    "from_publication_date:2021-01-01,"
                    "to_publication_date:2025-12-31"
                ),
                "per-page": 200,
                "cursor": cursor,
            }
            url = "https://api.openalex.org/works?" + urllib.parse.urlencode(params)
            page = get(url)
            works = page["results"]
            data.extend(works)
            cursor = page["meta"].get("next_cursor") if works else None

        # Avoid leaving an incomplete cache file if writing is interrupted.
        temporary = dest.with_suffix(".json.tmp")
        temporary.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
        temporary.replace(dest)

    print(
        json.dumps({"author": name, "id": aid, "count": len(data)}, ensure_ascii=False),
        flush=True,
    )
    return {"index": index, "id": aid, "works": len(data)}


def main():
    source = candidates_path()
    try:
        curated = json.loads(source.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Invalid JSON in {source}: {exc}") from exc

    if not isinstance(curated, list):
        raise ValueError("candidates.json must contain a list of supervisors")

    selected = []
    specs = []
    seen_names = set()
    for index, entry in enumerate(curated):
        name = entry["name"]
        if name in seen_names:
            raise ValueError(f"Duplicate supervisor in candidates.json: {name}")
        seen_names.add(name)

        candidates = entry["candidates"]
        ids = list(
            dict.fromkeys(candidate["id"].rstrip("/").split("/")[-1]
                          for candidate in candidates)
        )
        if not ids:
            continue

        # Keep the original single-candidate fields for later scripts.
        first = candidates[0]
        selected.append({
            "name": name,
            "index": index,
            "ids": ids,
            "orcid": first.get("orcid") if len(candidates) == 1 else None,
            "openalex_name": first.get("name") if len(candidates) == 1 else None,
            "candidates": candidates,
        })
        specs.extend((index, name, aid) for aid in ids)

    RAW.mkdir(parents=True, exist_ok=True)
    (ROOT / "selected_authors.json").write_text(
        json.dumps(selected, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        results = list(executor.map(retrieve, specs))

    (ROOT / "retrieval_log.json").write_text(
        json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8"
    )


if __name__ == "__main__":
    main()

