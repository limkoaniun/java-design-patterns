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
name: cheng-design-patterns-en
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

SKILL_ZH = SKILL_EN.replace("name: cheng-design-patterns-en", "name: cheng-design-patterns-zh") \
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
    en = tmp_path / "cheng-design-patterns-en"
    zh = tmp_path / "cheng-design-patterns-zh"
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
    _skill_pair(write, en, zh, zh_text=SKILL_ZH.replace("name: cheng-design-patterns-zh\n", ""))
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


def test_files_unknown_path_is_error(trees, heading_map):
    en, zh, write = trees
    _ok_pair(write, en, zh)
    errs = check_tree(en, zh, heading_map, files=["chapters/ch02-stratgy.md"])
    assert any("ch02-stratgy.md" in e and "not an en file" in e for e in errs)


def test_files_dot_slash_prefix_is_normalized(trees, heading_map):
    en, zh, write = trees
    _ok_pair(write, en, zh)
    assert check_tree(en, zh, heading_map, files=["./chapters/ch02-strategy.md"]) == []


def test_files_empty_list_is_error(trees, heading_map):
    en, zh, write = trees
    _ok_pair(write, en, zh)
    assert check_tree(en, zh, heading_map, files=[])
    r = subprocess.run([sys.executable, str(ROOT / "tools/check_parity.py"), str(en), str(zh), "--files"], capture_output=True, text=True)
    assert r.returncode == 1


def test_straight_quoted_tagged_quote_is_checked(trees, heading_map):
    en, zh, write = trees
    _ok_pair(write, en, zh)
    write(en, "chapters/ch02-strategy.md", EN_CH + '\nHe said "建立相应数目的原型"[DP] ok.\n')
    write(zh, "chapters/ch02-strategy.md", ZH_CH + '\n他说 "建立相应数目的原型"[DP] 好。\n')
    assert check_tree(en, zh, heading_map) == []
    write(zh, "chapters/ch02-strategy.md", ZH_CH + '\n他说 "建立若干原型"[DP] 好。\n')
    errs = check_tree(en, zh, heading_map)
    assert any("quote" in e and "建立相应数目的原型" in e for e in errs)


def test_topic_index_chapter_refs_must_match(trees, heading_map):
    en, zh, write = trees
    en_text = SKILL_EN.replace("- **Strategy** → ch02", "- **Strategy** → ch02, ch04")
    _skill_pair(write, en, zh, zh_text=en_text.replace("name: cheng-design-patterns-en", "name: cheng-design-patterns-zh")
                .replace("## Chapter Index", "## 章节索引").replace("## Topic Index", "## 主题索引").replace("→ ch02, ch04", "→ ch02"))
    write(en, "SKILL.md", en_text)
    errs = check_tree(en, zh, heading_map)
    assert any("topic index row 1" in e for e in errs)


def test_frontmatter_name_ok_when_run_from_dot(tmp_path, heading_map, monkeypatch):
    en = tmp_path / "cheng-design-patterns-en"
    zh = tmp_path / "cheng-design-patterns-zh"
    for d in (en, zh):
        (d / "chapters").mkdir(parents=True)
    (en / "SKILL.md").write_text(SKILL_EN, encoding="utf-8")
    (zh / "SKILL.md").write_text(SKILL_ZH, encoding="utf-8")
    (en / "chapters/ch02-strategy.md").write_text(EN_CH, encoding="utf-8")
    (zh / "chapters/ch02-strategy.md").write_text(ZH_CH, encoding="utf-8")
    (en / "chapters/ch04-open-closed.md").write_text("# x\n\n## Core Idea\ny\n", encoding="utf-8")
    (zh / "chapters/ch04-open-closed.md").write_text("# x\n\n## 核心思想\ny\n", encoding="utf-8")
    monkeypatch.chdir(en)
    assert check_tree(Path("."), zh, heading_map) == []
