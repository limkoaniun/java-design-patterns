# Bilingual Skill Repo Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Turn the single English-scaffolded `java-design-patterns` skill into a public repo holding two parallel skills, `java-design-patterns-en` (frozen copy) and `java-design-patterns-zh` (full Chinese translation), verified by a parity checker.

**Architecture:** The en tree is copied verbatim and only its frontmatter `name` changes. The zh tree is produced one file at a time by independent translator jobs that all read the same brief, heading map, and term table. A stdlib-only checker compares the two trees structurally (files, headings, code blocks, links, quotes, frontmatter, index tables) and is the gate for every translation batch. Publishing happens last.

**Tech Stack:** Markdown, Python 3.14 stdlib for the checker, pytest (dev only) for checker tests, `gh` CLI for publishing, `tools/validate_skill.py` from book-to-skill as an external validator.

**Spec:** `docs/specs/2026-10-04-bilingual-skill-design.md`

## Global Constraints

- Repo root: `~/Dev/projects/java-design-patterns`. All relative paths below are from there.
- Source of the en tree: `~/.agents/skills/java-design-patterns` (34 markdown files: `SKILL.md`, `glossary.md`, `patterns.md`, `cheatsheet.md`, `chapters/ch00…ch29`). It is never edited.
- Skill folder names and frontmatter names: `java-design-patterns-zh`, `java-design-patterns-en`. They must match exactly.
- SKILL.md frontmatter `description` must be 1024 characters or fewer.
- No edit to en content beyond the frontmatter `name` line.
- zh tree: identical file names, identical relative links, byte-identical fenced code blocks, verbatim tagged quotes, headings via the heading map, terms via the term table.
- Checker is stdlib only. pytest is the only dev dependency.
- Commit after every task. Do not push until Task 8.
- Translator jobs never see each other's output. Consistency comes from the shared brief, heading map, and term table.

## Review Focus

Inputs the spec implies but no task's tests would otherwise exercise. Each has a test pinned to Task 2.

1. A zh file uses `~~~` fences or an indented code block instead of a backtick fence, so a code block silently disappears from the comparison. Expected: the checker counts fences by the same rule in both trees and reports the count mismatch.
2. A translated heading carries a trailing space or full-width colon variant (`## 核心思想：`), so exact-match fails on an invisible difference. Expected: headings are compared after `strip()`, and the error message prints both strings with `repr()`.
3. A link with an anchor fragment (`chapters/ch29-pattern-summary.md#judges`) is treated as a missing file. Expected: the fragment is dropped before the existence check.
4. A curly-quoted author sentence in en spans a line break inside a table cell or list item, so the regex misses it and the check passes vacuously. Expected: the quote regex uses `re.DOTALL` and the test includes a multi-line quote.
5. A zh file is present but empty or missing frontmatter, and the heading check passes because both sequences are empty for that file. Expected: a zh file with zero headings when en has any is an error; a SKILL.md without a `name:` line is an error.

---

### Task 1: Scaffold the repo with the frozen en tree

**Files:**
- Create: `java-design-patterns-en/` (copy of source, 34 files)
- Create: `.gitignore`
- Create: `LICENSE`
- Modify: `java-design-patterns-en/SKILL.md:2` (frontmatter `name`)

**Interfaces:**
- Consumes: nothing.
- Produces: `java-design-patterns-en/` as the fixed source for every later task.

- [ ] **Step 1: Copy the source tree**

```bash
cd ~/Dev/projects/java-design-patterns
cp -R ~/.agents/skills/java-design-patterns java-design-patterns-en
rm -f java-design-patterns-en/README.md java-design-patterns-en/.DS_Store
find java-design-patterns-en -name '*.md' | wc -l
```
Expected: `34`

- [ ] **Step 2: Change the frontmatter name**

```bash
sed -i '' '2s/^name: java-design-patterns$/name: java-design-patterns-en/' java-design-patterns-en/SKILL.md
sed -n '2p' java-design-patterns-en/SKILL.md
```
Expected: `name: java-design-patterns-en`

- [ ] **Step 3: Verify the copy differs from source only on that line**

```bash
diff -r ~/.agents/skills/java-design-patterns java-design-patterns-en
```
Expected: exactly two differing lines (the `name:` line) plus `Only in ~/.agents/...: README.md` and possibly `.DS_Store`. Nothing else.

- [ ] **Step 4: Validate the en SKILL.md**

```bash
python3 ~/Dev/projects/book-to-skill/tools/validate_skill.py java-design-patterns-en/SKILL.md
```
Expected: line starting with `✓` and exit code 0.

- [ ] **Step 5: Add .gitignore and LICENSE**

`.gitignore`:
```
.DS_Store
__pycache__/
.pytest_cache/
```

`LICENSE`: MIT, copyright 2026 Guanyu Lin, followed by this paragraph after the MIT text:

```
The book 大话设计模式 is © 程杰 and its publisher. This
repository contains synthesized summaries, reconstructed code listings, and
short attributed quotations for study purposes. It does not contain the
book's text. The MIT license above covers only this repository's own prose,
structure, and scripts.
```

