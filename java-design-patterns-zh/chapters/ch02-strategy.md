# 第2章：商场促销——策略模式（Store Promotions: Strategy）

## 核心思想
折扣、返利和"满300返100"都是同一项工作（计算应付金额）的可互换算法。策略模式（Strategy）把每个算法封装在各自的类中，放在一个共同父类之下，并向客户端提供一个 Context（上下文），这样算法可以被替换、新增和单元测试，而客户端无需改动。"策略模式封装了变化"，再结合简单工厂模式（Simple Factory），客户端只需认识一个类。

## 引入的框架
- **策略模式（Strategy）** — “它定义了算法家族，分别封装起来，让它们之间可以互相替换，此模式让算法的变化，不会影响到使用算法的客户。”[DP]
  - 结构：`Strategy`（抽象类，`algorithmInterface()`）← `ConcreteStrategyA/B/C`；`Context` 持有一个 `Strategy` 引用，并暴露 `contextInterface()` 委托给它。
  - 适用场景：多个算法做同一件事但实现不同，并在运行时互相替换；作者把它扩展到「几乎任何类型的规则」：“只要在分析过程中听到需要在不同时间应用不同的业务规则，就可以考虑使用策略模式处理这种变化的可能性”[DPE]。
  - 做法：(1) 带有该操作的抽象策略；(2) 每个算法一个具体类，参数化而非每个*值*一个类（一个 `CashRebate(0.8)`，而不是 `Rebate80`、`Rebate70`）；(3) 以策略构造的 Context，负责委托；(4) 客户端实例化 Context 并调用它。
- **策略 + 简单工厂结合（Strategy combined with Simple Factory）** — 工厂的 `switch` 移入 `CashContext(int cashType)` 内部。客户端从认识两个类（`CashSuper`、`CashFactory`）变为只认识一个（`CashContext`）；连策略父类也被隐藏了。
- **类的划分基础是抽象（Classes are drawn by abstraction, not by count）** — “面向对象的编程，并不是类越多越好……打一折和打九折只是形式的不同，抽象分析出来，所有的打折算法都是一样的，所以打折算法应该是一个类。”

## 关键概念
- **算法家族（Algorithm family）**：一组可互相替换的计算（正常收费、打折、返利）。
- **Context（上下文）**：配置了策略、客户端实际与之交互的对象。
- **变化点（Variation point）**：会变化的东西（这里是计价规则）；面向对象的核心做法就是封装它。
- **CashSuper / CashNormal / CashRebate / CashReturn**：书中的策略层次结构；`acceptCash(price, num)` 就是算法。
- **反射（Reflection）**：作为去除最后一个 `switch` 的方法被预先提及（见 ch15）。

## 心智模型
- **当你听到「不同时间应用不同规则」时，使用策略模式。** 计价、税费、运费、评分：任何规则家族。
- **把策略模式看作简单工厂模式的兄弟，只是提的问题不同。** 工厂回答「用哪个对象？」；策略模式回答「用哪个可随意替换的算法？」。作者展示了同样的四个类可以同时服务于两者，只有面向客户端的形态不同。
- **对于数值，优先用参数而非子类。** 八折和七折是同一个带构造参数的类；"满300返100"和"满500返200"是同一个带两个参数的类。
- **把选择逻辑移出客户端。** 基本的策略模式把 `switch` 留在客户端；结合工厂后把它推入 Context；反射（后文）则将其删除。

## 反模式
- **硬编码折扣**（`totalPrices * 0.8`）：促销结束后，每台收银机都要重新部署。
- **在界面中为每个促销写一个 `switch`**：三个分支的主体只差一个常量；既重复，客户端又不断膨胀。
- **每个折扣值一个子类**（`Rebate80`、`Rebate70`、`Rebate50` ……）：混淆了形式与本质；抽象是「打折」，数值只是数据。
- **客户端仍带 `switch` 的基本策略模式**：“不又回到了原来的老路了吗”；客户端依然在做决定。应把选择逻辑并入 Context。
- **对多变的规则只用简单工厂模式**：每次促销变更都要修改、重新编译并重新部署工厂：“这真的是很糟糕的处理方式”。

