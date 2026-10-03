# Translator brief: cheng-design-patterns-en → cheng-design-patterns-zh

You translate exactly one file. Input: the en file at the path you were given. Output: the zh file at the same relative path under `cheng-design-patterns-zh/`. Do not touch any other file.

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
9. Register: 简体中文, technical, concise. Prefer the book's own vocabulary (the term table) over textbook variants. Prefer 「」 only if the en file used plain double quotes "…" for a non-author phrase; keep curly “…” reserved for author quotations as described in rule 4.
10. For `SKILL.md` only: the frontmatter `name` becomes `cheng-design-patterns-zh`. The `description` is written in Chinese, keeps the English pattern names in parentheses so mixed-language prompts trigger, and must be 1024 characters or fewer. The HTML comment `argument-hint` is translated. The Chapter Index and Topic Index keep the same rows in the same order with identical link targets; translate the title and framework cells.

## Self-check before you finish

Run from the repo root:

    python3 tools/check_parity.py cheng-design-patterns-en cheng-design-patterns-zh --files <your relative path>

It must print `✓ parity: 0 error(s)`. If it prints errors, fix your file and run again. Do not finish while it reports errors.
