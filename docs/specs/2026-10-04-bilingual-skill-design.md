# Bilingual skill repo: cheng-design-patterns

Date: 2026-10-04
Status: approved design, pending implementation plan

## Goal

Publish the `cheng-design-patterns` agent skill (generated from 大话设计模式（Java溢彩加强版）by 程杰 with book-to-skill) as a public GitHub repository containing two complete, parallel skills: one in Chinese, one in English. A user installs one skill and gets the whole knowledge base in that language.

## Decisions already made

| Decision | Choice |
|---|---|
| Layout | Two sibling skills in one repo, each self-contained with its own `SKILL.md` |
| English tree | Frozen. The current files become the en skill unchanged except for the frontmatter `name` |
| Verbatim author quotes and reconstructed code | Kept, with an attribution notice in both READMEs |
| Spec location | This file, in the new repo, not in book-to-skill |

## Repository layout

```
cheng-design-patterns/                  ~/Dev/projects/cheng-design-patterns
├── README.md                           中文, opens with "English · 中文" toggle line
├── README.en.md                        English, same toggle line
├── LICENSE                             covers the repo's own prose and scripts
├── docs/specs/…                        this spec and the implementation plan
├── tools/check_parity.py               stdlib-only parity checker
├── cheng-design-patterns-zh/
│   ├── SKILL.md                        name: cheng-design-patterns-zh
│   ├── chapters/ch00-oo-basics.md … ch29-pattern-summary.md
│   ├── glossary.md
│   ├── patterns.md
│   └── cheatsheet.md
└── cheng-design-patterns-en/
    ├── SKILL.md                        name: cheng-design-patterns-en
    ├── chapters/ch00-oo-basics.md … ch29-pattern-summary.md
    ├── glossary.md
    ├── patterns.md
    └── cheatsheet.md
```

Source of the en tree: `~/.agents/skills/cheng-design-patterns` (34 files, ~332 KB), currently untracked inside the private agent-skills repo.

Install commands advertised in the READMEs:

```bash
npx skills add https://github.com/limkoaniun/cheng-design-patterns --skill cheng-design-patterns-zh
npx skills add https://github.com/limkoaniun/cheng-design-patterns --skill cheng-design-patterns-en
```

Local install after publishing: `~/.claude/skills/cheng-design-patterns-zh` and `~/.claude/skills/cheng-design-patterns-en` are symlinks into the new repo. The old `~/.claude/skills/cheng-design-patterns` symlink and the untracked copy in `~/.agents/skills/` are removed.

## Translation rules for the zh tree

Every rule below is checked mechanically where possible (see Verification).

1. **File names, folder layout, relative links** are identical to the en tree. A link `[ch15](chapters/ch15-abstract-factory.md)` in en appears with the same target in zh.
2. **Section headings** map through a fixed table. Chapters:

   | en | zh |
   |---|---|
   | Core Idea | 核心思想 |
   | Frameworks Introduced | 引入的框架 |
   | Key Concepts | 关键概念 |
   | Mental Models | 心智模型 |
   | Anti-patterns | 反模式 |
   | Code Examples | 代码示例 |
   | Reference Tables | 参考表 |
   | Worked Example | 实战示例 |
   | Key Takeaways | 关键要点 |
   | Connects To | 关联章节 |

   `SKILL.md`, `glossary.md`, `patterns.md`, `cheatsheet.md` get their own heading tables, written into the plan before translation starts.
3. **Pattern and principle names** appear as 中文（English）on first mention in each file, then Chinese alone. The en tree does the reverse, so the pairing is symmetric.
4. **Author quotes** carrying a `[DP]`, `[DPE]`, `[ASD]` or `[J&DP]` tag are copied verbatim, tag included. They are already Chinese.
5. **Fenced code blocks** are byte-identical to the en tree, including the info string. Comments inside them are already Chinese.
6. **Tables** keep the same row and column count. Header cells and prose cells are translated; code and quoted cells are not.
7. **Terminology** comes from a term table derived from `glossary.md` before any translation starts. Every translator job receives it. Examples: 合成/聚合复用原则, 迪米特法则, 双重锁定, 浅复制/深复制, 透明方式/安全方式.
8. **Frontmatter**: `name: cheng-design-patterns-zh`; `description` is Chinese, keeps the English pattern names in it so mixed-language prompts still trigger, and stays within the 1024-character loader limit. The `argument-hint` comment is translated.
9. **Chapter and topic index tables in SKILL.md** keep the same rows in the same order with the same link targets.
10. Nothing is added that is not in the en file. The zh tree is a translation, not a revision.

## Production method

Parallel subagent translation, one job per file, 34 jobs. Each job receives the en file, the heading table for that file type, the term table, and rules 1–10. The job writes exactly one zh file. No job sees another job's output, so consistency is enforced by the shared tables and the checker, not by agents coordinating.

Alternatives considered and rejected for this task:

- A `--lang` flag in the book-to-skill generator. Produces a Chinese skill from the PDF, not a line-for-line parallel of the frozen English tree, and is a product feature with its own evidence gate. Possible later task.
- External machine translation. Needs an API key, and output still needs the same checking and review.

## Verification

`tools/check_parity.py en_dir zh_dir` exits non-zero if any of these hold:

- A file exists in one tree and not the other.
- After mapping through the heading table, the sequence of `##` and `###` headings differs.
- Fenced code blocks differ in count or in bytes.
- A relative link target does not exist.
- A tagged quote (`“…”[DP]` and the other three tags) present in en is absent from zh.
- Frontmatter `name` does not equal the folder name.
- Chapter and topic index tables in SKILL.md differ in row count or link targets.

Additional gates:

- `python3 ~/Dev/projects/book-to-skill/tools/validate_skill.py <skill>/SKILL.md` passes for both skills.
- Human-quality read of three full chapters: ch02 (strategy), ch15 (abstract factory, longest reflection section), ch29 (summary, densest cross-references).
- Live smoke test: with the zh skill installed, ask 什么是策略模式 and confirm the agent loads `cheng-design-patterns-zh/chapters/ch02-strategy.md` and answers in Chinese.

A task is not done while any gate is red.

## READMEs

Both READMEs contain, in this order: the toggle line, one-paragraph description, install commands for both skills, contents table, and a content notice. The notice states that all files are synthesized summaries and reconstructions rather than the book's text, that short quoted definitions are attributed to 程杰, that code listings were recovered by OCR from embedded images and cleaned by hand and may differ from the printed listings in minor details, and links to the book. The sentence "This repository is private because the source is a copyrighted work" is removed.

## Publishing

Done last, after every gate above is green:

1. Commit the full tree.
2. `gh repo create limkoaniun/cheng-design-patterns --public --source . --push`.
3. Replace the local symlinks as described in Repository layout.
4. Remove the untracked copy from `~/.agents/skills/`.

## Out of scope

- Any edit to English content beyond the frontmatter `name`.
- English glosses for Chinese quotes in the en tree.
- Changes to book-to-skill.
- Generator-level multilingual support.
