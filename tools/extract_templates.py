#!/usr/bin/env python3
"""Extract P[key]() template content uit index.html.

Output: tools/templates.json — { "home": "<html...>", "over": "<html...>", ... }

Genereert NIET de uiteindelijke pagina's; alleen de body-content per key.
build_pages.py gebruikt dit als input.
"""
from __future__ import annotations
import json
import re
from pathlib import Path

SRC = Path(__file__).parent.parent / "index.html"
OUT = Path(__file__).parent / "templates.json"


def extract_templates(text: str) -> dict[str, str]:
    """Parse "key": () => `...` blocks.

    P-object opent op `const P = {` (line ~724). Sluit op `};` (line ~2883).
    Elke entry: `"<key>": () => `<html>`,?  (mogelijk gevolgd door witregel).
    Template literals (backticks) kunnen newlines bevatten + ${expr} -- maar
    in deze codebase zijn er geen ${...} interpolaties in P[].
    """
    # Vind start van het P-object
    m = re.search(r"const P\s*=\s*\{", text)
    if not m:
        raise SystemExit("Could not find 'const P = {' in index.html")
    start = m.end()

    out: dict[str, str] = {}
    i = start
    # Loop totdat we eindigend `};` tegenkomen op col 0
    while True:
        # Skip whitespace + comma
        while i < len(text) and text[i] in " \t\n\r,":
            i += 1
        if i >= len(text):
            break
        # Stop bij eind van object
        if text[i] == "}":
            break
        # Verwacht "key":
        km = re.match(r'"([^"]+)"\s*:\s*\(\)\s*=>\s*`', text[i:])
        if not km:
            # Probeer single-line skip — maar geef foutmelding
            line_no = text[:i].count("\n") + 1
            raise SystemExit(f"Parse error around line {line_no}: {text[i:i+60]!r}")
        key = km.group(1)
        body_start = i + km.end()
        # Vind matching closing backtick (geen escaped ` in source, dus simpel)
        body_end = text.index("`", body_start)
        body = text[body_start:body_end]
        out[key] = body
        i = body_end + 1

    return out


def main() -> None:
    text = SRC.read_text(encoding="utf-8")
    templates = extract_templates(text)
    OUT.write_text(json.dumps(templates, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Extracted {len(templates)} templates -> {OUT}")
    for k in templates:
        size = len(templates[k])
        print(f"  {k:25s}  {size:>7d} chars")


if __name__ == "__main__":
    main()
