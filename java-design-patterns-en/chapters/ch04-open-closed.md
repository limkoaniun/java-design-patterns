# Chapter 4: 考研求职两不误——开放-封闭原则 — Exams and Job Hunting Both: Open-Closed Principle

## Core Idea
Software entities should be extendable without being modified. You cannot predict every change, so do not try; instead, when the *first* change of a kind arrives, build the abstraction that isolates that kind, and thereafter meet new requirements by adding code rather than editing working code. The author calls this “面向对象设计的核心所在” (the core of OO design) and pairs it with an equally strong warning against premature abstraction.

## Frameworks Introduced
- **开放-封闭原则 (Open-Closed Principle, OCP)** — “软件实体（类、模块、函数等）应该可以扩展，但是不可修改。”[ASD] Two features: “对于扩展是开放的 (Open for extension)” and “对于修改是封闭的 (Closed for modification)”[ASD].
  - Story analogy: 一国两制 (one country, two systems): the mainland system is closed to modification, so reunification worked by *adding* a second system rather than rewriting either. Also: a boss who cannot fix lateness by punishment redefines the closed thing (8 hours / results) and opens the schedule (flexitime).
  - When to use: at the first sign of a recurring kind of change; and as the standard for judging any pattern (it is the criterion that eliminated Simple Factory in ch29).
  - How: (1) write the first version assuming no change; (2) when a change arrives, do not patch; create an abstraction that isolates *that kind* of change; (3) route the new requirement through a new class; (4) leave existing classes untouched.
- **何时应对变化 (When to respond to change)** — “在我们最初编写代码时，假设变化不会发生。当变化发生时，我们就创建抽象来隔离以后发生的同类变化。”[ASD] And: “等到变化发生时立即采取行动”[ASD]. Falling in the same place twice is your fault.
- **拒绝不成熟的抽象 (Refuse immature abstraction)** — “开发人员应该仅对程序中呈现出频繁变化的那些部分做出抽象，然而，对于应用程序中的每个部分都刻意地进行抽象同样不是一个好主意。拒绝不成熟的抽象和抽象本身一样重要。”[ASD]
- **选择对什么封闭 (Choose what to close against)** — “无论模块是多么的'封闭'，都会存在一些无法对之封闭的变化。……设计人员必须对于他设计的模块应该对哪种变化封闭做出选择。他必须先猜测出最有可能发生的变化种类，然后构造抽象来隔离那些变化。”[ASD]

## Key Concepts
- **软件实体 (Software entity)**: class, module, function; OCP applies at every granularity.
- **对扩展开放 (Open for extension)**: new behaviour can be added.
- **对修改封闭 (Closed for modification)**: existing, working source is not edited to add it.
- **抽象隔离变化 (Abstraction isolates change)**: the mechanism (inheritance, polymorphism, interfaces) by which closure is achieved.
- **过度设计 (Over-design)**: abstracting parts that never vary; the opposite failure.
- **变化的时机 (Timing of change)**: the longer you wait to identify a variation, the harder the right abstraction becomes [ASD].

## Mental Models
- **Use "first time is not your fault; second time is" as the trigger.** One change: accept the edit. The same *kind* of change again: extract the abstraction now.
- **Think of closure as a choice, not a property.** Every module is open to some change; you decide which changes it must be closed against and pay for abstraction only there.
- **Prefer adding a class over editing one.** If a requirement can be met by a new subclass, the design already obeys OCP; if it requires editing a `switch` in stable code, it does not.
- **Abstraction has a price; charge it only where change is frequent.** "过犹不及" (too far is as bad as not far enough).

## Anti-patterns
- **Trying to foresee every change up front**: “那不就成了未卜先知”; impossible, and it produces speculative complexity.
- **Patching the original class for each new requirement**: adding subtraction inside the addition client; the ch01 v1–v3 shape.
- **Abstracting everything "just in case"**: makes simple designs complex and is itself a violation of the spirit of OCP.
- **Waiting too long**: once add/sub are used in many places, extracting `Operation` becomes expensive; act at the first repeat.
- **Absolute closure as a goal**: "绝对的对修改关闭是不可能的"; aim for closure against the likely changes, not all.

## Code Examples
The chapter references ch01's calculator as its worked code. The OCP-compliant shape:

```java
// Closed: this hierarchy is never edited when a new operation arrives
public abstract class Operation {
    public abstract double getResult(double numberA, double numberB);
}
public class Add extends Operation {
    public double getResult(double a, double b) { return a + b; }
}
public class Sub extends Operation {
    public double getResult(double a, double b) { return a - b; }
}

// Open: a new requirement is met by adding a class, not editing one
public class Pow extends Operation {
    public double getResult(double a, double b) { return Math.pow(a, b); }
}

// Client depends on the abstraction, so it is closed too
Operation oper = OperationFactory.createOperate(strOperate);
double result = oper.getResult(numberA, numberB);
```
- **What it demonstrates**: `Add`, `Sub` and the client are untouched by `Pow`. (The factory's `switch` is the one place still open to modification; ch08 and ch15 close it.)

## Worked Example
The author retells the ch01 calculator as an OCP timeline:

1. **Addition only**, all in one client class. Change has not happened; no abstraction. Correct by OCP's own rule ("假设变化不会发生").
2. **Add subtraction.** Doing it requires editing the client: the first violation. This is the moment to act: refactor, introduce abstract `Operation`, isolate `Add` and `Sub` behind inheritance and polymorphism. Requirements are still met, and the design can now absorb the *kind* of change just observed.
3. **Add multiplication and division.** No edits to the client, `Add` or `Sub`; two new subclasses. "对程序的改动是通过增加新代码进行的，而不是更改现有的代码"[ASD]: this is the spirit of OCP.
4. **The warning.** Had add/sub already been called from many places before step 2, extracting `Operation` would have been much harder. And had 小菜 abstracted `Operation` at step 1 with only addition, it would likely have been over-design.

The life lesson the chapter hangs on it: 小菜 failed the postgraduate exam by two marks and had no job leads because he did nothing but study. 大鸟: the study plan is closed to modification; the *schedule* should have been open to extension (write a CV, watch recruitment) with no harm to the plan. The author's own footnote admits the analogy is “有些牵强” (a bit forced): treat it as mnemonic, not doctrine.

## Key Takeaways
1. Extend by adding code; do not modify working code to add behaviour.
2. Write v1 assuming no change; on the first change of a kind, build the abstraction that isolates that kind.
3. Decide deliberately which changes a module is closed against; total closure is impossible.
4. Refusing premature abstraction matters as much as abstracting; abstract only the frequently changing parts.
5. Act early: the cost of the right abstraction rises with every place the un-abstracted code is used.
6. OCP is the source of OO's promised benefits: 可维护、可扩展、可复用、灵活性好.

## Connects To
- **[ch01](ch01-simple-factory.md)**: the calculator's v1→v5 evolution is OCP's canonical example here.
- **[ch02](ch02-strategy.md)**: Strategy is OCP applied to interchangeable algorithms; its remaining `switch` is the residual openness.
- **[ch05](ch05-dependency-inversion.md)**: programming to abstractions is the technique that makes closure possible.
- **[ch08](ch08-factory-method.md)** and **[ch15](ch15-abstract-factory.md)**: close the factory's `switch` via subclassing and reflection.
- **[ch29](ch29-pattern-summary.md)**: 开放封闭 is the judge who eliminates Simple Factory (“你在对每一次扩展时都要更改工厂类”) and votes for Factory Method.