## 代码示例
策略家族（与简单工厂模式版本相比没有变化）以及结合后的 Context：

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
- **演示内容**：`CashSuper` 及其子类在工厂版本与策略版本之间没有变化；变化的只是面向客户端的对象。客户端再也看不到 `CashSuper`。

## 参考表
| | 简单工厂 | 策略（基本） | 策略 + 简单工厂 |
|---|---|---|---|
| 客户端需要认识 | `CashSuper`, `CashFactory` | `CashSuper`, `CashContext`, 所有具体策略 | 仅 `CashContext` |
| `switch` 所在位置 | 工厂 | 客户端 | Context 构造函数 |
| 客户端调用 | `CashFactory.createCashAccept(n).acceptCash(p, q)` | `new CashContext(new CashRebate(0.8)).getResult(p, q)` | `new CashContext(n).getResult(p, q)` |
| 新增规则 | 新增子类 + 工厂分支 | 新增子类 + 客户端分支 | 新增子类 + Context 分支 |
| 耦合 | 中 | 高（由客户端选择） | 三者中最低 |

## 实战示例
任务：做一个商场收银程序，输入单价和数量，计算账单总额。

**v1.0**：在 `do/while` 循环中 `totalPrices = price * num`。大鸟：现在全场打八折。

**v1.1**：加一个 `discount` 选择器和一个带 `* 0.8`、`* 0.7` 的 `switch`。有所改善，但三个分支几乎一样，而且商场现在又想要满300返100。

**简单工厂模式（经由 ch01）**：小菜提议每种促销一个子类。大鸟：要几个？"要几个写几个"是不对的。抽象找出两种形态：打折（一个参数）和返利（两个参数）。结果：`CashSuper` ← `CashNormal`、`CashRebate(rate)`、`CashReturn(condition, amount)`；`CashFactory.createCashAccept(int)`。新增满100积分10点 = 一个子类加一个分支。结论：解决了创建问题，但促销经常变化，而每次变更都要重新编译工厂。

**策略模式（v1.2）**：小菜自己发现了这个模式。现有的类原封不动；新增 `CashContext(CashSuper)` 和 `getResult`。现在由客户端的 `switch` 选择传入哪个策略。小菜：我们不是把问题又推回客户端了吗？

**策略模式 + 工厂**：“难道简单工厂就一定要是一个单独的类吗？” 把 `switch` 移入 `CashContext(int cashType)`。客户端：`new CashContext(discount).getResult(price, num)`。耦合下降：客户端从此不知道 `CashSuper` 的存在。

**遗留缺陷**：新增满200送50仍然要修改 `CashContext` 中的 `switch`。"任何需求的变更都是需要成本的"，但高手会把成本降到最低；反射（ch15）将彻底去掉这个分支。

为什么有效：*算法家族*的形态是稳定的（单价、数量 → 金额），而它的*成员*却不断变动。策略模式固定形态，让成员自由变化。

## 关键要点
1. 当同一项工作有多个可互相替换的算法时，让每个算法各占一个类，放在同一个抽象父类之下。
2. 策略模式明确的好处：可复用的算法层次结构、更易于单元测试（每个算法单独测试），以及消除客户端中的条件语句 [DP][DPE]。
3. 把变体参数化；不要为每个常量创建一个类。
4. 把选择逻辑并入 Context，使客户端恰好只依赖一个类。
5. 策略模式可以从算法推广到任何随时间变化的业务规则。
6. 随每条新规则增长的 `switch`，只是一笔被你转移、而非消除的成本。

## 关联章节
- **[ch01](ch01-simple-factory.md)**：同样的类层次结构；作者把两种客户端形态并排对比。
- **[ch04](ch04-open-closed.md)**：`CashContext` 中残留的 `switch` 正是开放-封闭原则（OCP）所反对的。
- **[ch06](ch06-decorator.md)** 和 **[ch08](ch08-factory-method.md)**：收银系统再次升级，使用装饰模式（Decorator，可叠加的促销）和工厂方法模式（Factory Method）。
- **[ch15](ch15-abstract-factory.md)**：反射 + 配置去掉最后一个 `switch`。
- **[ch29](ch29-pattern-summary.md)**：策略模式入选最终名单；作者自己的表述是「对可互换的行为采用合成/聚合复用原则（CARP）」。
