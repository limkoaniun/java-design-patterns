English · [中文](README.zh.md)

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
| `patterns.md` | 24 pattern cards (GoF 23 + 简单工厂): when to use / how / trade-offs |
| `cheatsheet.md` | Decision rules, confusable-pattern table, code smells → pattern |

Both versions share one directory layout. `tools/check_parity.py` verifies that files, headings, code blocks, links, and quotations match between them. Run its tests with `python3 -m pytest -q` (pytest required).

## Note on content

All files are synthesized summaries and reconstructions, not the book's text. Pattern definitions appear as short quotations from the book, carrying the book's own citation tags ([DP], [DPE], [ASD], [J&DP]). Code listings were recovered by OCR from the PDF's embedded images and cleaned by hand; they are faithful in structure and naming but may differ from the printed listings in minor details. For the full material, buy the book: [大话设计模式](https://book.douban.com/subject/36116620/) by 程杰, Tsinghua University Press, ISBN 978-7-302-61553-8.
