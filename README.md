# cheng-design-patterns

Agent skill generated from *大话设计模式（Java溢彩加强版）* by 程杰 (Cheng Jie) with [book-to-skill](https://github.com/virgiliojr94/book-to-skill).

It packages the book's 23 GoF design patterns and six OO design principles as a queryable knowledge base: the author's exact Chinese definitions, pattern-selection rules, the 商场收银 refactoring ladder, similar-pattern disambiguation, and compact reconstructed Java listings for each chapter.

## Install

```bash
npx skills add https://github.com/limkoaniun/cheng-design-patterns --skill cheng-design-patterns
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

## Note on content

All files are synthesized summaries and reconstructions, not the book's text. Code listings were recovered by OCR from the PDF's embedded images and cleaned by hand; they are faithful in structure and naming but may differ from the printed listings in minor details. This repository is private because the source is a copyrighted work.
