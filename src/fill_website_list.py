#!/usr/bin/env python3
"""Fill static_data/websites.json from a pasted "Institution Name    URL" list.

Usage (pasted block as one quoted argument):

    python3 src/fill_website_list.py "LTL Holdings (Pvt.) Ltd.    https://www.ltl.lk/
Lanka Coal Company (Pvt) Ltd    https://lankacoal.lk/"

Unquoted pastes also work (URL-looking tokens separate the names), and with
no arguments the script reads the list from standard input:

    cat list.txt | python3 src/fill_website_list.py

New entries are merged under the "--section" group (default "Imported
Websites"); existing URLs are skipped and existing names updated. Only
previously unseen URLs are added.
"""

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WEBSITES = ROOT / "static_data" / "websites.json"
DEFAULT_SECTION = "Imported Websites"

URL_TOKEN = re.compile(
    r"^(?:[a-z0-9]+://)?[a-z0-9-]+(?:\.[a-z0-9-]+)+(?:[/:?#][^\s]*)?$",
    re.IGNORECASE,
)


def parse_lines(text: str) -> list[tuple[str, str]]:
    entries = []
    for raw in text.splitlines():
        line = raw.strip()
        if not line:
            continue
        parts = line.rsplit(None, 1)
        if len(parts) != 2:
            print(f"  ! skipped (no URL on line): {line!r}")
            continue
        name, url = parts
        entries.append((name.strip(), url.strip()))
    return entries


def parse_tokens(tokens: list[str]) -> list[tuple[str, str]]:
    entries = []
    name_words = []
    for token in tokens:
        if URL_TOKEN.match(token):
            if not name_words:
                print(f"  ! skipped (URL with no name): {token}")
                continue
            entries.append((" ".join(name_words), token.strip()))
            name_words = []
        else:
            name_words.append(token)
    if name_words:
        print(f"  ! trailing text without a URL: {' '.join(name_words)!r}")
    return entries


def leaf_urls(item) -> set[str]:
    if isinstance(item, dict):
        urls = set()
        for value in item.values():
            urls.update(leaf_urls(value))
        return urls
    if isinstance(item, list):
        urls = set()
        for value in item:
            urls.update(leaf_urls(value))
        return urls
    return {item} if isinstance(item, str) else set()


def merge(entries: list[tuple[str, str]], section: str) -> int:
    try:
        data = json.loads(WEBSITES.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        print(
            f"Error: cannot read {WEBSITES.relative_to(ROOT)}: {error}"
        )
        return 1
    known = leaf_urls(data)
    group = data.setdefault(section, {}).setdefault("General", {})
    added, updated, skipped = [], [], []
    for name, url in entries:
        if url in known:
            skipped.append((name, url))
            continue
        if name in group:
            group[name] = url
            updated.append((name, url))
        else:
            group[name] = url
            added.append((name, url))
        known.add(url)
    try:
        WEBSITES.write_text(
            json.dumps(data, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
    except OSError as error:
        print(
            f"Error: cannot write {WEBSITES.relative_to(ROOT)}: {error}"
        )
        return 1
    for name, url in added:
        print(f"  + {name}: {url}")
    for name, url in updated:
        print(f"  ~ {name}: {url}")
    for name, url in skipped:
        print(f"  - {name}: {url} (already present)")
    print(
        f"Added {len(added)}, updated {len(updated)}, "
        f"skipped {len(skipped)} duplicate(s)."
    )
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Merge a pasted 'Institution Name    URL' list into "
            f"{WEBSITES.relative_to(ROOT)}."
        )
    )
    parser.add_argument(
        "paste",
        nargs="*",
        help="The pasted list (quote it as one argument); "
        "reads stdin when omitted.",
    )
    parser.add_argument(
        "--section",
        default=DEFAULT_SECTION,
        help=f"Top-level group to merge into (default: {DEFAULT_SECTION}).",
    )
    args = parser.parse_args(argv)

    if not args.paste:
        entries = parse_lines(sys.stdin.read())
    elif len(args.paste) == 1 and "\n" in args.paste[0]:
        entries = parse_lines(args.paste[0])
    else:
        entries = parse_tokens(args.paste)

    if not entries:
        print("No usable entries found.")
        return 1
    print(f"Merging {len(entries)} entr{'y' if len(entries) == 1 else 'ies'} "
          f"into section {args.section!r} of {WEBSITES.relative_to(ROOT)}:")
    return merge(entries, args.section)


if __name__ == "__main__":
    raise SystemExit(main())
