---
name: cheng-design-patterns-en
description: "Knowledge base from \"大话设计模式（Java溢彩加强版）\" by 程杰 (Cheng Jie). Use when applying the 23 GoF design patterns (策略/工厂/装饰/观察者/状态 etc.) or the six OO design principles (单一职责, 开放-封闭, 依赖倒转, 里氏代换, 迪米特, 合成/聚合复用) while designing or refactoring Java/OO code, choosing between similar patterns, studying the book, or referencing its chapters."
---

<!-- argument-hint: [pattern name (中/英), principle, chapter number, or design question] -->

# 大话设计模式（Java溢彩加强版）
**Author**: 程杰 (Cheng Jie) | **Pages**: ~500 | **Chapters**: 30 (楔子 ch00 + ch01–ch29) | **Generated**: 2026-09-30

## How to Use This Skill

- **Without arguments** — load the principles and pattern-selection rules below
- **With a topic** — ask about `策略模式`, `strategy`, `double-checked locking`, `商场收银`; I find and read the relevant chapter
- **With chapter** — ask for `ch14`; I load that specific chapter
- **Browse** — ask "what chapters do you have?" to see the full index

When you ask about a topic not covered in Core Frameworks below, I will read
the relevant chapter file before answering. Pattern names are indexed in both
Chinese and English.

---

## Core Frameworks & Mental Models

### The author's thesis
Design patterns are "面向对象编程思维的体操". You learn all 23 not to use all 23, but to acquire three reflexes: **封装变化** (encapsulate what varies), **对象间松散耦合** (loose coupling), **针对接口编程** (program to an interface). The goal of every refactoring in the book is code that is 可维护、可扩展、可复用、灵活性好.

**Four stages of mastery (设计模式四境界)**: (1) don't know patterns, write bad code → (2) know a few, over-apply them → (3) know all, confused by similarity, hesitant → (4) apply freely, "无剑胜有剑". Over-design is a temporary symptom of stage 2; not using patterns for fear of over-design is 因噎废食.

### Six design principles (the judges of every pattern)
| Principle | Author's formulation | Apply when |
|---|---|---|
| **单一职责原则 (SRP)** | 就一个类而言，应该仅有一个引起它变化的原因 | A class has two reasons to change → split (手机 vs 电子阅读器; 俄罗斯方块 logic vs display) |
| **开放-封闭原则 (OCP)** | 软件实体（类、模块、函数等）应该可以扩展，但是不可修改 [ASD] | Extend by adding classes, not editing working ones. Abstract only where change actually appears; "拒绝不成熟的抽象和抽象本身一样重要" |
| **依赖倒转原则 (DIP)** | 抽象不应该依赖细节，细节应该依赖于抽象 — 针对接口编程，不要对实现编程 | High-level modules should depend on interfaces (电脑 modules plug into the motherboard; 收音机 is soldered) |
| **里氏代换原则 (LSP)** | 子类型必须能够替换掉它们的父类型 [ASD] | Any place a base type is used must work unchanged with any subtype; this is what makes DIP and OCP possible |
| **迪米特法则 (LoD / 最少知识原则)** | 如果两个类不必彼此直接通信，那么这两个类就不应当发生直接的相互作用；可以通过第三者转发这个调用 [J&DP] | Route calls through a mediator/manager; minimize member visibility (第一天上班 should call HR, not hunt for someone in IT) |
| **合成/聚合复用原则 (CARP)** | 尽量使用合成/聚合，尽量不要使用类继承 [J&DP] | Inheritance leaks parent details and explodes subclasses under two axes of change; use object composition (手机品牌 × 手机软件) |

