# Chapter 5: 会修电脑不会修收音机？——依赖倒转原则 — Dependency Inversion & Liskov Substitution

## Core Idea
A PC is repairable by an amateur because every part plugs into a standard interface; a radio is unrepairable because everything is soldered together. Code should be a PC: make every dependency terminate at an abstraction (interface or abstract class), never at a concrete detail. The author calls this the hallmark of object-oriented design: "程序中所有的依赖关系都是终止于抽象类或者接口，那就是面向对象的设计，反之那就是过程化的设计了。"[ASD]

## Frameworks Introduced
- **依赖倒转原则 (Dependency Inversion Principle, DIP)** — author's exact formulation [ASD]:
  1. 高层模块不应该依赖低层模块。两个都应该依赖抽象。
  2. 抽象不应该依赖细节。细节应该依赖抽象。
  - Plain-language version: "针对接口编程，不要对实现编程。"
  - When to use: whenever a high-level policy module (business logic) would otherwise call a low-level utility module (database access, I/O) directly and you expect the low-level side to be swapped.
  - How: introduce an interface owned by the high-level side; both the business code and the concrete low-level implementation depend on that interface. Structure: `高层模块 → «interface» 接口或抽象类 ← 低层模块`.
  - Why "倒转": in procedural code, reuse flowed upward (high-level modules called a library of low-level functions, so they depended on it). DIP flips the arrow so the low-level detail depends on the abstraction the high-level module defines.
  - Story analogy: repairing a computer by phone works because memory, CPU and disk are interchangeable against standard sockets (强内聚、松耦合); a radio can't be repaired because its resistors and transistors are all soldered to each other (耦合过度).
- **里氏代换原则 (Liskov Substitution Principle, LSP)** — author's exact formulation [ASD]: "子类型必须能够替换掉它们的父类型。" Longer form: a software entity that uses a parent class must work unchanged with any of its subclasses, and must not be able to tell the difference.
  - When to use: every time you decide whether B should inherit A. Ask "can every place that uses an A be handed a B without behaviour changing?"
  - How: only inherit if the subclass honours every non-private behaviour of the parent. If the parent promises `飞()`, a penguin subclass that can't fly breaks the promise; give the parent only what all children satisfy (e.g. `下蛋()`), or don't inherit.
  - Why it matters: LSP is what makes DIP safe. You can depend on the abstraction only because any concrete subtype can be plugged in without the caller changing. It is also what makes open-closed extension possible: "正是由于子类型的可替换性才使得使用父类类型的模块在无须修改的情况下就可以扩展。"

## Key Concepts
- **高层模块 / 低层模块**: business-policy code vs. mechanism code (e.g. database access functions) — the pair whose dependency direction DIP inverts.
- **抽象 (abstraction)**: an interface or abstract class that both sides depend on; stable, so changes on either side don't ripple.
- **细节 (detail)**: a concrete implementation class; volatile, must depend on the abstraction, never be depended upon.
- **强内聚、松耦合**: the OO name for a PC's "易插拔" property; each part is self-contained, connected only via standard interfaces.
- **可替换性 (substitutability)**: the LSP property; subclass instances can stand in for parent instances anywhere.
- **接口 (interface)**: the CPU-socket analogy: define the contract, hide arbitrary internal complexity, and any conforming part fits.

## Mental Models
- Think of your system as a PC, not a radio: if a bad "memory stick" forces you to replace the "motherboard", the dependency arrows point the wrong way.
- Use "who defines the interface?" as the tell: if the high-level module dictates the contract and the low-level module implements it, the dependency is inverted correctly.
- Think of inheritance as a promise: a subclass is only legitimate when it can keep every promise the parent's public methods make (penguin ≠ flying bird).
- Use LSP to reason about growth: because `Cat`, `Dog`, `Cow` all substitute for `Animal`, adding a new animal changes only the instantiation site.

## Anti-patterns
- **High-level business modules bound to a concrete database layer**: works until the customer wants a different database; the mature business logic can't be reused because it is welded to the old detail.
- **Inheriting because it's biologically true**: "企鹅是鸟" in taxonomy, but if `鸟` declares `飞()`, `企鹅 extends 鸟` violates LSP and any code calling `鸟.飞()` breaks.
- **Radio-style coupling**: every component references every other; any fault might be anywhere, so nobody but the original author can maintain it (the author cites a bank that had to halt servers for most of a day to trace one fault).
- **Treating "uses abstract classes" as "is object-oriented"**: the test is not language features but whether all dependencies end at abstractions.

## Code Examples
The chapter's only listing is the substitutability demo that makes LSP concrete:

```java
// Client depends on the parent type only.
动物 animal = new 猫();   // later: new 狗(), new 牛(), new 羊()
animal.吃喝();
animal.移动();            // 跑、飞、游…
// Swapping the concrete subclass changes ONLY the instantiation line;
// every other line that talks to `animal` is untouched.
```
- **What it demonstrates**: because each subclass can replace `动物` without changing behaviour, the calling module is closed to modification and open to extension, which is why DIP can safely target the abstraction.

Structural shape of DIP (from the chapter's diagram):

```java
interface IDataAccess { /* contract the business layer needs */ }   // owned by the high-level side
class BusinessModule { private IDataAccess dao; /* uses only the interface */ }
class MySqlAccess implements IDataAccess { /* detail depends on abstraction */ }
```

## Worked Example
1. **Naive version (procedural reuse)**: every project needs database access, so those routines are written once as a low-level function library. New projects call it directly. High-level depends on low-level.
2. **What broke**: the next customer wants a different database or storage method. The business logic is identical, but it can't be reused because it is bound to the old access functions. Analogy: if CPU, RAM and disk all depended on one specific motherboard, one dead board would kill every part.
3. **Refactored design**: define an interface (or abstract class) that the business module depends on; make each concrete storage implementation depend on that interface too. Now either side can change as long as the interface is stable.
4. **Why it works**: LSP guarantees any implementation can be substituted for the abstraction without the caller noticing, so the caller never needs modification. Open-closed follows.
5. **Sanity check via the penguin**: the author uses the bird/penguin case to show why substitutability is a design decision, not a taxonomy fact: if the parent promises `飞()`, the penguin can't be its subtype.

## Key Takeaways
1. Make all dependencies terminate at abstractions; that single test distinguishes OO design from procedural design.
2. State DIP the author's way: high-level and low-level modules both depend on abstractions; abstractions never depend on details.
3. Only inherit when the subclass can replace the parent everywhere without changing behaviour (LSP); otherwise compose or redesign the parent.
4. LSP is the enabling condition for both DIP and the open-closed principle; teach them together.
5. Prefer a system you can "repair by swapping parts" over one that is compact but soldered together.

## Connects To
- **[ch04](ch04-open-closed.md)**: open-closed extension is only possible because substitutable subtypes exist.
- **[ch03](ch03-single-responsibility.md)**: the PC analogy also illustrates SRP (a dead memory stick is no reason to replace the CPU).
- **[ch08](ch08-factory-method.md)**: factory method is DIP applied to object creation: the client depends on an `IFactory` interface, not on concrete factories.
- **[ch15](ch15-abstract-factory.md)**: the database-swapping scenario introduced here is solved concretely with abstract factory and reflection.
- **[ch22](ch22-bridge.md)**: 合成/聚合复用原则 extends this chapter's "prefer interfaces over concrete inheritance" theme.
