[English](README.en.md) · 中文

# cheng-design-patterns

从程杰《大话设计模式（Java溢彩加强版）》生成的 Agent Skill，使用 [book-to-skill](https://github.com/virgiliojr94/book-to-skill) 构建。中英文两个版本并行维护，结构逐文件对应。

它把书中的 23 个 GoF 设计模式和六大面向对象设计原则整理成可查询的知识库：作者的原文定义、模式选择规则、商场收银重构阶梯、相似模式辨析，以及每章紧凑的 Java 代码重构。

## 安装

中文版：

```bash
npx skills add https://github.com/limkoaniun/cheng-design-patterns --skill cheng-design-patterns-zh
```

英文版：

```bash
npx skills add https://github.com/limkoaniun/cheng-design-patterns --skill cheng-design-patterns-en
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
