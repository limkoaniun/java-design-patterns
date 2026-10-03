# Chapter 2: 商场促销——策略模式 — Store Promotions: Strategy

## Core Idea
Discounts, rebates and "满300返100" are interchangeable algorithms for one job (compute the amount due). Strategy encapsulates each algorithm in its own class behind a common parent and hands the client a Context, so algorithms can be swapped, added and unit-tested without the client changing. "策略模式封装了变化" (Strategy encapsulates variation), and combined with Simple Factory it reduces the client to knowing a single class.

## Frameworks Introduced
- **策略模式 (Strategy)** — “它定义了算法家族，分别封装起来，让它们之间可以互相替换，此模式让算法的变化，不会影响到使用算法的客户。”[DP]
  - Structure: `Strategy` (abstract, `algorithmInterface()`) ← `ConcreteStrategyA/B/C`; `Context` holds a `Strategy` reference and exposes `contextInterface()` that delegates to it.
  - When to use: several algorithms do the same work with different implementations and are swapped at runtime; the author extends this to "almost any type of rule": “只要在分析过程中听到需要在不同时间应用不同的业务规则，就可以考虑使用策略模式处理这种变化的可能性”[DPE].
  - How: (1) abstract strategy with the operation; (2) one concrete class per algorithm, parameterised rather than one class per *value* (one `CashRebate(0.8)` not `Rebate80`, `Rebate70`); (3) a Context constructed with a strategy, delegating; (4) client instantiates Context and calls it.
- **策略 + 简单工厂结合 (Strategy combined with Simple Factory)** — the factory `switch` moves inside `CashContext(int cashType)`. Client goes from knowing two classes (`CashSuper`, `CashFactory`) to knowing one (`CashContext`); even the strategy parent is hidden.
- **类的划分基础是抽象 (Classes are drawn by abstraction, not by count)** — “面向对象的编程，并不是类越多越好……打一折和打九折只是形式的不同，抽象分析出来，所有的打折算法都是一样的，所以打折算法应该是一个类。”

## Key Concepts
- **算法家族 (Algorithm family)**: the set of interchangeable computations (normal, rebate, return).
- **Context (上下文)**: the object configured with a strategy that clients actually talk to.
- **变化点 (Variation point)**: the thing that changes (here, the pricing rule); OO's core move is to encapsulate it.
- **CashSuper / CashNormal / CashRebate / CashReturn**: the book's strategy hierarchy; `acceptCash(price, num)` is the algorithm.
- **反射 (Reflection)**: foreshadowed as the way to remove the last `switch` (see ch15).

## Mental Models
- **Use Strategy when you hear "at different times we apply different rules".** Pricing, tax, shipping, scoring: any rule family.
- **Think of Strategy as Simple Factory's sibling with a different question.** Factory answers "which object?"; Strategy answers "which algorithm, swappable at will?". The author shows the same four classes serve both; only the client-facing shape differs.
- **Prefer parameters over subclasses for values.** Eight-percent and seven-percent are one class with a constructor argument; "满300返100" and "满500返200" are one class with two arguments.
- **Move selection out of the client.** Basic Strategy leaves the `switch` in the client; combining with a factory pushes it into the Context; reflection (later) deletes it.

## Anti-patterns
- **Hard-coding the discount** (`totalPrices * 0.8`): promotion ends, you redeploy every register.
- **A `switch` per promotion in the UI**: three branches whose bodies differ only by a constant; duplication plus a growing client.
- **One subclass per discount value** (`Rebate80`, `Rebate70`, `Rebate50`, ...): confuses form with substance; the abstraction is "rebate", the value is data.
- **Basic Strategy with a client-side `switch`**: “不又回到了原来的老路了吗”; the client still decides. Fold selection into the Context.
- **Simple Factory alone for volatile rules**: every promotion change edits, recompiles and redeploys the factory: “这真的是很糟糕的处理方式”.

## Code Examples
The strategy family (unchanged from the Simple Factory version) and the combined Context:

