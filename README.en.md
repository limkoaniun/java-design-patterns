English · [中文](README.md)

# cheng-design-patterns

Agent skill generated from *大话设计模式（Java溢彩加强版）* by 程杰 (Cheng Jie) with [book-to-skill](https://github.com/virgiliojr94/book-to-skill). Maintained in two parallel versions, Chinese and English, with a file-for-file matching structure.

It packages the book's 23 GoF design patterns and six OO design principles as a queryable knowledge base: the author's definitions, pattern-selection rules, the 商场收银 refactoring ladder, similar-pattern disambiguation, and compact reconstructed Java listings for each chapter.

## Install

Chinese version:

```bash
npx skills add https://github.com/limkoaniun/cheng-design-patterns --skill cheng-design-patterns-zh
```

English version:

```bash
npx skills add https://github.com/limkoaniun/cheng-design-patterns --skill cheng-design-patterns-en
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