### Pattern selection: what varies decides the pattern
- **A family of interchangeable algorithms** (discount rules) → **策略 Strategy**; combine with 简单工厂 so the client never sees concrete strategies. 策略 vs 状态: same structure; 策略 is chosen by the client, 状态 switches itself as conditions change.
- **Which concrete class to create** → start with **工厂方法 Factory Method** ("通常设计应该是从工厂方法开始"). 简单工厂 centralizes the `switch` and violates OCP; 工厂方法 pushes creation to subclasses; **抽象工厂 Abstract Factory** when you create *families* of related products (all DAOs for SQL Server vs Oracle). Collapse the class explosion with 简单工厂 + 反射 + configuration file.
- **Add responsibilities to an object at runtime, in any order** → **装饰 Decorator** (穿衣 order matters). Prefer it over subclass explosion when behaviours combine.
- **Control access to an object** (lazy load, remote, permission, smart reference) → **代理 Proxy**; 代理 wraps one object with the same interface, 装饰 adds behaviour, 适配器 changes the interface.
- **Make an existing incompatible interface fit** → **适配器 Adapter** — only after the fact, for legacy or third-party code; never design new code to need it.
- **A subsystem is hard to use; layering** → **外观 Facade** (基金 hides 股票/国债/房产). Facade is one-way simplification; **中介者 Mediator** manages many-to-many peer interaction (安理会).
- **Same algorithm skeleton, varying steps** → **模板方法 Template Method** (试卷 with answers that vary). Inheritance-based; prefer 策略 if the whole algorithm varies.
- **One-to-many change notification, sender should not know receivers** → **观察者 Observer**; declare the abstract observer as an *interface* so unrelated classes can subscribe, and type the subject as an interface (not `Boss`). `java.util.Observable` works but is deprecated and blocks other inheritance.
- **Behaviour depends on state with long `if/else` chains on a state field** → **状态 State**; each state decides the next transition ("方法过长是坏味道").
- **Part-whole tree where leaf and composite are used uniformly** → **组合 Composite** (分公司 = 部门). 透明方式 (leaf implements add/remove) vs 安全方式.
- **Requests as objects** (undo, queue, log, decouple invoker from receiver) → **命令 Command**; **职责链 Chain of Responsibility** when the handler is decided at runtime by passing along a chain (加薪 escalation); **备忘录 Memento** when you must snapshot and restore state without exposing internals.
- **Two independent dimensions of variation** → **桥接 Bridge** (abstraction × implementation, both via composition). 桥接 separates dimensions up-front; 装饰 stacks behaviour on one dimension.
- **Many fine-grained objects with shared intrinsic state** → **享元 Flyweight**; split 内部状态 (shared) from 外部状态 (passed in).
- **One object, globally accessed** → **单例 Singleton**; in Java prefer 静态初始化 (饿汉) or 双重锁定 with `volatile`.
- **Object copies with different data** → **原型 Prototype** via `Cloneable`; know 浅复制 vs 深复制 (a `WorkExperience` field is shared unless you clone it too).
- **Complex object built step by step, same process different representations** → **建造者 Builder** (小人 must have head, body, arms, legs; the Director enforces the order).
- **Traverse a collection without exposing its structure** → **迭代器 Iterator** (already in `java.util.Iterator`; learn the structure, use the library).
- **A stable, simple grammar interpreted repeatedly** → **解释器 Interpreter** (音乐解释器); **访问者 Visitor** when the data structure is fixed (男人/女人) and operations keep growing (成功/失败/恋爱).

### The 商场收银 evolution ladder (the book's spine)
Calculator/POS → 简单工厂 (ch01) → 策略 + 简单工厂 (ch02) → + 装饰 for stackable promotions (ch06) → + 工厂方法 (ch08) → + 抽象工厂 with 反射 + 配置文件 (ch15). Each step is motivated by one new requirement; use it as the template for "how far should I go".

---

## Chapter Index

| # | Title | Key Frameworks |
|---|-------|----------------|
| [ch00](chapters/ch00-oo-basics.md) | 楔子 培训实习生——面向对象基础 | 类/实例, 封装, 继承, 多态, 抽象类, 接口, 泛型 |
| [ch01](chapters/ch01-simple-factory.md) | 代码无错就是优？ | 简单工厂 Simple Factory, 复制 vs 复用, 紧耦合 vs 松耦合, UML类图 |
| [ch02](chapters/ch02-strategy.md) | 商场促销 | 策略 Strategy, 策略+简单工厂 |
| [ch03](chapters/ch03-single-responsibility.md) | 电子阅读器vs.手机 | 单一职责原则 SRP |
| [ch04](chapters/ch04-open-closed.md) | 考研求职两不误 | 开放-封闭原则 OCP |
| [ch05](chapters/ch05-dependency-inversion.md) | 会修电脑不会修收音机？ | 依赖倒转原则 DIP, 里氏代换原则 LSP |
| [ch06](chapters/ch06-decorator.md) | 穿什么有这么重要？ | 装饰 Decorator, 简单工厂+策略+装饰 |
| [ch07](chapters/ch07-proxy.md) | 为别人做嫁衣 | 代理 Proxy (远程/虚拟/安全/智能指引) |
| [ch08](chapters/ch08-factory-method.md) | 工厂制造细节无须知 | 工厂方法 Factory Method, 简单工厂 vs 工厂方法 |
| [ch09](chapters/ch09-prototype.md) | 简历复印 | 原型 Prototype, 浅复制 vs 深复制 |
| [ch10](chapters/ch10-template-method.md) | 考题抄错会做也白搭 | 模板方法 Template Method |
| [ch11](chapters/ch11-law-of-demeter.md) | 无熟人难办事？ | 迪米特法则 LoD |
| [ch12](chapters/ch12-facade.md) | 牛市股票还会亏钱？ | 外观 Facade, 何时使用外观 (三层架构) |
| [ch13](chapters/ch13-builder.md) | 好菜每回味不同 | 建造者 Builder, Director |
| [ch14](chapters/ch14-observer.md) | 老板回来，我不知道 | 观察者 Observer, 接口 vs 抽象类, java.util.Observable |
| [ch15](chapters/ch15-abstract-factory.md) | 就不能不换DB吗？ | 抽象工厂 Abstract Factory, 反射, 配置文件 |
| [ch16](chapters/ch16-state.md) | 无尽加班何时休 | 状态 State, 方法过长坏味道 |
| [ch17](chapters/ch17-adapter.md) | 在NBA我需要翻译 | 适配器 Adapter (类/对象适配器) |
| [ch18](chapters/ch18-memento.md) | 如果再回到从前 | 备忘录 Memento, Originator/Caretaker |
| [ch19](chapters/ch19-composite.md) | 分公司=一部门 | 组合 Composite, 透明方式 vs 安全方式 |
| [ch20](chapters/ch20-iterator.md) | 想走？可以！先买票 | 迭代器 Iterator, java.util.Iterator |
| [ch21](chapters/ch21-singleton.md) | 有些类也需计划生育 | 单例 Singleton, 双重锁定, 静态初始化 |
| [ch22](chapters/ch22-bridge.md) | 手机软件何时统一 | 桥接 Bridge, 合成/聚合复用原则 CARP |
| [ch23](chapters/ch23-command.md) | 烤羊肉串引来的思考 | 命令 Command, Invoker/Receiver, 撤销/队列/日志 |
| [ch24](chapters/ch24-chain-of-responsibility.md) | 加薪非要老总批？ | 职责链 Chain of Responsibility |
| [ch25](chapters/ch25-mediator.md) | 世界需要和平 | 中介者 Mediator, Colleague |
| [ch26](chapters/ch26-flyweight.md) | 项目多也别傻做 | 享元 Flyweight, 内部状态 vs 外部状态 |
| [ch27](chapters/ch27-interpreter.md) | 其实你不懂老板的心 | 解释器 Interpreter, 音乐解释器 |
| [ch28](chapters/ch28-visitor.md) | 男人和女人 | 访问者 Visitor, 双分派 |
| [ch29](chapters/ch29-pattern-summary.md) | OOTV杯超级模式大赛——模式总结 | 创建型/结构型/行为型分类, 相似模式对比, 决赛应用题 |

