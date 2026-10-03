# Chapter 29: OOTV杯超级模式大赛——模式总结 — Pattern Summary

## Core Idea
All 23 GoF patterns are personified as contestants judged by the six design principles; the chapter's real content is the side-by-side comparisons the judges force out of them and the closing thesis that every pattern is abstraction applied at a different level (class abstracts object, abstract class abstracts class, interface abstracts behaviour).

## Frameworks Introduced
- **Three GoF categories** — 创建型 (Creational, 5), 结构型 (Structural, 7), 行为型 (Behavioral, 11, split into two contest groups). See the full table under Reference Tables.
- **The judging panel = the six principles** — 单一职责, 开放-封闭, 依赖倒转, 里氏代换, 合成/聚合复用, 迪米特, with GoF as host. Patterns are evaluated by how well they serve these principles; 简单工厂 is eliminated in the pre-selection for violating 开放-封闭 (every extension edits the factory class).
- **Author's model of OO's purpose** (面向对象's opening speech) — procedural code models business flows, and flows are the most volatile part of requirements. OO models objects, which are more stable and closed; you cannot predict what will change, but you can usually predict where, and OO lets you encapsulate those areas. Patterns are reused, proven designs that lift your thinking "to the top of the mountain" [DPE].
- **Creational starting point** — “通常设计应该是从工厂方法开始，当设计者发现需要更大的灵活性时，设计便会向其他创建型模式演化。”[DP] Abstract Factory, Prototype and Builder are more flexible but more complex.
- **The four levels of pattern mastery** (from the preface, restated as the book's arc) — not knowing patterns; overusing them everywhere; knowing them all but unable to tell them apart; applying them fluently or not at all, 无剑胜有剑.

## Key Concepts
- **创建型模式**: abstract the instantiation process so a system is independent of how its objects are created, composed and represented [DP]; configuration can be static (compile time) or dynamic (runtime).
- **高内聚 / 松耦合**: cohesion is how tightly a routine's internals relate; coupling is how tightly it relates to other routines; aim for complete inside, small/direct/visible/flexible outside [DPE].
- **找出变化并封装之**: 桥接's motto, encapsulate the axes of change.
- **信息的隐藏促进了软件的复用**: 迪米特's question to 外观; weaker coupling means edits do not ripple.
- **代码重复 = 最糟糕的坏味道**: 模板方法's answer; subtle duplication hides in structures that look different but are the same [R2P].
- **架构模式 vs 设计模式**: MVC is absent from the contest because it combines Observer, Composite and Strategy and is an architectural pattern, not a design pattern.
- **抽象**: the finale thesis, class → abstract class → interface are abstraction of object → class → behaviour.

## Mental Models
- Use the contest brackets as a decision map: creational when the pain is in `new`, structural when it is in how classes fit together, behavioral when it is in how responsibilities and control flow move.
- Think of Proxy, Adapter and Facade as three kinds of "in-between": Proxy stands for one object and controls access; Adapter reuses an existing interface to make two mismatched ones work; Facade defines a new, simpler interface over a whole subsystem (larger grain).
- Think of Bridge and Adapter as the same trick at different life-cycle stages: Bridge separates abstraction from implementation at design time; Adapter reconciles already-built classes after the fact. 外观's verdict: neither is superior, they solve different problems.
- Think of Decorator as the cure for subclass explosion: rather than a subclass per combination of extensions, add responsibilities dynamically and transparently, and remove them when not needed.
- Think of Strategy as composition beating inheritance: hard-coding behaviours into subclasses B, C, D of A mixes algorithm with A; encapsulating them as Strategy objects lets them vary independently of A.
- Think of State as the answer to "when are condition branches acceptable?": only if the logic will not change or grow; since that is rare, distribute state-dependent code into state subclasses so new states are new classes.
- Think of Command and Chain of Responsibility as two answers to "why separate sender from implementer": Command so requests can be queued, logged, undone, made transactional; Chain so the handler can be determined at runtime by passing along a chain (the county → city → province → national hospital referral).

## Anti-patterns
- **Simple Factory as final design**: eliminated for modifying the factory on every extension.
- **Treating "the pattern I know" as the answer**: the fans' slogans; Hibernate bets on Bridge, ADO.NET on Adapter, and the judges pick Facade.
- **Inheritance for every variation**: the recurring failure Bridge, Decorator and Strategy all answer, class explosion and rigid hierarchies.
- **Confusing similar patterns**: the third mastery level; the judges' questions exist to draw the distinctions.
- **Answering last and borrowing everyone's examples**: ADO.NET's complaint about 工厂方法's finale answer, a reminder that the "winner" is the pattern that composes the others, not a single best pattern.

## Reference Tables

### The 23 patterns with the author's [DP] definitions

| # | Pattern | Definition [DP] | Chapter |
|---|---------|-----------------|---------|
| **创建型 Creational** | | | |
| 1 | 抽象工厂 Abstract Factory | 提供一个创建一系列或相关依赖对象的接口，而无须指定它们具体的类 | [ch15](ch15-abstract-factory.md) |
| 2 | 建造者 Builder | 将一个复杂对象的构建与它的表示分离，使得同样的构建过程可以创建不同的表示 | [ch13](ch13-builder.md) |
| 3 | 工厂方法 Factory Method | 定义一个用于创建对象的接口，让子类决定实例化哪一个类，使一个类的实例化延迟到其子类 | [ch08](ch08-factory-method.md) |
| 4 | 原型 Prototype | 用原型实例指定创建对象的种类，并且通过复制这些原型创建新的对象 | [ch09](ch09-prototype.md) |
| 5 | 单例 Singleton | 保证一个类仅有一个实例，并提供一个访问它的全局访问点 | [ch21](ch21-singleton.md) |
| **结构型 Structural** | | | |
| 6 | 适配器 Adapter | 将一个类的接口转换成客户希望的另外一个接口，使原本接口不兼容的类可以一起工作 | [ch17](ch17-adapter.md) |
| 7 | 桥接 Bridge | 将抽象部分与它的实现部分分离，使它们都可以独立地变化 | [ch22](ch22-bridge.md) |
| 8 | 组合 Composite | 将对象组合成树形结构以表示“部分-整体”的层次结构，使用户对单个对象和组合对象的使用具有一致性 | [ch19](ch19-composite.md) |
| 9 | 装饰 Decorator | 动态地给一个对象添加一些额外的职责；就增加功能来说，比生成子类更加灵活 | [ch06](ch06-decorator.md) |
| 10 | 外观 Facade | 为子系统中的一组接口提供一个一致的界面，定义一个高层接口使子系统更容易使用 | [ch12](ch12-facade.md) |
| 11 | 享元 Flyweight | 运用共享技术有效地支持大量细粒度的对象 | [ch26](ch26-flyweight.md) |
| 12 | 代理 Proxy | 为其他对象提供一种代理以控制对这个对象的访问 | [ch07](ch07-proxy.md) |
| **行为型 Behavioral (group 1)** | | | |
| 13 | 观察者 Observer | 定义对象间的一种一对多的依赖关系，当一个对象的状态发生改变时，所有依赖于它的对象都得到通知并被自动更新 | [ch14](ch14-observer.md) |
| 14 | 模板方法 Template Method | 定义一个操作的算法骨架，而将一些步骤延迟到子类中，使子类可以不改变算法结构即可重定义某些步骤 | [ch10](ch10-template-method.md) |
| 15 | 命令 Command | 将一个请求封装为一个对象，从而可用不同的请求对客户进行参数化；可对请求排队或记录日志，以及支持可撤销的操作 | [ch23](ch23-command.md) |
| 16 | 状态 State | 允许一个对象在其内部状态改变时改变它的行为，让对象看起来似乎修改了它的类 | [ch16](ch16-state.md) |
| 17 | 职责链 Chain of Responsibility | 使多个对象都有机会处理请求，避免请求的发送者和接收者之间的耦合；将这些对象连成一条链并沿链传递请求，直到有一个对象处理它 | [ch24](ch24-chain-of-responsibility.md) |
| **行为型 Behavioral (group 2)** | | | |
| 18 | 解释器 Interpreter | 给定一个语言，定义它的文法的一种表示，并定义一个解释器使用该表示来解释语言中的句子 | [ch27](ch27-interpreter.md) |
| 19 | 中介者 Mediator | 用一个中介对象来封装一系列的对象交互，使各对象不需要显式地相互引用，从而耦合松散，且可独立改变它们之间的交互 | [ch25](ch25-mediator.md) |
| 20 | 访问者 Visitor | 表示一个作用于某对象结构中的各元素的操作，使你可以在不改变各元素的类的前提下定义作用于这些元素的新操作 | [ch28](ch28-visitor.md) |
| 21 | 策略 Strategy | 定义一系列的算法，把它们一个个封装起来，并且使它们可相互替换，使算法可独立于使用它的客户而变化 | [ch02](ch02-strategy.md) |
| 22 | 备忘录 Memento | 在不破坏封装性的前提下，捕获一个对象的内部状态并在该对象之外保存，以后可将该对象恢复到原先保存的状态 | [ch18](ch18-memento.md) |
| 23 | 迭代器 Iterator | 提供一种方法顺序访问一个聚合对象中的各个元素，而又不需暴露该对象的内部表示 | [ch20](ch20-iterator.md) |

### Contest results (the author's implicit ranking of "most generally useful")

| Group | Judges' pick | Runners-up / notes |
|-------|--------------|--------------------|
| 创建型 | 工厂方法 (5 votes) | 单例 1 vote; 开放-封闭 votes Factory Method because new products need no change to factory or product hierarchy |
| 结构型 | 外观 (after a 3-way PK) | 桥接 and 适配器 tied at 2 votes each; 适配器 later reaches the final on audience votes |
| 行为型 1 | 观察者 (3 votes) | 模板方法 2, 命令 1 |
| 行为型 2 | 策略 (4 votes) | 迭代器 2 |
| Finalists | 工厂方法, 外观, 观察者, 策略, 适配器 | Champion never announced; 小菜 wakes up |

### Judges' pairwise contrasts

| Question | Answer the author wants remembered |
|----------|-----------------------------------|
| Proxy vs Facade | Proxy represents a single object and clients cannot reach the target directly; Facade represents a subsystem whose parts clients may still access directly, it just offers a simplified common interface [R2P] |
| Proxy vs Adapter | Both are connectors; Proxy invents a representative, Adapter does not, it composes the existing class for a specific use [DP] |
| Bridge vs Adapter | Bridge is planned at design start so abstraction and implementation evolve independently; Adapter makes two already-designed classes cooperate without redesigning either; different life-cycle stages, no winner |
| Facade vs Adapter | Facade defines a new interface; Adapter reuses an old one; Adapter adapts objects, Facade adapts a subsystem (coarser grain) |
| Bridge vs Decorator | Both fight inheritance explosion; Bridge decouples multiple independent axes of variation via composition; Decorator adds responsibilities to one object dynamically and reversibly |
| Command vs Chain of Responsibility | Both separate sender from implementer; Command to schedule, queue, log, undo, make transactional; Chain because the handler is unknown until runtime |
| Strategy vs inheritance | Subclassing A into B, C, D hard-codes behaviour into A; Strategy objects vary independently of A, easier to switch, understand, extend |
| Memento's encapsulation clause | Saving state transparently would couple the saver to A's internals; Memento shields A's internal information from other objects, preserving the encapsulation boundary |
| Visitor's "few friends" | Adding a concrete Element is hard; adding an operation over the structure is one new visitor |
| Mediator and Demeter | Distributing behaviour creates many connections; the mediator lets objects know only it, reducing connections, which is exactly 最少知识原则 |

## Worked Example
**The finale problem.** A young software company wants an in-house payroll system it may later sell. Employee pay types: regular staff (monthly salary + bonus), sales (base + commission), senior management (annual salary + dividends), part-timers (hourly). UI must have menus, toolbar, status bar, be plain and easy. SQL Server first, but Oracle/MySQL possible once it becomes a product. Many queries and statistics; complex charts, built in-house if time allows, otherwise bought from a third party.

How each finalist contributes:
1. **外观 Facade**: typical enterprise app, so three layers (presentation, business logic, data access). Requirements are clear on business, vague on UI. Insert a business facade layer between presentation and logic so any UI change (desktop client vs browser) cannot disturb business and data design.
2. **观察者 Observer**: menus, toolbar, status bar mean every click fires a chain of events; every event mechanism is Observer, one state change notifies all dependents. Build the whole presentation layer event-driven; the status bar is a control updated on events.
3. **适配器 Adapter**: "build charts ourselves if time allows, otherwise buy" is a stated point of variation. Encapsulate it: by 依赖倒转, the business module depends on an abstract chart-generation interface, not on a component or own code. Where third-party components have mismatched interfaces, adapt them.
4. **策略 Strategy**: several pay rules, but each is only a different calculation; storage and display are the same. Encapsulate each pay rule as an interchangeable strategy so adding or changing rules never touches the rest of the business logic.
5. **工厂方法 Factory Method**: object creation is unavoidable; to honour 开放-封闭, 依赖倒转 and 里氏代换 the user of an object should not know which concrete object it uses, so an "object manager" factory takes charge [DPE]. Hard-coding SQL Server would hurt when Oracle arrives; use abstract factory plus reflection (or an ORM) to decouple business from data access. The strategies and adapters above are also created through factories. Start with Factory Method; move to Abstract Factory, Prototype, Builder when more flexibility is needed [DP]. Factory Method does not reduce work, but it stops complex code from getting more complex when new cases appear [DPE].

The unstated lesson: a real system is not "one pattern"; it is layered facades, event-driven UI, strategies for the volatile rules, adapters at the third-party boundary, and factories wherever creation would otherwise pin you to a concrete class.

## Key Takeaways
1. Judge a pattern by the principles: does it keep you closed to modification, dependent on abstractions, substitutable, loosely coupled? 简单工厂 loses on exactly this test.
2. Start creational design with Factory Method; escalate to Abstract Factory, Prototype or Builder only when you need their flexibility.
3. Learn patterns in contrasting pairs (Proxy/Facade/Adapter, Bridge/Decorator, Command/Chain, State vs branches); the differences are what let you choose.
4. Composition over inheritance is the shared answer of Bridge, Decorator and Strategy to class explosion.
5. Behind every pattern is one idea, abstraction, applied at the object, class or behaviour level; 封装变化, 松耦合 and 针对接口编程 are how it shows up.
6. Do not chase a champion pattern; the payroll finale shows five patterns cooperating across layers.
7. MVC and similar are architectural patterns built from design patterns; do not confuse the two levels.

## Connects To
- **[ch00](ch00-oo-basics.md)**: the finale thesis (class/abstract class/interface as levels of abstraction) is the楔子's vocabulary paid off.
- **[ch03](ch03-single-responsibility.md)**, **[ch04](ch04-open-closed.md)**, **[ch05](ch05-dependency-inversion.md)**, **[ch11](ch11-law-of-demeter.md)**, **[ch22](ch22-bridge.md)** (合成/聚合复用): the judges.
- **[ch01](ch01-simple-factory.md)**: why 简单工厂 was eliminated before the finals.
- **[ch15](ch15-abstract-factory.md)**: the reflection-based data-access factory 工厂方法 recommends in the finale.
- **GoF (Design Patterns)**, **[DPE] Design Patterns Explained**, **[R2P] Refactoring to Patterns**, **[J&DP] Java与模式**: the sources the [tags] cite.
