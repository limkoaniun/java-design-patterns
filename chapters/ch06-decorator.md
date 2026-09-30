# Chapter 6: 穿什么有这么重要？——装饰模式 — Decorator

## Core Idea
When a feature is only needed in some situations and in varying combinations, don't add fields and methods to the core class; put each feature in its own wrapper class that implements the same interface as the thing it wraps, and let the client stack wrappers at run time in whatever order it needs. The story: dressing 小菜 (T-shirt, baggy trousers, sneakers… or suit, tie, leather shoes… or straw hat plus one sneaker and one leather shoe) without a `Person` class that knows about every garment.

## Frameworks Introduced
- **装饰模式 (Decorator)** — “动态地给一个对象添加一些额外的职责，就增加功能来说，装饰模式比生成子类更为灵活。”[DP]
  - Structure: `Component { +operation() }` (interface for objects that can gain responsibilities dynamically); `ConcreteComponent` (the concrete object being decorated); `Decorator extends Component { -component; +setComponent(); +operation() }` (abstract wrapper: holds a `Component`, forwards `operation()`; `Component` never knows it exists); `ConcreteDecoratorA/B` (call `super.operation()` then add their own state/behaviour).
  - When to use: a class needs extra behaviour only in special cases; the set of add-ons and their order varies; you want to remove decorative logic from the core class ("把类中的装饰功能从类中搬移去除，这样可以简化原有的类").
  - How: (1) define the shared interface; (2) the core class implements it; (3) an abstract decorator implements it, holds a reference to another instance, forwards; (4) each concrete decorator overrides `operation()` as "forward first, then do my extra"; (5) client builds the chain: `d1.setComponent(c); d2.setComponent(d1); d2.operation();`.
  - Why it works: each decorator only knows its own job and the interface, not its position in the chain — "每个装饰对象只关心自己的功能，不需要关心如何被添加到对象链当中"[DPE]. Failure mode: **order matters** (encrypt-then-filter vs filter-then-encrypt); ideally keep decorators independent so any order is valid.
