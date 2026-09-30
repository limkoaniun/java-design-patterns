# Chapter 1: 代码无错就是优？——简单工厂模式 — "Bug-free equals good?": Simple Factory

## Core Idea
Correct output is the lowest bar. The interview calculator was rejected because it was not 可维护、可复用、可扩展、灵活性好 (maintainable, reusable, extensible, flexible): the four qualities the author uses as the definition of good OO code. Simple Factory is the first tool for getting there: isolate *which object to instantiate* into one class so that business classes, the factory and the UI change independently.

## Frameworks Introduced
- **面向对象的四大好处 (The four payoffs of OO)** — 可维护 (maintainable), 可复用 (reusable), 可扩展 (extensible), 灵活性好 (flexible). Taught through the 活字印刷 (movable-type printing) story: change one character, reuse characters across books, add characters, re-arrange layout. Woodblock printing (the naive calculator) can do none of these because everything is carved on one plate: coupling.
  - When to use: as the evaluation checklist for any piece of code, before "does it run".
- **业务逻辑与界面逻辑分离 (Separate business logic from UI logic)** — extract an `Operation` class so the same arithmetic serves console, desktop, web and mobile clients. This is encapsulation, the first of the three OO features.
- **紧耦合 vs 松耦合 (Tight vs loose coupling)** — one `switch` holding add/sub/mul/div means adding `pow` forces the other four to recompile and exposes them to accidental (or malicious) edits: the payroll story where the maintainer sneaks `salary *= 1.1` into the monthly-salary branch. Split each algorithm into its own subclass of an abstract `Operation` (inheritance + polymorphism).
- **简单工厂模式 (Simple Factory)** — a separate class whose single job is to decide which concrete `Operation` to instantiate, returning it as the abstract parent type.
  - Structure: `Operation` (abstract product) ← `Add`/`Sub`/`Mul`/`Div` (concrete products); `OperationFactory.createOperate(String)` (factory, static switch); client sees only `Operation` and the factory.
  - When to use: the *choice* of which class to instantiate is the thing likely to change or grow.
  - How: (1) abstract product with the operation method; (2) one subclass per algorithm; (3) a factory whose `switch` maps an input token to `new Concrete()`; (4) client calls factory, then the polymorphic method.
