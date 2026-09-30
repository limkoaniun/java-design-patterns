# Chapter 8: 工厂制造细节无须知——工厂方法模式 — Factory Method

## Core Idea
A simple factory's `switch` knows every product, so every new product edits it. Factory method abstracts the factory itself: the client depends on an `IFactory` interface, and each concrete factory decides which product to instantiate. "实例化的过程延迟到了工厂子类中" — the mature factory and product families stay untouched; growth happens in new factories.

## Frameworks Introduced
- **工厂方法模式 (Factory Method)** — “定义一个用于创建对象的接口，让子类决定实例化哪一个类。工厂方法使一个类的实例化延迟到其子类。”[DP]
  - Structure: `Product` (interface of the objects the factory method creates); `ConcreteProduct` (implements `Product`); `Creator { +factoryMethod() : Product }` (declares the factory method); `ConcreteCreator` (overrides `factoryMethod()` to return a `ConcreteProduct`).
  - When to use: a simple factory's branching class has become a "bad smell" (承载了太多功能); you must add products without touching a stable product/factory set; you want to hide complex construction (e.g. decorator chains) from the caller.
  - How: (1) keep the product hierarchy; (2) extract `IFactory { Product create…() }` per 依赖倒转原则; (3) one concrete factory per product family (not necessarily per product); (4) client codes against `IFactory` only.
  - Why it works: polymorphism replaces the branch: the client asks a factory, and which product appears is decided by which factory it holds. "工厂方法模式是简单工厂模式的进一步抽象和推广… 保持了简单工厂模式的优点，而且克服了它的缺点。" Failure mode: one factory per product for a handful of trivially-constructed products just multiplies classes (小菜's first objection); group products into factories by family instead.
- **Author's rule of thumb**: "当只有一个工厂时，就是简单工厂模式，当有多个工厂时，就是工厂方法模式。类似由一维进化成了二维。"
- **Two stated benefits of factory method**: (1) shields the caller from complex construction of a new instance (e.g. the decorator wiring for "先打折再满减"); (2) decoupling: modifying the implementation layer does not affect the upper layer because it only sees the interface.
- **简单工厂 + 策略 + 装饰 + 工厂方法** (商场收银 v4): `IFactory { ISale createSalesModel() }`; `CashRebateReturnFactory` and `CashReturnRebateFactory` build the decorator chains; `CashContext` picks a factory and calls `createSalesModel()`, knowing nothing of `CashNormal`/`CashRebate`/`CashReturn`.

## Key Concepts
- **简单工厂 (Simple Factory)**: one class with a `switch` that instantiates the right product; open to extension *and* to modification.
- **IFactory / Creator**: the factory interface; the only thing the client depends on.
- **ConcreteCreator**: `AddFactory`, `FactoryBasic`, `FactoryAdvanced`, `CashRebateReturnFactory`… each returns its family's products.
- **延迟到子类 (deferred to subclasses)**: the definition's key phrase: the abstract creator doesn't instantiate; concrete creators do.
- **产品族 by factory**: group 加减乘除 in 基础运算工厂, 指数/对数 in 高级运算工厂; new factories don't disturb old ones.
- **参数归并 (parameter folding)**: 原价 = rebate 1.0; 满减 = rebate 1.0 with condition; so five promotion variants collapse into two factories with (rebate, condition, return) parameters.

## Mental Models
- Think of a company opening a second plant for new products: the new plant must not disturb the old one; head office just adds a coordinating department (the top-level factory selector).
- Use "针对接口编程" on the factory itself: if the client references a concrete factory class, you still have a simple factory in disguise.
- Think "eggs in one basket": a single switch that creates everything means every product change risks every other product.
- Prefer factories that hide *how* an object is assembled (decorator chains, multi-step setup) — that is where factory method pays off most.

## Anti-patterns
- **Growing the simple factory's switch**: adding `pow` means editing `OperationFactory`: mature code modified for each extension, violating open-closed.
- **One factory per trivial product**: `AddFactory`, `SubFactory`, … for four one-line constructors adds classes without reducing risk (the chapter's straw-man version).
- **Factory selector that still `new`s products**: the intermediate `OperationFactory` that switches over factories still has a smell: adding a family edits it; the author defers the fix (reflection, [ch15](ch15-abstract-factory.md)).
- **`CashContext` full of `new` and `decorate` calls**: cases 5 and 6 in the decorator version expose the whole wiring in the context class.

## Code Examples
Calculator, factory-method form by family:

```java
public interface IFactory { Operation createOperation(String operType); }

public class FactoryBasic implements IFactory {          // 加减乘除: stable, don't touch
    public Operation createOperation(String operType) {
        Operation oper = null;
        switch (operType) {
            case "+": oper = new Add(); break;
            case "-": oper = new Sub(); break;
            case "*": oper = new Mul(); break;
            case "/": oper = new Div(); break;
        }
        return oper;
    }
}

public class FactoryAdvanced implements IFactory {       // 指数/对数: may grow further
    public Operation createOperation(String operType) {
        Operation oper = null;
        switch (operType) {
            case "pow": oper = new Pow(); break;
            case "log": oper = new Log(); break;
            // add sin/cos/tan here without touching FactoryBasic
        }
        return oper;
    }
}

public class Pow extends Operation {
    public double getResult(double a, double b) { return Math.pow(a, b); }
}
public class Log extends Operation {
    public double getResult(double a, double b) { return Math.log(b) / Math.log(a); }
}

public class OperationFactory {                           // selector: no product `new` left
    public static Operation createOperate(String operate) {
        IFactory factory = null;
        switch (operate) {
            case "+": case "-": case "*": case "/": factory = new FactoryBasic(); break;
            case "pow": case "log":                 factory = new FactoryAdvanced(); break;
        }
        return factory.createOperation(operate);          // polymorphism returns the real product
    }
}
```
- **What it demonstrates**: the selector holds only interfaces and factories; product instantiation moved into concrete factories, one per family.

Cashier program, v4 (factory method hides the decorator wiring):

```java
public interface IFactory { ISale createSalesModel(); }

// 先打x折, 再满m返n
public class CashRebateReturnFactory implements IFactory {
    private double moneyRebate = 1d, moneyCondition = 0d, moneyReturn = 0d;
    public CashRebateReturnFactory(double moneyRebate, double moneyCondition, double moneyReturn) { … }
    public ISale createSalesModel() {
        CashNormal cn  = new CashNormal();
        CashReturn cr1 = new CashReturn(moneyCondition, moneyReturn);
        CashRebate cr2 = new CashRebate(moneyRebate);
        cr1.decorate(cn);      // 满m返n wraps 原价
        cr2.decorate(cr1);     // 打x折 wraps that
        return cr2;
    }
}
// CashReturnRebateFactory is the mirror image: rebate wraps 原价, return wraps rebate.

public class CashContext {
    private ISale cs;
    public CashContext(int cashType) {
        IFactory fs = null;
        switch (cashType) {
            case 1: fs = new CashRebateReturnFactory(1d,   0d,   0d);   break; // 原价
            case 2: fs = new CashRebateReturnFactory(0.8d, 0d,   0d);   break; // 打8折
            case 3: fs = new CashRebateReturnFactory(0.7d, 0d,   0d);   break; // 打7折
            case 4: fs = new CashRebateReturnFactory(1d,   300d, 100d); break; // 满300返100
            case 5: fs = new CashRebateReturnFactory(0.8d, 300d, 100d); break; // 先8折再满300返100
            case 6: fs = new CashReturnRebateFactory(0.7d, 200d, 50d);  break; // 先满200返50再7折
        }
        cs = fs.createSalesModel();
    }
    public double getResult(double price, int num) { return cs.acceptCash(price, num); }
}
```
- **What it demonstrates**: `CashContext` programs against `ISale` and `IFactory` only; the decorator assembly is encapsulated; five promotion variants fold into two parameterised factories.

## Reference Tables
| | 简单工厂 (Simple Factory) | 工厂方法 (Factory Method) |
|---|---|---|
| Who chooses the class | One factory's `switch` | Which concrete factory the client holds (polymorphism) |
| Adding a product | Add product class **and** edit the factory switch | Add product class and a new/extended factory; old factories untouched |
| Open-closed | Open to extension, also open to modification | Extension only, for the stable families |
| Client dependency | Concrete factory class | `IFactory` interface |
| Class count | Fewest | More (one factory per family) |
| Author's summary | "一维" — one factory | "二维" — many factories; "简单工厂模式的进一步抽象和推广" |
| Residual smell | Switch grows forever | Top-level selector still branches (fix later with reflection) |

## Worked Example
1. **Simple factory (from ch01)**: `OperationFactory.createOperate("+")` switches over `Add/Sub/Mul/Div`. Client is decoupled from products, but adding `pow` edits this stable class.
2. **First factory-method attempt**: `IFactory { createOperation() }` with `AddFactory`, `SubFactory`, `MulFactory`, `DivFactory`. 小菜 objects: 5 classes became 10 and the problem isn't solved.
3. **Re-think by family**: 大鸟's second-plant analogy. Keep 加减乘除 in `FactoryBasic` (mature, sealed); put `Pow`, `Log` in `FactoryAdvanced` (may grow). `OperationFactory` now only chooses a factory and calls `createOperation` — no product `new` inside.
4. **Why**: DIP applied to creation. The client and selector depend on `IFactory`; each family is isolated; future 正余弦 go into `FactoryAdvanced` without risk to the basic family. Remaining smell (selector branch) acknowledged, deferred to reflection.
5. **Transfer to 商场收银**: the decorator-era `CashContext` has messy `new`/`decorate` chains in cases 5–6. Fold the five variants: 原价 = rebate 1.0; 满减 = rebate 1.0 + condition; so two factories suffice: `CashRebateReturnFactory` and `CashReturnRebateFactory`, each parameterised by (折扣, 满减条件, 返利). `CashContext` becomes a table of factory constructions.

## Key Takeaways
1. Factory method = a factory interface plus concrete factories that defer instantiation; the client depends only on the interface.
2. Group products into factories by family; don't reflexively create one factory per product.
3. Use factory method to seal mature product/factory sets and put new growth in new factories.
4. Its biggest practical win is hiding complicated construction (decorator chains, multi-parameter setup) from the caller.
5. Look for parameters that let variant classes collapse into one parameterised factory (rebate 1.0 = no discount).
6. A top-level factory selector with a `switch` is a leftover smell; reflection or configuration removes it later.

## Connects To
- **[ch01](ch01-simple-factory.md)**: the simple factory this chapter upgrades.
- **[ch05](ch05-dependency-inversion.md)**: extracting `IFactory` is the dependency-inversion move.
- **[ch06](ch06-decorator.md)**: the decorator chains that `CashRebateReturnFactory` now encapsulates.
- **[ch15](ch15-abstract-factory.md)**: abstract factory generalises to families of related products and introduces reflection to kill the remaining `switch`.
- **[ch29](ch29-pattern-summary.md)**: 工厂方法 wins the creational-group round because adding products needs no change to the existing product system or factory classes.