```java
// 收费抽象类 — the Strategy
public abstract class CashSuper {
    public abstract double acceptCash(double price, int num);
}

public class CashNormal extends CashSuper {
    public double acceptCash(double price, int num) { return price * num; }
}

public class CashRebate extends CashSuper {
    private double moneyRebate = 1d;
    public CashRebate(double moneyRebate) { this.moneyRebate = moneyRebate; }   // 八折就输入0.8
    public double acceptCash(double price, int num) { return price * num * this.moneyRebate; }
}

public class CashReturn extends CashSuper {
    private double moneyCondition = 0d;  // 返利条件
    private double moneyReturn    = 0d;  // 返利值
    public CashReturn(double moneyCondition, double moneyReturn) {
        this.moneyCondition = moneyCondition;
        this.moneyReturn    = moneyReturn;
    }
    public double acceptCash(double price, int num) {
        double result = price * num;
        if (moneyCondition > 0 && result >= moneyCondition)
            result = result - Math.floor(result / moneyCondition) * moneyReturn;
        return result;
    }
}

// Context with the factory folded in (策略与简单工厂结合)
public class CashContext {
    private CashSuper cs;
    public CashContext(int cashType) {
        switch (cashType) {
            case 1: this.cs = new CashNormal();            break;
            case 2: this.cs = new CashRebate(0.8d);        break;
            case 3: this.cs = new CashRebate(0.7d);        break;
            case 4: this.cs = new CashReturn(300d, 100d);  break;
        }
    }
    public double getResult(double price, int num) { return this.cs.acceptCash(price, num); }
}

// 客户端 — knows only CashContext
CashContext cc = new CashContext(discount);
totalPrices = cc.getResult(price, num);
total = total + totalPrices;
```
- **What it demonstrates**: `CashSuper` and its subclasses did not change between the factory version and the strategy version; only the client-facing object did. The client no longer sees `CashSuper` at all.

## Reference Tables
| | 简单工厂 (Simple Factory) | 策略 (basic) | 策略 + 简单工厂 |
|---|---|---|---|
| Client knows | `CashSuper`, `CashFactory` | `CashSuper`, `CashContext`, all concrete strategies | `CashContext` only |
| Where the `switch` lives | Factory | Client | Context constructor |
| Client call | `CashFactory.createCashAccept(n).acceptCash(p, q)` | `new CashContext(new CashRebate(0.8)).getResult(p, q)` | `new CashContext(n).getResult(p, q)` |
| Adding a rule | new subclass + factory branch | new subclass + client branch | new subclass + Context branch |
| Coupling | medium | high (client picks) | lowest of the three |

## Worked Example
Assignment: a 商场收银 (store checkout) that takes unit price and quantity and totals the bill.

**v1.0**: `totalPrices = price * num` in a `do/while` loop. 大鸟: now everything is 20% off.

**v1.1**: a `discount` selector and a `switch` with `* 0.8` and `* 0.7`. Better, but three near-identical branches, and now the store wants 满300返100.

**Simple Factory (via ch01)**: 小菜 proposes a subclass per promotion. 大鸟: how many? "要几个写几个" is wrong. Abstraction finds two shapes: rebate (one parameter) and return (two parameters). Result: `CashSuper` ← `CashNormal`, `CashRebate(rate)`, `CashReturn(condition, amount)`; `CashFactory.createCashAccept(int)`. Adding 满100积分10点 = one subclass + one branch. Verdict: solves creation, but promotions change constantly and each change recompiles the factory.

**Strategy (v1.2)**: 小菜 finds the pattern himself. Existing classes untouched; add `CashContext(CashSuper)` with `getResult`. Client now has the `switch` choosing which strategy to pass. 小菜: haven't we just moved the problem back to the client?

**Strategy + Factory**: “难道简单工厂就一定要是一个单独的类吗？” Move the `switch` into `CashContext(int cashType)`. Client: `new CashContext(discount).getResult(price, num)`. Coupling drops: the client never learns `CashSuper` exists.

**Remaining flaw**: adding 满200送50 still edits the `switch` in `CashContext`. "任何需求的变更都是需要成本的", but the master minimises it; reflection (ch15) will remove the branch entirely.

Why it works: the *algorithm family* is stable in shape (price, quantity → amount) while its *members* churn. Strategy fixes the shape and lets the members vary.

## Key Takeaways
1. When the same job has several interchangeable algorithms, give each its own class behind one abstract parent.
2. Strategy's stated wins: reusable algorithm hierarchy, easier unit testing (each algorithm tested alone), and elimination of conditionals in the client [DP][DPE].
3. Parameterise variants; do not mint a class per constant.
4. Fold selection into the Context so the client depends on exactly one class.
5. Strategy generalises beyond algorithms to any business rule that changes over time.
6. A `switch` that grows with each new rule is a cost you have merely relocated, not removed.

## Connects To
- **[ch01](ch01-simple-factory.md)**: same class hierarchy; the author contrasts the two client shapes side by side.
- **[ch04](ch04-open-closed.md)**: the residual `switch` in `CashContext` is exactly what OCP objects to.
- **[ch06](ch06-decorator.md)** and **[ch08](ch08-factory-method.md)**: the checkout is upgraded again with Decorator (stackable promotions) and Factory Method.
- **[ch15](ch15-abstract-factory.md)**: reflection + configuration removes the last `switch`.
- **[ch29](ch29-pattern-summary.md)**: Strategy reaches the final; the author's own framing of "composition over inheritance for interchangeable behaviour".