- **UML 类图 (UML class diagram basics)** — class box (name / fields and properties / methods; `+` public, `-` private, `#` protected; italic name = abstract); `<<interface>>` box or 棒棒糖 (lollipop) notation; 继承 (inheritance) hollow triangle + solid line; 实现接口 (realisation) hollow triangle + dashed line; 关联 (association) solid arrow, "knows about" (`Penguin` holds a `Climate`); 聚合 (aggregation) hollow diamond, weak ownership (雁群 has 大雁); 合成/组合 (composition) filled diamond, whole-part with shared lifetime (鸟 has 翅膀, cardinality 1–2); 依赖 (dependency) dashed arrow (Animal's metabolism depends on Oxygen, Water as parameters).

## Key Concepts
- **可维护 (Maintainable)**: change only what needs changing.
- **可复用 (Reusable)**: the same class serves multiple front-ends.
- **可扩展 (Extensible)**: add by adding, not by editing.
- **灵活性 (Flexible)**: re-arrange without re-building.
- **封装 (Encapsulation)**: hide the engine, expose the pedal.
- **多态 (Polymorphism)**: the factory returns `Operation`; the call `oper.getResult()` runs the subclass's code.
- **基数 (Cardinality)**: the `1`/`2`/`n` on association ends.

## Mental Models
- **Think of the naive calculator as woodblock printing.** Every change means re-carving the plate. Think of the OO version as movable type.
- **Use "does adding a feature force me to hand over unrelated code?" as the coupling smell.** If adding `pow` needs the `add` source, the design is tightly coupled.
- **Use a factory when instantiation is the variation point.** "到底要实例化谁，将来会不会增加实例化的对象……应该考虑用一个单独的类来做这个创造实例的过程."
- **Beginners think in computer steps; OO thinks in responsibilities.** "Input two numbers, branch on operator" is the CPU's view; `Operation`, `Add`, factory, UI is the domain's view.

## Anti-patterns
- **Variable names `A`, `B`, `C`, `D`**: non-descriptive; the first thing 大鸟 flags.
- **Chained `if` without `else` on the operator**: every branch is evaluated; use `switch`.
- **No division-by-zero check, repeated `Double.parseDouble`**: correctness and duplication issues that reveal a "works on my input" mindset.
- **Copy-paste to reuse across UIs**: "初级程序员的工作就是Ctrl+C和Ctrl+V"; duplication turns maintenance into disaster.
- **One `switch` containing every algorithm**: adding one forces recompiling all; every maintainer of any algorithm can break every other.
- **Forgetting the factory also changes**: adding a subclass is not enough; the factory's `switch` gains a branch. This is the pattern's known weakness, revisited in ch08.

## Code Examples
```java
public abstract class Operation {
    public double getResult(double numberA, double numberB) { return 0d; }
}

public class Add extends Operation {
    public double getResult(double numberA, double numberB) { return numberA + numberB; }
}
public class Sub extends Operation {
    public double getResult(double numberA, double numberB) { return numberA - numberB; }
}
public class Mul extends Operation {
    public double getResult(double numberA, double numberB) { return numberA * numberB; }
}
public class Div extends Operation {
    public double getResult(double numberA, double numberB) {
        if (numberB == 0) {
            System.out.println("除数不能为0");
            throw new ArithmeticException();
        }
        return numberA / numberB;
    }
}

// 简单运算工厂类
public class OperationFactory {
    public static Operation createOperate(String operate) {
        Operation oper = null;
        switch (operate) {
            case "+": oper = new Add(); break;
            case "-": oper = new Sub(); break;
            case "*": oper = new Mul(); break;
            case "/": oper = new Div(); break;
        }
        return oper;
    }
}

// 客户端
Operation oper = OperationFactory.createOperate(strOperate);
double result = oper.getResult(numberA, numberB);
```
- **What it demonstrates**: the client never names a concrete class; changing `Add` touches one file; adding `Pow` means one new subclass plus one factory branch, and the UI is untouched.

## Reference Tables
| UML relationship | Notation | Meaning | Book example |
|---|---|---|---|
| 继承 Inheritance | Hollow triangle, solid line | is-a | 鸟 → 动物 |
| 实现 Realisation | Hollow triangle, dashed line | implements interface | 大雁 → IFly |
| 关联 Association | Solid arrow | knows about (field reference) | 企鹅 → 气候 |
| 聚合 Aggregation | Hollow diamond | weak has-a, parts outlive whole | 雁群 ◇→ 大雁 |
| 合成/组合 Composition | Filled diamond, cardinality | strong has-a, same lifetime | 鸟 ◆→ 翅膀 (1:2) |
| 依赖 Dependency | Dashed arrow | uses as parameter/temporary | 动物 --> 氧气, 水 |

## Worked Example
The interview task: "用任意一种面向对象语言实现一个计算器控制台程序，输入两个数和运算符号，得到结果."

**v1 (rejected)**: everything in `main`; `String A, B, C; double D;` four independent `if`s on the operator, `parseDouble` repeated eight times, no zero check. Runs correctly. Fails the real question, which was "show me you can write OO code".

**v2 (code hygiene)**: `numberA`, `strOperate`, `numberB`, a `switch`, a `try/catch`. Still procedural: it reads the problem as computer steps.

**v3 (encapsulation)**: `Operation.getResult(numberA, numberB, operate)` holds the `switch`; `main` only does I/O. Now a Windows or web calculator reuses `Operation`. 大鸟's verdict: only one of the three OO features used.

**v4 (inheritance + polymorphism)**: ask "if I add `pow`, what must I touch?" Answer: the shared `switch`, and therefore every algorithm. Payroll analogy: giving a contractor the monthly-salary code to add an hourly rate is how `salary *= 1.1` gets slipped in. Split into abstract `Operation` and `Add`/`Sub`/`Mul`/`Div`. New problem: who decides which subclass to `new`?

**v5 (Simple Factory)**: `OperationFactory.createOperate("+")` returns an `Operation`. Quiz: change addition → edit `Add`; add sqrt/sin → new subclass **and** a factory branch; change the UI → edit the UI only.

Why it works: the three axes of change (algorithm internals, set of algorithms, presentation) now live in three places. Why it is not the end: the factory still has a `switch` that grows with every algorithm (see ch02, ch08).

## Key Takeaways
1. Judge code by 可维护、可复用、可扩展、灵活性好, not by "it runs".
2. First separate business logic from UI; that alone gives reuse across front-ends.
3. When adding a variant forces edits to sibling variants, the design is tightly coupled; split variants into subclasses of an abstraction.
4. Put the "which class to instantiate" decision in a factory; the client works only with the abstract type.
5. Simple Factory's cost is a growing `switch`; know it before choosing it.
6. Learn UML class diagrams: they are how the rest of the book communicates structure.

## Connects To
- **[ch00](ch00-oo-basics.md)**: prerequisite; the author says if v4 is hard to read, go back to the prologue.
- **[ch02](ch02-strategy.md)**: the same shape (abstract parent, subclasses) reappears as Strategy, and the factory is folded into a Context.
- **[ch04](ch04-open-closed.md)**: the v1→v5 evolution is retold as the textbook illustration of the Open-Closed Principle.
- **[ch08](ch08-factory-method.md)**: replaces the factory's `switch` with one factory subclass per product.
- **[ch15](ch15-abstract-factory.md)**: reflection removes the `switch` entirely.
