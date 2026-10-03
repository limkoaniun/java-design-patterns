# 第8章：工厂制造细节无须知——工厂方法模式（Factory Method）

## 核心思想
简单工厂模式（Simple Factory）的 `switch` 认识每一种产品，因此每新增一个产品都要修改它。工厂方法模式（Factory Method）把工厂本身抽象出来：客户端依赖 `IFactory` 接口，由各个具体工厂决定实例化哪个产品。"实例化的过程延迟到了工厂子类中"——成熟的工厂与产品族保持不动，增长发生在新增的工厂里。

## 引入的框架
- **工厂方法模式（Factory Method）** — “定义一个用于创建对象的接口，让子类决定实例化哪一个类。工厂方法使一个类的实例化延迟到其子类。”[DP]
  - 结构：`Product`（工厂方法所创建对象的接口）；`ConcreteProduct`（实现 `Product`）；`Creator { +factoryMethod() : Product }`（声明工厂方法）；`ConcreteCreator`（重写 `factoryMethod()` 以返回一个 `ConcreteProduct`）。
  - 适用时机：简单工厂模式的分支类已成为「坏味道」（承载了太多功能）；需要在不改动稳定的产品/工厂集合的前提下新增产品；想对调用者隐藏复杂的构造过程（例如装饰链）。
  - 做法：(1) 保留产品层次；(2) 依据依赖倒转原则（Dependency Inversion）提取 `IFactory { Product create…() }`；(3) 每个产品族一个具体工厂（不一定每个产品一个）；(4) 客户端只针对 `IFactory` 编程。
  - 为什么有效：多态取代了分支：客户端向工厂提出请求，出现哪种产品取决于它持有哪个工厂。"工厂方法模式是简单工厂模式的进一步抽象和推广… 保持了简单工厂模式的优点，而且克服了它的缺点。" 失效模式：为少数几个构造很简单的产品各建一个工厂，只会让类的数量成倍增加（小菜的第一个反对意见）；应改为按产品族把产品归入工厂。
- **作者的经验法则**："当只有一个工厂时，就是简单工厂模式，当有多个工厂时，就是工厂方法模式。类似由一维进化成了二维。"
- **工厂方法模式的两点好处**：(1) 让调用者免于面对新实例的复杂构造（例如「先打折再满减」的装饰装配）；(2) 解耦：修改实现层不会影响上层，因为上层只看得到接口。
- **简单工厂 + 策略 + 装饰 + 工厂方法**（商场收银 v4）：`IFactory { ISale createSalesModel() }`；`CashRebateReturnFactory` 与 `CashReturnRebateFactory` 负责构建装饰链；`CashContext` 选择一个工厂并调用 `createSalesModel()`，对 `CashNormal`/`CashRebate`/`CashReturn` 一无所知。

## 关键概念
- **简单工厂模式（Simple Factory）**：一个带 `switch` 的类，用它实例化正确的产品；对扩展开放，*同时*对修改也开放。
- **IFactory / Creator**：工厂接口；客户端唯一依赖的东西。
- **ConcreteCreator**：`AddFactory`、`FactoryBasic`、`FactoryAdvanced`、`CashRebateReturnFactory`……各自返回所属产品族的产品。
- **延迟到子类（deferred to subclasses）**：定义中的关键短语：抽象的创建者不做实例化，具体的创建者来做。
- **按工厂划分的产品族**：把加减乘除归入基础运算工厂，把指数/对数归入高级运算工厂；新增工厂不会干扰旧工厂。
- **参数归并（parameter folding）**：原价 = 折扣 1.0；满减 = 带条件的折扣 1.0；于是五种促销变体可以归并为两个工厂，参数为（折扣、条件、返利）。

## 心智模型
- 设想一家公司为新产品开设第二座工厂：新工厂不能干扰旧工厂；总部只需增设一个协调部门（顶层的工厂选择器）。
- 对工厂本身运用"针对接口编程"：如果客户端引用的是具体的工厂类，那你得到的仍然是一个伪装起来的简单工厂模式。
- 想想「鸡蛋不要放在同一个篮子里」：一个创建一切的 `switch`，意味着任何产品的改动都会危及其他所有产品。
- 优先选择那些隐藏对象*如何*装配（装饰链、多步骤初始化）的工厂——这正是工厂方法模式回报最大的地方。

