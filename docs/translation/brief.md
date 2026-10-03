# Translator brief: java-design-patterns-en → java-design-patterns-zh

You translate exactly one file. Input: the en file at the path you were given. Output: the zh file at the same relative path under `java-design-patterns-zh/`. Do not touch any other file.

## Rules

1. Keep the file name. Keep every relative link target byte-identical, including `(chapters/ch15-abstract-factory.md)` and `(ch04-open-closed.md)`. Translate only the link text.
2. Translate `##` and `###` headings using `tools/heading_map.json`. A heading in that map must become exactly the mapped string. Headings not in the map (H1 title lines, the `### 策略 Strategy (ch02)` cards in patterns.md) are rendered as 中文（English）(chNN), keeping the `(chNN)` suffix. Keep heading levels unchanged.
2a. The H1 title line follows one fixed form. The en H1 is `# Chapter N: <Chinese segment> — <English gloss>`. The zh H1 is `# 第N章：<Chinese segment verbatim>（<English gloss verbatim>）`, with no space around N, full-width parentheses, no `(chNN)` suffix, and nothing else. Example: en `# Chapter 2: 商场促销——策略模式 — Store Promotions: Strategy` becomes `# 第2章：商场促销——策略模式（Store Promotions: Strategy）`. For a file whose en H1 is not a chapter title (SKILL.md, glossary.md, patterns.md, cheatsheet.md) translate the English words and keep the Chinese words verbatim.
3. Pattern and principle names: 中文（English）on first mention in the file, then 中文 alone. Use `docs/translation/terms.md` for every term.
4. Any text wrapped in curly quotes “…” that contains Chinese is an author quotation. Copy it byte-for-byte, including the tag that follows it (`[DP]`, `[DPE]`, `[ASD]`, `[J&DP]`) and the space or absence of space before the tag. Never retranslate, reflow, or re-punctuate a quotation. Bare tags in English prose (for example `eliminates conditionals in the client [DP]`) stay in the translated sentence in the same position.
5. Fenced code blocks (``` ... ```) are copied byte-for-byte, including the info string `java` and every comment. Do not translate comments. Do not change whitespace.
6. Tables keep the same number of rows and columns. Translate header cells and prose cells. Do not translate cells that are code, class names, or quotations. Keep the `|---|---|` row.
7. Inline code in backticks stays as-is.
8. Do not add, remove, or reorder sections, bullets, table rows, or sentences. The zh file is a translation, not a revision. If a sentence seems wrong, translate it faithfully anyway.
9. Register: 简体中文, technical, concise. Prefer the book's own vocabulary (the term table) over textbook variants.
9a. Quote marks are a fixed convention, not a preference. Curly “…” is reserved for author quotations (rule 4) and must never be introduced around anything else. Any other quoted phrase in the en file, whether the en used "…" or '…', and whether the phrase is English or Chinese, becomes 「…」 in zh. ASCII "…" survives only inside code spans and fenced code, or when it wraps a Chinese author quotation that the en file itself wrote in ASCII quotes (then it is copied byte-for-byte per rule 4).
9b. English parentheticals that merely gloss adjacent Chinese text (for example `拒绝不成熟的抽象 (reject premature abstraction)`) are dropped in zh, never translated back into a Chinese repeat. A parenthetical that adds information the Chinese does not carry (for example `(not by count)`) is translated as a parenthetical. Bold labels of the form `**中文 (English)**` become `**中文（English）**` with full-width parentheses, and the English is kept.
9c. Principle abbreviations SRP, OCP, DIP, LSP, LoD, CARP are never left bare in prose. First mention per file: 单一职责原则（SRP）, 开放-封闭原则（OCP）, 依赖倒转原则（DIP）, 里氏代换原则（LSP）, 迪米特法则（LoD）, 合成/聚合复用原则（CARP）; afterwards the full Chinese name alone. Inside tables and headings the abbreviation may stay if the en cell is only the abbreviation.
9d. The word "combined" or "+ X (combined)" in a label means the patterns are used together, rendered 结合 or 三者结合, never 组合 (which is the Composite pattern in this book).
9e. Chapter cross-references written as `ch01`, `ch15` in en prose stay as `ch01`, `ch15`; do not rewrite them as 第1章. Do not insert spaces between Chinese characters and the names 大鸟 / 小菜.
10. For `SKILL.md` only: the frontmatter `name` becomes `java-design-patterns-zh`. The `description` is written in Chinese, keeps the English pattern names in parentheses so mixed-language prompts trigger, and must be 1024 characters or fewer. The HTML comment `argument-hint` is translated. The Chapter Index and Topic Index keep the same rows in the same order with identical link targets; translate the title and framework cells.

## Self-check before you finish

Run from the repo root:

    python3 tools/check_parity.py java-design-patterns-en java-design-patterns-zh --files <your relative path>

It must print `✓ parity: 0 error(s)`. If it prints errors, fix your file and run again. Do not finish while it reports errors.