## Topic Index

- **Abstract Factory / 抽象工厂** → ch15, ch29
- **Adapter / 适配器** → ch17, ch29
- **Bridge / 桥接** → ch22
- **Builder / 建造者** → ch13
- **Chain of Responsibility / 职责链** → ch24
- **Cohesion & coupling / 内聚与耦合, 紧耦合 vs 松耦合** → ch01, ch22, ch29
- **Command / 命令** → ch23
- **Composite / 组合** → ch19
- **Composition over inheritance / 合成/聚合复用原则 (CARP)** → ch22, ch29
- **Configuration file + reflection / 反射+配置文件** → ch15
- **Decorator / 装饰** → ch06
- **Dependency Inversion / 依赖倒转原则 (DIP)** → ch05
- **Double-checked locking / 双重锁定, volatile** → ch21
- **Facade / 外观, three-tier architecture / 三层架构** → ch12
- **Factory Method / 工厂方法** → ch08, ch15, ch29
- **Flyweight / 享元** → ch26
- **Interface vs abstract class / 接口 vs 抽象类** → ch00
- **Interpreter / 解释器** → ch27
- **Iterator / 迭代器** → ch20
- **Law of Demeter / 迪米特法则, 最少知识原则** → ch11, ch25
- **Liskov Substitution / 里氏代换原则 (LSP)** → ch05
- **Mediator / 中介者** → ch25
- **Memento / 备忘录** → ch18
- **Observer / 观察者, java.util.Observable** → ch14, ch29
- **Open-Closed / 开放-封闭原则 (OCP)** → ch04, ch08, ch29
- **Polymorphism, inheritance, encapsulation / 多态, 继承, 封装** → ch00, ch01
- **Prototype / 原型, deep vs shallow copy / 深复制 浅复制** → ch09
- **Proxy / 代理** → ch07
- **Refactoring / 重构, code smells / 坏味道** → ch00, ch01, ch10, ch16
- **Shopping-mall checkout / 商场收银** → ch02, ch06, ch08, ch15
- **Simple Factory / 简单工厂** → ch01, ch02, ch08, ch15
- **Single Responsibility / 单一职责原则 (SRP)** → ch03
- **Singleton / 单例** → ch21
- **State / 状态** → ch16
- **Strategy / 策略** → ch02, ch29
- **Template Method / 模板方法** → ch10
- **UML class diagrams / UML类图** → ch01
- **Visitor / 访问者, double dispatch / 双分派** → ch28

## Supporting Files

- [glossary.md](glossary.md) — all key terms with definitions (中/英)
- [patterns.md](patterns.md) — the 23 patterns and 6 principles as when/how/trade-off cards
- [cheatsheet.md](cheatsheet.md) — decision rules, similar-pattern disambiguation, code smells → pattern

---

## Scope & Limits

This skill covers the book content only. For hands-on implementation in your codebase,
combine with project-specific tools. For topics beyond this book, check related skills
or ask the agent directly.

Source note: in the PDF used, all code listings and UML diagrams were embedded as images.
They were recovered with OCR and cleaned by hand; code in the chapter files is a faithful
compact reconstruction, not a verbatim copy, and may differ from the printed listing in
minor details (variable names, comments).
