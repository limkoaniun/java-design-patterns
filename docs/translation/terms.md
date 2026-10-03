# Term table (en → zh)

Derived from glossary.md. Use the zh form everywhere. First mention per file: 中文（English）.

| English | 中文 |
|---|---|
| Abstract class | 抽象类 |
| Abstract Factory | 抽象工厂 |
| Adapter | 适配器 |
| Aggregation | 聚合 |
| Bridge | 桥接 |
| Builder | 建造者 |
| CARP | 合成/聚合复用原则 |
| Chain of Responsibility | 职责链 |
| Command | 命令 |
| Composite | 组合 |
| Composition | 合成（组合） |
| Coupling | 耦合 |
| Decorator | 装饰 |
| Deep copy | 深复制 |
| Dependency Inversion | 依赖倒转原则 (DIP) |
| Double-checked locking | 双重锁定 |
| Double dispatch | 双分派 |
| Encapsulation | 封装 |
| Extrinsic state | 外部状态 |
| Facade | 外观 |
| Factory Method | 工厂方法 |
| Flyweight | 享元 |
| Inheritance | 继承 |
| Interface | 接口 |
| Interpreter | 解释器 |
| Intrinsic state | 内部状态 |
| Iterator | 迭代器 |
| Law of Demeter | 迪米特法则 (LoD, 最少知识原则) |
| Liskov Substitution | 里氏代换原则 (LSP) |
| Mediator | 中介者 |
| Memento | 备忘录 |
| Observer | 观察者 |
| Open-Closed | 开放-封闭原则 (OCP) |
| Polymorphism | 多态 |
| Prototype | 原型 |
| Proxy | 代理 |
| Refactoring | 重构 |
| Shallow copy | 浅复制 |
| Simple Factory | 简单工厂模式 (prose); 简单工厂 only in headings and bare-name table cells |
| Single Responsibility | 单一职责原则 (SRP) |
| Singleton | 单例 |
| State | 状态 |
| Strategy | 策略 |
| Template Method | 模板方法 |
| Transparent vs safe Composite | 透明方式 vs 安全方式 |
| UML class diagram | UML类图 |
| Visitor | 访问者 |

## Fixed renderings (not in glossary, or overriding it)

Where a row below conflicts with the extracted table above, this block wins. Parentheticals in the extracted table such as `(DIP)` or `(LoD, 最少知识原则)` are glossary annotations, not part of the rendering; render the bare term and apply the 中文（English）first-mention rule from the brief.

| English | 中文 |
|---|---|
| Strategy (pattern name in prose) | 策略模式 |
| Simple Factory | 简单工厂模式 (prose); 简单工厂 only in headings and bare-name table cells |
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

Every one of the 24 pattern names (GoF 23 plus 简单工厂) takes the 模式 suffix in prose, matching the book's own usage: 观察者模式, 装饰模式, 工厂方法模式, 抽象工厂模式, 简单工厂模式, 单例模式, 原型模式, 建造者模式, 适配器模式, 桥接模式, 组合模式, 外观模式, 享元模式, 代理模式, 职责链模式, 命令模式, 解释器模式, 迭代器模式, 中介者模式, 备忘录模式, 状态模式, 策略模式, 模板方法模式, 访问者模式. Drop the suffix only inside the fixed `###` card headings of patterns.md (rule 2 of the brief) and inside tables whose en cell is the bare name. Principle names never take a suffix beyond 原则 (单一职责原则, 开放-封闭原则, 依赖倒转原则, 里氏代换原则, 迪米特法则, 合成/聚合复用原则).
Role names from UML (Context, Strategy, ConcreteStrategy, Creator, Product, Invoker, Receiver, Originator, Caretaker, Colleague) stay in English, in backticks when they name a class.
Tags `[DP]` `[DPE]` `[ASD]` `[J&DP]` stay exactly as written.

Additional fixed renderings: smart reference proxy → 智能指引代理; protection proxy → 安全代理 (the book's own names); 'unit test' → 单元测试; Builder in prose → 建造者模式（Builder）on first mention.

More fixed renderings (from batch-2 review): failure mode → 失效模式; "What it demonstrates" (code-example label) → 演示内容; intermediary / go-between (not the Mediator pattern) → 中间人; product family → 产品系列; the verb "compose / composes an X" (object composition) → 合成, never 组合 (组合 is reserved for the Composite pattern and for 投资组合-style ordinary nouns); "coupled" → 耦合 (add 紧 only when en says "tightly").