- **Simplification rule** (author's explicit variation): if there is only one `ConcreteComponent` and no abstract `Component`, `Decorator` may subclass `ConcreteComponent` directly; if there is only one `ConcreteDecorator`, merge `Decorator` and `ConcreteDecorator` into one class.
- **简单工厂 + 策略 + 装饰 (combined)** for the 商场收银 program: `ISale` = Component, `CashNormal` = ConcreteComponent, `CashSuper` = Decorator (holds an `ISale`, forwards), `CashRebate` / `CashReturn` = ConcreteDecorators; `CashContext` composes the chain for each promotion.

## Key Concepts
- **Component / ConcreteComponent / Decorator / ConcreteDecorator**: the four roles above.
- **setComponent / decorate**: the wrapping call; the author's version names it `decorate(ICharacter component)`.
- **包装顺序 (wrapping order)**: the last wrapper applied runs first; "先打8折再满300返100" ≠ "先满300返100再打8折".
- **核心职责 vs 装饰功能**: the split the pattern enforces; the core class keeps only its main behaviour.
- **穿衣舞 ("dressing dance")**: the author's name for version-2 code that exposes each step to the client instead of assembling internally.
- **Builder vs Decorator boundary**: builder needs a stable construction process; decorator is for unstable, freely recombinable steps.

## Mental Models
- Think of decorating as putting on clothes: each garment wraps whatever is already there, and you can wear them in any order (superman = underwear outside).
- Use decorator when the question is "which extras, in which order, this time?"; use builder when the steps are fixed.
- Think of `CashNormal` (原价) as the naked person and 打折 / 返利 as garments; new promotions are new combinations, not new classes.
- Prefer wrapping over subclassing when combinations would explode: N features via inheritance → 2^N subclasses; via decoration → N classes.

## Anti-patterns
- **Fat core class** (version 1): `Person` has `wearTShirts()`, `wearSuit()`, … Adding "超人" means editing `Person`: violates open-closed.
- **Inheritance without composition** (version 2): `Finery` subclasses exist but the client calls `dtx.show(); kk.show(); xc.show();` one by one; assembly is exposed and can't be reordered or nested.
- **Combination classes** (`CashReturnRebate`): one class per promotion combo duplicates `CashReturn` and `CashRebate` code and explodes as combos multiply (打折→返利, 返利→打折, 积分, 抽奖…).
- **Order-dependent decorators treated as order-free**: encrypt before word-filtering breaks the filter.

## Code Examples
Textbook decorator (author's names, cleaned):

```java
abstract class Component { public abstract void operation(); }

class ConcreteComponent extends Component {
    public void operation() { System.out.println("具体对象的实际操作"); }
}

abstract class Decorator extends Component {
    protected Component component;
    public void setComponent(Component component) { this.component = component; }
    public void operation() { if (component != null) component.operation(); }   // forward
}

class ConcreteDecoratorA extends Decorator {
    private String addedState;
    public void operation() {
        super.operation();                       // run the wrapped object first
        addedState = "具体装饰对象A的独有操作";  // then this decorator's own work
        System.out.println(addedState);
    }
}
class ConcreteDecoratorB extends Decorator {
    public void operation() { super.operation(); addedBehavior(); }
    private void addedBehavior() { System.out.println("具体装饰对象B的独有操作"); }
}

ConcreteComponent c = new ConcreteComponent();
ConcreteDecoratorA d1 = new ConcreteDecoratorA();
ConcreteDecoratorB d2 = new ConcreteDecoratorB();
d1.setComponent(c);      // d1 wraps c
d2.setComponent(d1);     // d2 wraps d1
d2.operation();          // c → A → B
```
- **What it demonstrates**: the chain is built by the client at run time; each decorator forwards then adds.

Cashier program, three patterns combined:

```java
public interface ISale { double acceptCash(double price, int num); }        // Component

public class CashNormal implements ISale {                                  // ConcreteComponent
    public double acceptCash(double price, int num) { return price * num; }
}

public class CashSuper implements ISale {                                   // Decorator (no longer abstract)
    protected ISale component;
    public void decorate(ISale component) { this.component = component; }
    public double acceptCash(double price, int num) {
        double result = 0d;
        if (component != null) result = component.acceptCash(price, num);   // run wrapped algorithm
        return result;
    }
}

public class CashRebate extends CashSuper {                                 // ConcreteDecorator
    private double moneyRebate = 1d;
    public CashRebate(double moneyRebate) { this.moneyRebate = moneyRebate; }
    public double acceptCash(double price, int num) {
        double result = price * num * moneyRebate;
        return super.acceptCash(result, 1);       // hand result to the next layer
    }
}

public class CashReturn extends CashSuper {                                 // ConcreteDecorator
    private double moneyCondition = 0d, moneyReturn = 0d;
    public CashReturn(double moneyCondition, double moneyReturn) { … }
    public double acceptCash(double price, int num) {
        double result = price * num;
        if (moneyCondition > 0 && result >= moneyCondition)
            result = result - Math.floor(result / moneyCondition) * moneyReturn;
        return super.acceptCash(result, 1);
    }
}

public class CashContext {                                                   // strategy context + simple factory
    private ISale cs;
    public CashContext(int cashType) {
        switch (cashType) {
            case 1: cs = new CashNormal(); break;
            case 5: // 先打8折, 再满300返100
                CashNormal cn = new CashNormal();
                CashReturn cr1 = new CashReturn(300d, 100d);
                CashRebate cr2 = new CashRebate(0.8d);
                cr1.decorate(cn);    // 满300返100 wraps 原价
                cr2.decorate(cr1);   // 打8折 wraps that   → executes 8折 first, then 返利
                cs = cr2; break;
            case 6: // 先满200返50, 再打7折
                CashNormal cn2 = new CashNormal();
                CashRebate cr3 = new CashRebate(0.7d);
                CashReturn cr4 = new CashReturn(200d, 50d);
                cr3.decorate(cn2); cr4.decorate(cr3);
                cs = cr4; break;
        }
    }
    public double getResult(double price, int num) { return cs.acceptCash(price, num); }
}
```
- **What it demonstrates**: no `CashReturnRebate` class is needed; each concrete decorator computes its step and passes the running total (as `price` with `num = 1`) down the chain. Worked numbers: 1000×1 with case 5 → 800 → two 300s → 600. 500×4 with case 6 → 2000 → ten 200s → 1500 → ×0.7 → 1050.

## Worked Example
1. **Version 1**: `Person` has one method per garment plus `show()`. Adding 超人 requires editing `Person` (open-closed violated).
2. **Version 2**: abstract `Finery` with `TShirts`, `BigTrouser`, … subclasses; `Person` only has `show()`. Extension is by subclass, but the client calls each garment's `show()` in sequence and then `xc.show()`: the "穿衣舞" — assembly exposed, no nesting, no control of order.
3. **Not builder**: 小菜 suggests builder; 大鸟 rejects it because the assembly process here is unstable (any garments, any order, even none).
4. **Version 3 (decorator)**: `ICharacter { show() }`; `Person implements ICharacter`; `Finery implements ICharacter` holds an `ICharacter component`, `decorate(component)`, and forwards `show()`; each garment overrides `show()` to print itself then `super.show()`. Client: `pqx.decorate(xc); kk.decorate(pqx); dtx.decorate(kk); dtx.show();`. Adding 草帽 = one new subclass and a new chain.
5. **Transfer to 商场收银**: first attempt adds `CashReturnRebate` (duplicated code, one class per combo). Second attempt introduces `ISale` but forgets a `ConcreteComponent`; 大鸟 points out `CashNormal` is the base algorithm. Final: `CashSuper` becomes the concrete decorator base, `CashRebate` / `CashReturn` end with `super.acceptCash(result, 1)`, and `CashContext` composes chains. Any new promotion sequence changes only `CashContext`.

## Key Takeaways
1. Put each optional feature in its own class implementing the core interface, holding and forwarding to the wrapped object.
2. Concrete decorators follow "forward, then add"; the client assembles the chain, so order and membership are run-time decisions.
3. Decorator strips decorative logic out of the core class and removes duplicated combination code.
4. Wrapping order changes results; keep decorators independent so any order is valid, or document the required order.
5. Collapse roles when the pattern has only one concrete component or one concrete decorator.
6. Use decorator, not builder, when the assembly process is not stable.

## Connects To
- **[ch02](ch02-strategy.md)**: the cashier program's `CashContext` / `CashSuper` family originates as strategy + simple factory; this chapter adds decoration.
- **[ch08](ch08-factory-method.md)**: the tangle of `new` and `decorate` calls inside `CashContext` is cleaned up with factory method.
- **[ch13](ch13-builder.md)**: the boundary case the author draws: builder for stable construction sequences, decorator for free combination.
- **[ch07](ch07-proxy.md)**: proxy has the same "wrapper implements the same interface" shape but controls access instead of adding responsibilities.
- **[ch04](ch04-open-closed.md)**: the running motivation: add garments and promotions by extension, not by editing `Person` or the algorithm classes.