(Assumption: MIT for the repo's own work. Change the license text here if you want something else; nothing else in the plan depends on it.)

- [ ] **Step 6: Commit**

```bash
git add .gitignore LICENSE java-design-patterns-en
git commit -m "feat: add frozen English skill tree as java-design-patterns-en"
```

---

### Task 2: Parity checker with tests

**Files:**
- Create: `tools/heading_map.json`
- Create: `tools/check_parity.py`
- Create: `tests/test_check_parity.py`
- Create: `tests/conftest.py`

**Interfaces:**
- Consumes: `java-design-patterns-en/` layout from Task 1.
- Produces:
  - CLI: `python3 tools/check_parity.py EN_DIR ZH_DIR [--files REL ...]`. Exit 0 when no errors, 1 otherwise. Prints one error per line as `path: message`.
  - `check_tree(en_dir: Path, zh_dir: Path, heading_map: dict[str, str], files: list[str] | None = None) -> list[str]`
  - `tools/heading_map.json`: a flat `{"English heading text": "中文标题"}` object. Used by Task 3's brief and by every translator job.

- [ ] **Step 1: Write the heading map**

`tools/heading_map.json`:
```json
{
  "Core Idea": "核心思想",
  "Frameworks Introduced": "引入的框架",
  "Key Concepts": "关键概念",
  "Mental Models": "心智模型",
  "Anti-patterns": "反模式",
  "Code Examples": "代码示例",
  "Reference Tables": "参考表",
  "Worked Example": "实战示例",
  "Key Takeaways": "关键要点",
  "Connects To": "关联章节",
  "How to Use This Skill": "使用方法",
  "Core Frameworks & Mental Models": "核心框架与心智模型",
  "The author's thesis": "作者的核心观点",
  "Six design principles (the judges of every pattern)": "六大设计原则（评判每个模式的标尺）",
  "Pattern selection: what varies decides the pattern": "模式选择：变化点决定模式",
  "The 商场收银 evolution ladder (the book's spine)": "商场收银演进阶梯（全书主线）",
  "Chapter Index": "章节索引",
  "Topic Index": "主题索引",
  "Supporting Files": "辅助文件",
  "Scope & Limits": "范围与限制",
  "Creational 创建型": "创建型 Creational",
  "Structural 结构型": "结构型 Structural",
  "Behavioral 行为型": "行为型 Behavioral",
  "Principles 原则": "原则 Principles",
  "Decision rules": "决策规则",
  "Similar patterns — pick by intent": "相似模式：按意图区分",
  "Smells → pattern": "坏味道 → 模式",
  "Thresholds & defaults the author commits to": "作者明确给出的阈值与默认做法",
  "The book's growth ladder (use as a \"how far to go\" gauge)": "全书的演进阶梯（衡量“该走多远”的标尺）",
  "The 23 patterns with the author's [DP] definitions": "23 个模式及作者引用的 [DP] 定义",
  "Contest results (the author's implicit ranking of \"most generally useful\")": "比赛结果（作者对“最通用模式”的隐含排名）",
  "Judges' pairwise contrasts": "评委的两两对比"
}
```

Headings not in this map (the H1 title lines, and the 23 `### 策略 Strategy (ch02)` cards in `patterns.md`) are compared by level only. Rule for translators: unmapped `###` cards in `patterns.md` become `### 策略模式（Strategy）(ch02)`, keeping the `(chNN)` suffix.

- [ ] **Step 2: Write conftest with a tree-builder fixture**

`tests/conftest.py`:
```python
import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))  # so `from tools.check_parity import ...` resolves


@pytest.fixture
def heading_map():
    return json.loads((ROOT / "tools" / "heading_map.json").read_text(encoding="utf-8"))


@pytest.fixture
def trees(tmp_path):
    """Return (en_dir, zh_dir, write) where write(tree, relpath, text) creates a file."""
    en = tmp_path / "en"
    zh = tmp_path / "zh"
    en.mkdir()
    zh.mkdir()

    def write(tree, relpath, text):
        p = tree / relpath
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text, encoding="utf-8")
        return p

    return en, zh, write
```

- [ ] **Step 3: Write the failing tests**

`tests/test_check_parity.py`:
```python
import subprocess
import sys
from pathlib import Path

from tools.check_parity import check_tree

ROOT = Path(__file__).resolve().parents[1]

EN_CH = """# Chapter 2

## Core Idea
Strategy encapsulates variation. “它定义了算法家族”[DP] and more [ASD].

## Code Examples
```java
class A {}
```
See [ch04](ch04-open-closed.md).
"""

ZH_CH = """# 第 2 章

## 核心思想
策略模式封装变化。“它定义了算法家族”[DP] 以及更多 [ASD]。

## 代码示例
```java
class A {}
```
见 [ch04](ch04-open-closed.md)。
"""


def _ok_pair(write, en, zh):
    write(en, "chapters/ch02-strategy.md", EN_CH)
    write(zh, "chapters/ch02-strategy.md", ZH_CH)
    write(en, "chapters/ch04-open-closed.md", "# x\n\n## Core Idea\ny\n")
    write(zh, "chapters/ch04-open-closed.md", "# x\n\n## 核心思想\ny\n")


def test_identical_structure_passes(trees, heading_map):
    en, zh, write = trees
    _ok_pair(write, en, zh)
    assert check_tree(en, zh, heading_map) == []


def test_missing_zh_file_is_error(trees, heading_map):
    en, zh, write = trees
    _ok_pair(write, en, zh)
    write(en, "chapters/ch05-dip.md", "# x\n\n## Core Idea\ny\n")
    errs = check_tree(en, zh, heading_map)
    assert any("ch05-dip.md" in e and "missing in zh" in e for e in errs)


def test_extra_zh_file_is_error(trees, heading_map):
    en, zh, write = trees
    _ok_pair(write, en, zh)
    write(zh, "chapters/extra.md", "# x\n")
    errs = check_tree(en, zh, heading_map)
    assert any("extra.md" in e and "not in en" in e for e in errs)


def test_heading_mismatch_is_error(trees, heading_map):
    en, zh, write = trees
    _ok_pair(write, en, zh)
    write(zh, "chapters/ch02-strategy.md", ZH_CH.replace("## 核心思想", "## 核心理念"))
    errs = check_tree(en, zh, heading_map)
    assert any("heading" in e and "核心理念" in e for e in errs)


def test_heading_trailing_space_and_fullwidth_colon(trees, heading_map):
    en, zh, write = trees
    _ok_pair(write, en, zh)
    # trailing space is tolerated, a full-width colon is not
    write(zh, "chapters/ch02-strategy.md", ZH_CH.replace("## 核心思想", "## 核心思想 "))
    assert check_tree(en, zh, heading_map) == []
    write(zh, "chapters/ch02-strategy.md", ZH_CH.replace("## 核心思想", "## 核心思想："))
    errs = check_tree(en, zh, heading_map)
    assert any("'核心思想：'" in e for e in errs)  # repr in message


def test_heading_level_sequence_checked_for_unmapped(trees, heading_map):
    en, zh, write = trees
    write(en, "patterns.md", "# P\n\n## Creational 创建型\n\n### 策略 Strategy (ch02)\nx\n")
    write(zh, "patterns.md", "# P\n\n## 创建型 Creational\n\n## 策略模式（Strategy）(ch02)\nx\n")
    errs = check_tree(en, zh, heading_map)
    assert any("patterns.md" in e and "heading" in e for e in errs)


def test_zh_file_with_no_headings_is_error(trees, heading_map):
    en, zh, write = trees
    _ok_pair(write, en, zh)
    write(zh, "chapters/ch02-strategy.md", "")
    errs = check_tree(en, zh, heading_map)
    assert any("ch02-strategy.md" in e and "heading" in e for e in errs)


def test_code_block_byte_difference_is_error(trees, heading_map):
    en, zh, write = trees
    _ok_pair(write, en, zh)
    write(zh, "chapters/ch02-strategy.md", ZH_CH.replace("class A {}", "class A { }"))
    errs = check_tree(en, zh, heading_map)
    assert any("code block" in e for e in errs)


def test_tilde_fence_counts_as_missing_block(trees, heading_map):
    en, zh, write = trees
    _ok_pair(write, en, zh)
    write(zh, "chapters/ch02-strategy.md", ZH_CH.replace("```java\nclass A {}\n```", "~~~java\nclass A {}\n~~~"))
    errs = check_tree(en, zh, heading_map)
    assert any("code block count" in e for e in errs)


def test_broken_link_is_error(trees, heading_map):
    en, zh, write = trees
    _ok_pair(write, en, zh)
    write(zh, "chapters/ch02-strategy.md", ZH_CH.replace("ch04-open-closed.md", "ch04-ocp.md"))
    errs = check_tree(en, zh, heading_map)
    assert any("link" in e and "ch04-ocp.md" in e for e in errs)


def test_link_with_anchor_resolves(trees, heading_map):
    en, zh, write = trees
    _ok_pair(write, en, zh)
    write(en, "chapters/ch02-strategy.md", EN_CH.replace("ch04-open-closed.md", "ch04-open-closed.md#x"))
    write(zh, "chapters/ch02-strategy.md", ZH_CH.replace("ch04-open-closed.md", "ch04-open-closed.md#x"))
    assert check_tree(en, zh, heading_map) == []


def test_missing_tagged_quote_is_error(trees, heading_map):
    en, zh, write = trees
    _ok_pair(write, en, zh)
    write(zh, "chapters/ch02-strategy.md", ZH_CH.replace("“它定义了算法家族”", "“它定义了算法族”"))
    errs = check_tree(en, zh, heading_map)
    assert any("quote" in e and "它定义了算法家族" in e for e in errs)


def test_multiline_quote_is_checked(trees, heading_map):
    en, zh, write = trees
    _ok_pair(write, en, zh)
    write(en, "chapters/ch02-strategy.md", EN_CH.replace("“它定义了算法家族”", "“它定义了\n算法家族”"))
    write(zh, "chapters/ch02-strategy.md", ZH_CH.replace("“它定义了算法家族”", "“它定义了算法家族”"))
    errs = check_tree(en, zh, heading_map)
    assert any("quote" in e for e in errs)


def test_tag_count_mismatch_is_error(trees, heading_map):
    en, zh, write = trees
    _ok_pair(write, en, zh)
    write(zh, "chapters/ch02-strategy.md", ZH_CH.replace(" [ASD]", ""))
    errs = check_tree(en, zh, heading_map)
    assert any("[ASD]" in e and "count" in e for e in errs)


SKILL_EN = """---
name: java-design-patterns-en
description: "x"
---

# T

## Chapter Index
| # | Title |
|---|---|
| [ch02](chapters/ch02-strategy.md) | a |
| [ch04](chapters/ch04-open-closed.md) | b |

## Topic Index
- **Strategy** → ch02
- **OCP** → ch04
"""

SKILL_ZH = SKILL_EN.replace("name: java-design-patterns-en", "name: java-design-patterns-zh") \
    .replace("## Chapter Index", "## 章节索引").replace("## Topic Index", "## 主题索引")


def _skill_pair(write, en, zh, zh_text=SKILL_ZH):
    _ok_pair(write, en, zh)
    write(en, "SKILL.md", SKILL_EN)
    write(zh, "SKILL.md", zh_text)


def test_frontmatter_name_must_match_folder(trees, heading_map):
    en, zh, write = trees
    _skill_pair(write, en, zh)
    errs = check_tree(en, zh, heading_map)
    # tmp dirs are named en/zh, not the skill names, so both files should error
    assert sum("frontmatter name" in e for e in errs) == 2


def test_frontmatter_name_ok_when_folder_matches(tmp_path, heading_map):
    en = tmp_path / "java-design-patterns-en"
    zh = tmp_path / "java-design-patterns-zh"
    for d in (en, zh):
        (d / "chapters").mkdir(parents=True)
    (en / "SKILL.md").write_text(SKILL_EN, encoding="utf-8")
    (zh / "SKILL.md").write_text(SKILL_ZH, encoding="utf-8")
    (en / "chapters/ch02-strategy.md").write_text(EN_CH, encoding="utf-8")
    (zh / "chapters/ch02-strategy.md").write_text(ZH_CH, encoding="utf-8")
    (en / "chapters/ch04-open-closed.md").write_text("# x\n\n## Core Idea\ny\n", encoding="utf-8")
    (zh / "chapters/ch04-open-closed.md").write_text("# x\n\n## 核心思想\ny\n", encoding="utf-8")
    assert check_tree(en, zh, heading_map) == []


def test_skill_missing_name_line_is_error(trees, heading_map):
    en, zh, write = trees
    _skill_pair(write, en, zh, zh_text=SKILL_ZH.replace("name: java-design-patterns-zh\n", ""))
    errs = check_tree(en, zh, heading_map)
    assert any("SKILL.md" in e and "name" in e for e in errs)


def test_description_over_1024_is_error(trees, heading_map):
    en, zh, write = trees
    _skill_pair(write, en, zh, zh_text=SKILL_ZH.replace('description: "x"', 'description: "' + "x" * 1025 + '"'))
    errs = check_tree(en, zh, heading_map)
    assert any("description" in e and "1024" in e for e in errs)


def test_index_link_sequence_must_match(trees, heading_map):
    en, zh, write = trees
    swapped = SKILL_ZH.replace("| [ch02](chapters/ch02-strategy.md) | a |\n| [ch04](chapters/ch04-open-closed.md) | b |",
                               "| [ch04](chapters/ch04-open-closed.md) | b |\n| [ch02](chapters/ch02-strategy.md) | a |")
    _skill_pair(write, en, zh, zh_text=swapped)
    errs = check_tree(en, zh, heading_map)
    assert any("index" in e and "link" in e for e in errs)


def test_topic_index_row_count_must_match(trees, heading_map):
    en, zh, write = trees
    _skill_pair(write, en, zh, zh_text=SKILL_ZH.replace("- **OCP** → ch04\n", ""))
    errs = check_tree(en, zh, heading_map)
    assert any("topic index" in e for e in errs)


def test_files_filter_limits_scope(trees, heading_map):
    en, zh, write = trees
    _ok_pair(write, en, zh)
    write(en, "chapters/ch05-dip.md", "# x\n\n## Core Idea\ny\n")  # missing in zh
    assert check_tree(en, zh, heading_map, files=["chapters/ch02-strategy.md"]) == []


def test_cli_exit_codes(trees):
    en, zh, write = trees
    _ok_pair(write, en, zh)
    r = subprocess.run([sys.executable, str(ROOT / "tools/check_parity.py"), str(en), str(zh)], capture_output=True, text=True)
    assert r.returncode == 0, r.stdout + r.stderr
    write(zh, "chapters/ch02-strategy.md", "")
    r = subprocess.run([sys.executable, str(ROOT / "tools/check_parity.py"), str(en), str(zh)], capture_output=True, text=True)
    assert r.returncode == 1
    assert "ch02-strategy.md" in r.stdout
```

- [ ] **Step 4: Run tests to verify they fail**

```bash
cd ~/Dev/projects/java-design-patterns && touch tools/__init__.py && python3 -m pytest -q tests/test_check_parity.py
```
Expected: collection error `ModuleNotFoundError: No module named 'tools.check_parity'`.

- [ ] **Step 5: Implement the checker**

`tools/check_parity.py`:
```python
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
```

- [ ] **Step 6: Run tests to verify they pass**

```bash
python3 -m pytest -q tests/test_check_parity.py
```
Expected: `22 passed`. If `test_heading_level_sequence_checked_for_unmapped` fails, note that `## 策略模式` vs `### 策略 Strategy` is a level difference and the error must mention `heading`.

- [ ] **Step 7: Run the checker against en vs en as a sanity baseline**

```bash
python3 tools/check_parity.py java-design-patterns-en java-design-patterns-en
```
Expected: `✗ parity: 302 error(s)`, and every error line is a heading-map error (`heading ... should be ...`). Confirm with `python3 tools/check_parity.py java-design-patterns-en java-design-patterns-en | grep -v 'heading ' | grep -vc parity` printing `0`. This proves that on real data the file, code-block, link, quote, tag, frontmatter and index checks are all clean, while the heading check correctly demands Chinese headings.

- [ ] **Step 8: Commit**

```bash
git add tools tests
git commit -m "feat: add stdlib parity checker for en/zh skill trees"
```

---

### Task 3: Translation kit (brief and term table)

**Files:**
- Create: `docs/translation/terms.md`
- Create: `docs/translation/brief.md`

**Interfaces:**
- Consumes: `tools/heading_map.json` (Task 2), `java-design-patterns-en/glossary.md` (Task 1).
- Produces: the two files every translator job in Tasks 4 and 5 reads verbatim.

- [ ] **Step 1: Extract the term pairs from the glossary**

```bash
cd ~/Dev/projects/java-design-patterns && mkdir -p docs/translation
{
  echo '# Term table (en → zh)'
  echo
  echo 'Derived from glossary.md. Use the zh form everywhere. First mention per file: 中文（English）.'
  echo
  echo '| English | 中文 |'
  echo '|---|---|'
  grep -o '^\*\*[^*]*\*\*' java-design-patterns-en/glossary.md | sed 's/\*\*//g' | awk -F' / ' 'NF==2 {printf "| %s | %s |\n", $1, $2}'
} > docs/translation/terms.md
grep -c '^| ' docs/translation/terms.md
```
Expected: a count of at least 60 rows. Open the file and confirm rows look like `| Strategy | 策略 |`.

- [ ] **Step 2: Append the fixed conventions block**

Append to `docs/translation/terms.md`:

```markdown

## Fixed renderings (not in glossary, or overriding it)

| English | 中文 |
|---|---|
| Strategy (pattern name in prose) | 策略模式 |
| Simple Factory | 简单工厂 |
| Factory Method | 工厂方法 |
| Abstract Factory | 抽象工厂 |
| Template Method | 模板方法 |
| Chain of Responsibility | 职责链 |
| Law of Demeter / LoD | 迪米特法则 |
| Composition over inheritance / CARP | 合成/聚合复用原则 |
| Open-Closed / OCP | 开放-封闭原则 |
| Dependency Inversion / DIP | 依赖倒转原则 |
| Liskov Substitution / LSP | 里氏代换原则 |
| Single Responsibility / SRP | 单一职责原则 |
| double-checked locking | 双重锁定 |
| shallow copy / deep copy | 浅复制 / 深复制 |
| transparent / safe form (Composite) | 透明方式 / 安全方式 |
| intrinsic / extrinsic state | 内部状态 / 外部状态 |
| client | 客户端 |
| Context | Context（上下文） |
| code smell | 坏味道 |
| refactoring | 重构 |
| loose coupling / tight coupling | 松耦合 / 紧耦合 |
| the author (程杰) | 作者 |
| 大鸟 / 小菜 | keep as-is |
| "worked example" | 实战示例 |
| mental model | 心智模型 |
| anti-pattern | 反模式 |
| takeaway | 要点 |

Pattern names in prose: 中文（English）on first mention in the file, 中文 alone afterwards. Example: 策略模式（Strategy）… 策略模式 …
Role names from UML (Context, Strategy, ConcreteStrategy, Creator, Product, Invoker, Receiver, Originator, Caretaker, Colleague) stay in English, in backticks when they name a class.
Tags `[DP]` `[DPE]` `[ASD]` `[J&DP]` stay exactly as written.
```

- [ ] **Step 3: Write the translator brief**

`docs/translation/brief.md`:

```markdown
# Translator brief: java-design-patterns-en → java-design-patterns-zh

You translate exactly one file. Input: the en file at the path you were given. Output: the zh file at the same relative path under `java-design-patterns-zh/`. Do not touch any other file.

## Rules

1. Keep the file name. Keep every relative link target byte-identical, including `(chapters/ch15-abstract-factory.md)` and `(ch04-open-closed.md)`. Translate only the link text.
2. Translate `##` and `###` headings using `tools/heading_map.json`. A heading in that map must become exactly the mapped string. Headings not in the map (H1 title lines, the `### 策略 Strategy (ch02)` cards in patterns.md) are rendered as 中文（English）(chNN), keeping the `(chNN)` suffix. Keep heading levels unchanged.
3. Pattern and principle names: 中文（English）on first mention in the file, then 中文 alone. Use `docs/translation/terms.md` for every term.
4. Any text wrapped in curly quotes “…” that contains Chinese is an author quotation. Copy it byte-for-byte, including the tag that follows it (`[DP]`, `[DPE]`, `[ASD]`, `[J&DP]`) and the space or absence of space before the tag. Never retranslate, reflow, or re-punctuate a quotation. Bare tags in English prose (for example `eliminates conditionals in the client [DP]`) stay in the translated sentence in the same position.
5. Fenced code blocks (``` ... ```) are copied byte-for-byte, including the info string `java` and every comment. Do not translate comments. Do not change whitespace.
6. Tables keep the same number of rows and columns. Translate header cells and prose cells. Do not translate cells that are code, class names, or quotations. Keep the `|---|---|` row.
7. Inline code in backticks stays as-is.
8. Do not add, remove, or reorder sections, bullets, table rows, or sentences. The zh file is a translation, not a revision. If a sentence seems wrong, translate it faithfully anyway.
9. Register: 简体中文, technical, concise. Prefer the book's own vocabulary (the term table) over textbook variants. Prefer 「」 only if the en file used plain double quotes "…" for a non-author phrase; keep curly “…” reserved for author quotations as described in rule 4.
10. For `SKILL.md` only: the frontmatter `name` becomes `java-design-patterns-zh`. The `description` is written in Chinese, keeps the English pattern names in parentheses so mixed-language prompts trigger, and must be 1024 characters or fewer. The HTML comment `argument-hint` is translated. The Chapter Index and Topic Index keep the same rows in the same order with identical link targets; translate the title and framework cells.

## Self-check before you finish

Run from the repo root:

    python3 tools/check_parity.py java-design-patterns-en java-design-patterns-zh --files <your relative path>

It must print `✓ parity: 0 error(s)`. If it prints errors, fix your file and run again. Do not finish while it reports errors.
```

- [ ] **Step 4: Commit**

```bash
git add docs/translation
git commit -m "docs: add translator brief and term table"
```

---

### Task 4: Translate the 30 chapters

**Files:**
- Create: `java-design-patterns-zh/chapters/ch00-oo-basics.md` … `ch29-pattern-summary.md` (30 files)

**Interfaces:**
- Consumes: `docs/translation/brief.md`, `docs/translation/terms.md`, `tools/heading_map.json`, `java-design-patterns-en/chapters/*.md`, `tools/check_parity.py --files`.
- Produces: 30 zh chapter files that pass the checker individually.

Run the jobs in three batches of ten so a systematic mistake in the brief is caught after the first batch, not after all thirty.

- [ ] **Step 1: Create the target directory**

```bash
mkdir -p ~/Dev/projects/java-design-patterns/java-design-patterns-zh/chapters
```

- [ ] **Step 2: Dispatch batch 1 (ch00–ch09), one job per file, in parallel**

Each job gets this prompt, with `<FILE>` substituted (for example `chapters/ch02-strategy.md`):

```
You are translating one file of an agent skill from English to Simplified Chinese.
Repo root: ~/Dev/projects/java-design-patterns
Read, in this order:
  1. docs/translation/brief.md   (the rules; follow every one)
  2. docs/translation/terms.md   (the term table; use it)
  3. tools/heading_map.json      (heading translations; exact strings)
  4. java-design-patterns-en/<FILE>   (your only source)
Write: java-design-patterns-zh/<FILE>
Then run: python3 tools/check_parity.py java-design-patterns-en java-design-patterns-zh --files <FILE>
Fix and re-run until it prints "✓ parity: 0 error(s)". Report the final checker output verbatim.
Do not edit any file other than java-design-patterns-zh/<FILE>.
```

- [ ] **Step 3: Verify batch 1 with the checker**

```bash
cd ~/Dev/projects/java-design-patterns
python3 tools/check_parity.py java-design-patterns-en java-design-patterns-zh --files $(cd java-design-patterns-en && ls chapters/ch0*.md)
```
Expected: `✓ parity: 0 error(s)`.

- [ ] **Step 4: Read one batch-1 file end to end (ch02-strategy.md) for brief compliance**

Check by eye: first mention is 策略模式（Strategy）; quotes untouched; headings exactly as mapped; code unchanged; no added or dropped bullets. If the brief produced a systematic problem (for example every job translated code comments), fix `docs/translation/brief.md`, commit the fix, and re-dispatch the affected files before continuing.

- [ ] **Step 5: Commit batch 1**

```bash
git add java-design-patterns-zh/chapters/ch0*.md
git commit -m "feat(zh): translate chapters ch00-ch09"
```

- [ ] **Step 6: Dispatch batch 2 (ch10–ch19) with the same prompt, verify, commit**

```bash
python3 tools/check_parity.py java-design-patterns-en java-design-patterns-zh --files $(cd java-design-patterns-en && ls chapters/ch1*.md)
git add java-design-patterns-zh/chapters/ch1*.md
git commit -m "feat(zh): translate chapters ch10-ch19"
```
Expected before commit: `✓ parity: 0 error(s)`.

- [ ] **Step 7: Dispatch batch 3 (ch20–ch29) with the same prompt, verify, commit**

```bash
python3 tools/check_parity.py java-design-patterns-en java-design-patterns-zh --files $(cd java-design-patterns-en && ls chapters/ch2*.md)
git add java-design-patterns-zh/chapters/ch2*.md
git commit -m "feat(zh): translate chapters ch20-ch29"
```
Expected before commit: `✓ parity: 0 error(s)`.

- [ ] **Step 8: Whole-chapters check**

```bash
python3 tools/check_parity.py java-design-patterns-en java-design-patterns-zh --files $(cd java-design-patterns-en && ls chapters/*.md)
ls java-design-patterns-zh/chapters | wc -l
```
Expected: `✓ parity: 0 error(s)` and `30`.

---

### Task 5: Translate the four root files

**Files:**
- Create: `java-design-patterns-zh/SKILL.md`
- Create: `java-design-patterns-zh/glossary.md`
- Create: `java-design-patterns-zh/patterns.md`
- Create: `java-design-patterns-zh/cheatsheet.md`

**Interfaces:**
- Consumes: same kit as Task 4; `tools/validate_skill.py` from book-to-skill.
- Produces: a complete zh skill that passes the full checker and the external validator.

- [ ] **Step 1: Dispatch four jobs in parallel with the Task 4 prompt**

`<FILE>` is `SKILL.md`, `glossary.md`, `patterns.md`, `cheatsheet.md`. Add this line to the SKILL.md job only:

```
Extra for SKILL.md: frontmatter name must be exactly `java-design-patterns-zh`; description in Chinese with English pattern names in parentheses, 1024 chars max; keep both index tables' rows, order and link targets identical; translate the "How to Use This Skill" bullets and the "Scope & Limits" and "Supporting Files" text; the source note paragraph at the end is translated too.
```

- [ ] **Step 2: Full-tree checker**

```bash
cd ~/Dev/projects/java-design-patterns
python3 tools/check_parity.py java-design-patterns-en java-design-patterns-zh
```
Expected: `✓ parity: 0 error(s)`. This run has no `--files`, so it also catches extra files in zh.

- [ ] **Step 3: External validator on both SKILL.md files**

```bash
python3 ~/Dev/projects/book-to-skill/tools/validate_skill.py java-design-patterns-en/SKILL.md
python3 ~/Dev/projects/book-to-skill/tools/validate_skill.py java-design-patterns-zh/SKILL.md
```
Expected: both print a `✓` line and exit 0.

- [ ] **Step 4: Description length and name, printed explicitly**

```bash
sed -n '2,3p' java-design-patterns-zh/SKILL.md | cut -c1-120
sed -n '3p' java-design-patterns-zh/SKILL.md | wc -c
```
Expected: `name: java-design-patterns-zh`; the count is 1024 or less.

- [ ] **Step 5: Commit**

```bash
git add java-design-patterns-zh
git commit -m "feat(zh): translate SKILL.md, glossary, patterns, cheatsheet"
```

---

### Task 6: Quality read and fixes

**Files:**
- Modify (only if a defect is found): `java-design-patterns-zh/chapters/ch02-strategy.md`, `ch15-abstract-factory.md`, `ch29-pattern-summary.md`, `SKILL.md`

**Interfaces:**
- Consumes: the complete zh tree.
- Produces: a signed-off zh tree; defects found are fixed in place and re-checked.

- [ ] **Step 1: Read the three chapters in full against their en source**

Read `java-design-patterns-zh/chapters/ch02-strategy.md`, `ch15-abstract-factory.md`, `ch29-pattern-summary.md` side by side with the en files. Record every defect in a scratch list with file, line, and the fix. Defect classes to look for: untranslated English sentence; translated code comment; term not from the term table; a sentence dropped or added; a pattern name without （English） on first mention; mistranslated table cell; broken Markdown (unbalanced `|`, lost bold).

- [ ] **Step 2: Read the zh SKILL.md in full**

Same defect classes, plus: the six-principles table renders; the pattern-selection bullets still read as rules; the description is Chinese with English names.

- [ ] **Step 3: Apply the fixes and re-run the gates**

```bash
python3 tools/check_parity.py java-design-patterns-en java-design-patterns-zh
python3 ~/Dev/projects/book-to-skill/tools/validate_skill.py java-design-patterns-zh/SKILL.md
```
Expected: `✓ parity: 0 error(s)` and `✓`.

- [ ] **Step 4: If any defect class appeared in all three chapters, sweep the other 27**

For a systematic defect (same mistake in three of three), grep for it across `java-design-patterns-zh/chapters/` and fix every occurrence. Example for untranslated headings that slipped the map:

```bash
grep -n '^## [A-Za-z]' java-design-patterns-zh/chapters/*.md
```
Expected after fixes: no output. Re-run the checker.

- [ ] **Step 5: Commit**

```bash
git add java-design-patterns-zh
git commit -m "fix(zh): quality-read corrections"
```

---

### Task 7: READMEs

**Files:**
- Create: `README.md` (中文)
- Create: `README.zh.md` (English)

**Interfaces:**
- Consumes: skill folder names from Task 1 and Task 5.
- Produces: the two files a visitor reads on GitHub.

- [ ] **Step 1: Write README.md (中文)**

```markdown
[English](README.zh.md) · 中文

# java-design-patterns

从程杰《大话设计模式》生成的 Agent Skill，使用 [book-to-skill](https://github.com/virgiliojr94/book-to-skill) 构建。中英文两个版本并行维护，结构逐文件对应。

它把书中的 23 个 GoF 设计模式和六大面向对象设计原则整理成可查询的知识库：作者的原文定义、模式选择规则、商场收银重构阶梯、相似模式辨析，以及每章紧凑的 Java 代码重构。

## 安装

中文版：

```bash
npx skills add https://github.com/limkoaniun/java-design-patterns --skill java-design-patterns-zh
```

英文版：

```bash
npx skills add https://github.com/limkoaniun/java-design-patterns --skill java-design-patterns-en
```

Claude Code 用户也可以把对应文件夹软链接到 `~/.claude/skills/`。

## 内容

| 文件 | 用途 |
|---|---|
| `SKILL.md` | 常驻入口：原则表、模式选择规则、章节与主题索引 |
| `chapters/ch00–ch29` | 每章一个文件：框架、关键概念、反模式、代码示例、实战示例、要点 |
| `glossary.md` | 中英术语表，附章节引用 |
| `patterns.md` | 23 个模式卡片：何时用 / 怎么用 / 取舍 |
| `cheatsheet.md` | 决策规则、易混模式对照表、坏味道 → 模式 |

两个版本目录结构相同。`tools/check_parity.py` 会校验文件、标题、代码块、链接与引文在两个版本间一致。

## 关于内容

本仓库的所有文件都是归纳整理与重构，不是原书文本。书中的模式定义以短引文形式出现并注明出处（程杰）。代码清单由 PDF 内嵌图片经 OCR 恢复并手工整理，结构与命名忠实于原书，细节可能略有出入。请购买原书以获取完整内容。
```

- [ ] **Step 2: Write README.zh.md**

```markdown
English · [中文](README.md)

# java-design-patterns

Agent skill generated from *大话设计模式* by 程杰 (Cheng Jie) with [book-to-skill](https://github.com/virgiliojr94/book-to-skill). Maintained in two parallel versions, Chinese and English, with a file-for-file matching structure.

It packages the book's 23 GoF design patterns and six OO design principles as a queryable knowledge base: the author's definitions, pattern-selection rules, the 商场收银 refactoring ladder, similar-pattern disambiguation, and compact reconstructed Java listings for each chapter.

## Install

Chinese version:

```bash
npx skills add https://github.com/limkoaniun/java-design-patterns --skill java-design-patterns-zh
```

English version:

```bash
npx skills add https://github.com/limkoaniun/java-design-patterns --skill java-design-patterns-en
```

Claude Code users can instead symlink the folder into `~/.claude/skills/`.

## Contents

| File | Purpose |
|---|---|
| `SKILL.md` | Always-loaded entry point: principles table, pattern-selection rules, chapter and topic indexes |
| `chapters/ch00–ch29` | One file per chapter: frameworks, key concepts, anti-patterns, code example, worked example, takeaways |
| `glossary.md` | Key terms, 中/英, with chapter references |
| `patterns.md` | 23 pattern cards: when to use / how / trade-offs |
| `cheatsheet.md` | Decision rules, confusable-pattern table, code smells → pattern |

Both versions share one directory layout. `tools/check_parity.py` verifies that files, headings, code blocks, links, and quotations match between them.

## Note on content

All files are synthesized summaries and reconstructions, not the book's text. Pattern definitions appear as short quotations attributed to 程杰. Code listings were recovered by OCR from the PDF's embedded images and cleaned by hand; they are faithful in structure and naming but may differ from the printed listings in minor details. Please buy the book for the full material.
```

- [ ] **Step 3: Check the toggle lines and links**

```bash
head -1 README.md README.zh.md
grep -o '(README[^)]*)' README.md README.zh.md
```
Expected: `[English](README.zh.md) · 中文` and `English · [中文](README.md)`; link targets `README.zh.md` and `README.md` both exist.

- [ ] **Step 4: Commit**

```bash
git add README.md README.zh.md
git commit -m "docs: bilingual READMEs with language toggle"
```

---

### Task 8: Publish and switch local install

**Files:**
- Remote: `github.com/limkoaniun/java-design-patterns` (new, public)
- Modify: `~/.claude/skills/` symlinks
- Delete: `~/.agents/skills/java-design-patterns` (untracked copy), `~/.claude/skills/java-design-patterns` (old symlink)

**Interfaces:**
- Consumes: the fully green repo from Tasks 1–7.
- Produces: a public repo and a working local install of both skills.

- [ ] **Step 1: Final gates, all three, with output captured**

```bash
cd ~/Dev/projects/java-design-patterns
python3 -m venv .venv && .venv/bin/pip -q install pytest && .venv/bin/python -m pytest -q
python3 tools/check_parity.py java-design-patterns-en java-design-patterns-zh
python3 ~/Dev/projects/book-to-skill/tools/validate_skill.py java-design-patterns-en/SKILL.md
python3 ~/Dev/projects/book-to-skill/tools/validate_skill.py java-design-patterns-zh/SKILL.md
git status --short
```
Expected: `28 passed`, `✓ parity: 0 error(s)`, two `✓` validator lines, empty status. Stop here if anything is red.

- [ ] **Step 1b: Fast-forward main to the branch so the published default branch carries the work**

```bash
git checkout main && git merge --ff-only bilingual && git log --oneline -1 && git branch --show-current
```
Expected: the merge fast-forwards (main was never advanced independently), the latest commit matches the branch head, and the current branch is `main`. `gh repo create --push` pushes the current branch, so this step must precede Step 2.

- [ ] **Step 2: Create the public repo and push**

```bash
gh repo create limkoaniun/java-design-patterns --public --source . --remote origin --push \
  --description "大话设计模式 as a bilingual (中文/English) agent skill: 23 GoF patterns and 6 OO principles"
gh repo view limkoaniun/java-design-patterns --json url,visibility
```
Expected: JSON with `"visibility": "PUBLIC"` and the repo URL.

- [ ] **Step 3: Switch the local install to the new repo**

```bash
rm ~/.claude/skills/java-design-patterns
ln -s ~/Dev/projects/java-design-patterns/java-design-patterns-zh ~/.claude/skills/java-design-patterns-zh
ln -s ~/Dev/projects/java-design-patterns/java-design-patterns-en ~/.claude/skills/java-design-patterns-en
ls -l ~/.claude/skills | grep cheng
```
Expected: two symlinks, no `java-design-patterns` entry.

- [ ] **Step 4: Remove the untracked copy from the private agent-skills repo**

```bash
git -C ~/.agents status --short skills/java-design-patterns
rm -rf ~/.agents/skills/java-design-patterns
git -C ~/.agents status --short | grep cheng || echo "clean"
```
Expected: first command shows `?? skills/java-design-patterns/` (confirming it was never committed), last prints `clean`.

- [ ] **Step 5: Live smoke test of the zh skill**

In a fresh Claude Code session in any directory, ask:

```
什么是策略模式？
```
Expected: the session invokes `java-design-patterns-zh`, reads `java-design-patterns-zh/chapters/ch02-strategy.md` (visible in the tool call), and answers in Chinese with the 商场收银 example and the `[DP]` definition. Record the session's answer summary as evidence in the final report.

- [ ] **Step 6: Verify the GitHub rendering**

Open `https://github.com/limkoaniun/java-design-patterns` and `…/blob/main/README.zh.md`. Expected: the toggle line is the first line on both pages and each link switches language.
