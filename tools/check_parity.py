#!/usr/bin/env python3
"""Structural parity check between the en and zh skill trees. Stdlib only.

Usage: check_parity.py EN_DIR ZH_DIR [--files REL ...]
Exit 0 when no errors, 1 otherwise. One error per line: "path: message".
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
TAGS = ("[DP]", "[DPE]", "[ASD]", "[J&DP]")
HEADING_RE = re.compile(r"^(#{1,6})\s+(.*?)\s*$")
FENCE_RE = re.compile(r"^```.*$")
LINK_RE = re.compile(r"\]\(([^)\s]+?\.md)(?:#[^)]*)?\)")
QUOTE_RE = re.compile(r"“[^”]*”", re.DOTALL)
CJK_RE = re.compile(r"[一-鿿]")
MAX_DESC = 1024


def load_heading_map(path: Path = HERE / "heading_map.json") -> dict[str, str]:
    return json.loads(path.read_text(encoding="utf-8"))


def _md_files(root: Path) -> list[str]:
    return sorted(p.relative_to(root).as_posix() for p in root.rglob("*.md"))


def _headings(text: str) -> list[tuple[int, str]]:
    out, in_fence = [], False
    for line in text.splitlines():
        if FENCE_RE.match(line):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        m = HEADING_RE.match(line)
        if m:
            out.append((len(m.group(1)), m.group(2).strip()))
    return out


def _code_blocks(text: str) -> list[str]:
    blocks, cur, in_fence = [], [], False
    for line in text.splitlines():
        if FENCE_RE.match(line):
            cur.append(line)
            if in_fence:
                blocks.append("\n".join(cur))
                cur = []
            in_fence = not in_fence
            continue
        if in_fence:
            cur.append(line)
    return blocks


def _frontmatter(text: str) -> dict[str, str] | None:
    if not text.startswith("---\n"):
        return None
    end = text.find("\n---", 4)
    if end < 0:
        return None
    fm: dict[str, str] = {}
    for line in text[4:end].splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            fm[k.strip()] = v.strip().strip('"')
    return fm


def _index_links(text: str) -> list[str]:
    return re.findall(r"\]\((chapters/[^)#]+\.md)", text)


def _topic_rows(text: str, headings: tuple[str, ...]) -> int:
    lines, inside, n = text.splitlines(), False, 0
    for line in lines:
        m = HEADING_RE.match(line)
        if m:
            inside = m.group(2).strip() in headings
            continue
        if inside and line.startswith("- **"):
            n += 1
    return n


def check_file(rel: str, en_text: str, zh_text: str, heading_map: dict[str, str]) -> list[str]:
    errs: list[str] = []
    en_h, zh_h = _headings(en_text), _headings(zh_text)
    if en_h and not zh_h:
        errs.append(f"{rel}: zh has no headings (en has {len(en_h)})")
    elif len(en_h) != len(zh_h):
        errs.append(f"{rel}: heading count en={len(en_h)} zh={len(zh_h)}")
    else:
        for (el, et), (zl, zt) in zip(en_h, zh_h):
            if el != zl:
                errs.append(f"{rel}: heading level {el}!={zl} at {et!r} / {zt!r}")
            elif et in heading_map and zt != heading_map[et]:
                errs.append(f"{rel}: heading {et!r} should be {heading_map[et]!r}, zh has {zt!r}")

    en_c, zh_c = _code_blocks(en_text), _code_blocks(zh_text)
    if len(en_c) != len(zh_c):
        errs.append(f"{rel}: code block count en={len(en_c)} zh={len(zh_c)}")
    else:
        for i, (a, b) in enumerate(zip(en_c, zh_c)):
            if a != b:
                errs.append(f"{rel}: code block #{i + 1} differs")

    for q in QUOTE_RE.findall(en_text):
        if CJK_RE.search(q) and q not in zh_text:
            errs.append(f"{rel}: quote missing in zh: {q[:40]}")
    en_tags, zh_tags = Counter(), Counter()
    for t in TAGS:
        en_tags[t], zh_tags[t] = en_text.count(t), zh_text.count(t)
        if en_tags[t] != zh_tags[t]:
            errs.append(f"{rel}: tag {t} count en={en_tags[t]} zh={zh_tags[t]}")
    return errs


def check_links(root: Path, rel: str, text: str) -> list[str]:
    errs = []
    base = (root / rel).parent
    for target in LINK_RE.findall(text):
        if not (base / target).exists():
            errs.append(f"{rel}: link target does not exist: {target}")
    return errs


def check_skill(root: Path, rel: str, text: str) -> list[str]:
    errs = []
    fm = _frontmatter(text)
    if fm is None or "name" not in fm:
        errs.append(f"{rel}: SKILL.md has no frontmatter name")
        return errs
    if fm["name"] != root.name:
        errs.append(f"{rel}: frontmatter name {fm['name']!r} != folder {root.name!r}")
    if len(fm.get("description", "")) > MAX_DESC:
        errs.append(f"{rel}: description is {len(fm['description'])} chars, limit {MAX_DESC}")
    return errs


def check_tree(en_dir: Path, zh_dir: Path, heading_map: dict[str, str], files: list[str] | None = None) -> list[str]:
    en_dir, zh_dir = Path(en_dir), Path(zh_dir)
    errs: list[str] = []
    en_files, zh_files = _md_files(en_dir), _md_files(zh_dir)
    if files is None:
        for f in sorted(set(zh_files) - set(en_files)):
            errs.append(f"{f}: present in zh, not in en")
        wanted = en_files
    else:
        wanted = [f for f in en_files if f in set(files)]
    for rel in wanted:
        zh_path = zh_dir / rel
        if not zh_path.exists():
            errs.append(f"{rel}: missing in zh")
            continue
        en_text = (en_dir / rel).read_text(encoding="utf-8")
        zh_text = zh_path.read_text(encoding="utf-8")
        errs += check_file(rel, en_text, zh_text, heading_map)
        errs += check_links(zh_dir, rel, zh_text)
        if rel == "SKILL.md":
            errs += check_skill(en_dir, rel, en_text)
            errs += check_skill(zh_dir, rel, zh_text)
            if _index_links(en_text) != _index_links(zh_text):
                errs.append(f"{rel}: index link sequence differs between en and zh")
            en_rows = _topic_rows(en_text, ("Topic Index",))
            zh_rows = _topic_rows(zh_text, ("Topic Index", heading_map.get("Topic Index", "Topic Index")))
            if en_rows != zh_rows:
                errs.append(f"{rel}: topic index rows en={en_rows} zh={zh_rows}")
    return errs


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("en_dir", type=Path)
    ap.add_argument("zh_dir", type=Path)
    ap.add_argument("--files", nargs="*", default=None, help="relative paths to check (default: all en files)")
    args = ap.parse_args(argv)
    errs = check_tree(args.en_dir, args.zh_dir, load_heading_map(), args.files)
    for e in errs:
        print(e)
    print(f"{'✗' if errs else '✓'} parity: {len(errs)} error(s)")
    return 1 if errs else 0


if __name__ == "__main__":
    sys.exit(main())