## 反模式
- **不断膨胀的简单工厂模式 switch**：新增 `pow` 意味着要修改 `OperationFactory`：每次扩展都要改动成熟代码，违反开放-封闭原则（Open-Closed）。
- **每个琐碎产品一个工厂**：为四个只有一行的构造器建 `AddFactory`、`SubFactory` 等，只增加了类，并没有降低风险（本章的稻草人版本）。
- **仍然 `new` 产品的工厂选择器**：在各工厂之间做 switch 的中间层 `OperationFactory` 仍有坏味道：新增一个产品族就要改它；作者把修复推迟了（反射，[ch15](ch15-abstract-factory.md)）。
- **充斥 `new` 与 `decorate` 调用的 `CashContext`**：装饰版本中的情形 5 和 6 把全部装配过程暴露在上下文类里。

## 代码示例
计算器，按产品族划分的工厂方法形式：

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
- **展示了什么**：选择器只持有接口和工厂；产品的实例化已移入具体工厂，每个产品族一个。

收银程序 v4（工厂方法隐藏装饰装配）：

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
- **展示了什么**：`CashContext` 只针对 `ISale` 和 `IFactory` 编程；装饰的装配被封装起来；五种促销变体归并为两个参数化的工厂。

## 参考表
| | 简单工厂（Simple Factory） | 工厂方法（Factory Method） |
|---|---|---|
| 谁来选择类 | 一个工厂的 `switch` | 客户端持有哪个具体工厂（多态） |
| 新增产品 | 新增产品类，**并且**修改工厂的 switch | 新增产品类，并新增/扩展一个工厂；旧工厂不动 |
| 开放-封闭 | 对扩展开放，对修改也开放 | 对稳定的产品族而言，只扩展 |
| 客户端依赖 | 具体的工厂类 | `IFactory` 接口 |
| 类的数量 | 最少 | 更多（每个产品族一个工厂） |
| 作者的总结 | "一维"——一个工厂 | "二维"——多个工厂；"简单工厂模式的进一步抽象和推广" |
| 残留的坏味道 | switch 无止境地膨胀 | 顶层选择器仍有分支（之后用反射修复） |

## 实战示例
1. **简单工厂模式（来自 ch01）**：`OperationFactory.createOperate("+")` 在 `Add/Sub/Mul/Div` 之间做 switch。客户端与产品解耦，但新增 `pow` 要修改这个稳定的类。
2. **第一次工厂方法尝试**：`IFactory { createOperation() }`，配上 `AddFactory`、`SubFactory`、`MulFactory`、`DivFactory`。小菜反对：5 个类变成了 10 个，问题并没有解决。
3. **按产品族重新思考**：大鸟的第二座工厂类比。把加减乘除留在 `FactoryBasic`（成熟、封存）；把 `Pow`、`Log` 放进 `FactoryAdvanced`（可能继续增长）。`OperationFactory` 现在只选择工厂并调用 `createOperation`——内部不再有产品的 `new`。
4. **原因**：把依赖倒转原则应用到创建过程。客户端与选择器依赖 `IFactory`；各产品族相互隔离；将来的正余弦放进 `FactoryAdvanced`，对基础产品族没有风险。残留的坏味道（选择器分支）已被承认，并推迟到反射阶段解决。
5. **迁移到商场收银**：装饰时代的 `CashContext` 在情形 5–6 中有杂乱的 `new`/`decorate` 链。归并这五种变体：原价 = 折扣 1.0；满减 = 折扣 1.0 + 条件；于是两个工厂就够了：`CashRebateReturnFactory` 与 `CashReturnRebateFactory`，各自以（折扣, 满减条件, 返利）为参数。`CashContext` 变成一张工厂构造表。

## 关键要点
1. 工厂方法模式 = 一个工厂接口加若干延迟实例化的具体工厂；客户端只依赖接口。
2. 按产品族把产品归入工厂；不要条件反射式地为每个产品各建一个工厂。
3. 用工厂方法模式封存成熟的产品/工厂集合，把新的增长放进新的工厂。
4. 它最大的实际收益，是对调用者隐藏复杂的构造过程（装饰链、多参数初始化）。
5. 寻找能让变体类归并为一个参数化工厂的参数（折扣 1.0 = 不打折）。
6. 带 `switch` 的顶层工厂选择器是遗留的坏味道；之后可用反射或配置将其消除。

## 关联章节
- **[ch01](ch01-simple-factory.md)**：本章所升级的简单工厂模式。
- **[ch05](ch05-dependency-inversion.md)**：提取 `IFactory` 就是依赖倒转的做法。
- **[ch06](ch06-decorator.md)**：`CashRebateReturnFactory` 现在所封装的装饰链。
- **[ch15](ch15-abstract-factory.md)**：抽象工厂模式（Abstract Factory）推广到相关产品的产品族，并引入反射来消除残留的 `switch`。
- **[ch29](ch29-pattern-summary.md)**：工厂方法在创建型分组的比赛中胜出，因为新增产品无需改动现有的产品体系或工厂类。
