# 第12章：牛市股票还会亏钱？——外观模式（Facade）

## 核心思想
在一堆子系统类前面放置一个简单的高层接口，让调用者只与一个对象打交道，而不是与许多对象打交道。买基金，让基金经理去应付上千只股票。

## 引入的框架
- **外观模式（Facade），又叫门面模式** — “为子系统中的一组接口提供一个一致的界面，此模式定义了一个高层接口，这个接口使得这一子系统更加容易使用。”[DP]
  - 结构：`Client` → `Facade`（知道哪些子系统类负责处理请求，并把请求委派给它们；`methodA()`、`methodB()`）→ `SubSystemOne..Four`（实现具体工作；**不**持有对 Facade 的引用）。
  - 何时使用——作者给出的三个阶段 [R2P]：
    1. **设计初期**：有意识地划分层次（经典三层架构：在数据访问层与业务逻辑层之间、业务逻辑层与表示层之间各放一个 Facade），使层与层之间的耦合保持在较低水平。
    2. **开发阶段**：随着重构产生越来越多的小类，加入 Facade，使外部调用者不必逐个了解它们。
    3. **维护遗留系统**：把难以修改但又必不可少的遗留系统包在 Facade 里；新代码只与 Facade 交互，由 Facade 去应付遗留系统的混乱。团队分成两组：一组负责 Facade 与遗留系统之间的对接，另一组基于 Facade 的接口开发。
  - 做法：（1）找出子系统类以及客户端真正需要的操作。（2）创建一个类，持有这些子系统对象的引用。（3）暴露粗粒度的方法来编排调用。（4）让客户端只指向 Facade；子系统类不知道它的存在。
  - 为何有效：它是“依赖倒转原则和迪米特法则”在模式中的体现——客户端依赖一个抽象，对子系统的内部一无所知。失败模式：Facade 膨胀成上帝对象，或者在方法签名中泄露子系统的类型。

## 关键概念
- **子系统（subsystem）**：共同实现某项功能的一组类；直接使用时很复杂。
- **高层接口（high-level interface）**：Facade 暴露的粗粒度操作（用 `buyFund()`，而不是四次 `buy()` 调用）。
- **耦合性过高（excessive coupling）**：每个投资者都接触每只股票；在代码中，就是客户端实例化并调用许多子系统类。
- **一致的界面（uniform interface）**：即使子系统各不相同（股票、债券、房地产），Facade 也呈现一个一致的界面。
- **三层架构中的 Facade**：层的边界天然就是 Facade 的位置。
- **遗留系统封装**：封装遗留代码，使其可以被使用但不必被改动。

## 心智模型
- 把 Facade 看作基金：投资者只与一个产品交互，由经理处理投资组合。
- 当调用者否则需要了解多个类*以及*它们的调用顺序时，就使用 Facade。
- 相比「让客户端自己去学习子系统」，更倾向于 Facade，因为它让子系统可以在稳定的界面之后演进。
- Facade 并不禁止直接访问子系统；它只是提供一条简便的路径。高级用户仍然可以绕过它。

## 反模式
- **客户端直接操作所有子系统**（`stock1.buy(); stock2.buy(); nd1.buy(); rt1.buy(); ...`）：客户端与每个具体类以及正确的调用顺序都耦合在一起；增加一个产品就要修改每个客户端。
- **子系统知道 Facade**：结构图写得很明确——子系统类不持有对 Facade 的引用；反向引用会重新引入耦合。
- **没有体系的投机赌博**（大鸟关于炒股的题外话）：随机的盈利只是运气；只有经过验证的框架才能产生可重复的结果。设计也一样——不理解一个模式消除了什么耦合就照搬它，什么也得不到。

## 代码示例
```java
// Subsystem classes (each has buy()/sell())
class Stock1        { public void buy(){ System.out.println("股票1买入"); }  public void sell(){ System.out.println("股票1卖出"); } }
class Stock2        { public void buy(){ System.out.println("股票2买入"); }  public void sell(){ System.out.println("股票2卖出"); } }
class NationalDebt1 { public void buy(){ System.out.println("国债1买入"); }  public void sell(){ System.out.println("国债1卖出"); } }
class Realty1       { public void buy(){ System.out.println("房地产1买入"); } public void sell(){ System.out.println("房地产1卖出"); } }

// Facade
class Fund {
    private Stock1 stock1 = new Stock1();
    private Stock2 stock2 = new Stock2();
    private NationalDebt1 nd1 = new NationalDebt1();
    private Realty1 rt1 = new Realty1();

    public void buyFund()  { stock1.buy();  stock2.buy();  nd1.buy();  rt1.buy();  }
    public void sellFund() { stock1.sell(); stock2.sell(); nd1.sell(); rt1.sell(); }
    // holdings ratios, rebalancing, etc. happen here — the client is never told
}

// Client
Fund fund1 = new Fund();
fund1.buyFund();
fund1.sellFund();
```
- **演示了什么**：客户端对四个类、八次调用的依赖，收缩为对一个对象、两个方法的依赖。

```java
// Generic structure
class Facade {
    private SubSystemOne one = new SubSystemOne();
    private SubSystemTwo two = new SubSystemTwo();
    private SubSystemThree three = new SubSystemThree();
    private SubSystemFour four = new SubSystemFour();

    public void methodA() { one.methodOne(); two.methodTwo(); three.methodThree(); four.methodFour(); }
    public void methodB() { two.methodTwo(); three.methodThree(); }
}
Facade facade = new Facade();
facade.methodA();   // client need not know the subsystems exist
facade.methodB();
```
- **演示了什么**：Facade 的方法可以组合不同子集的子系统调用。

## 实战示例
**朴素版本（股民炒股）：** 每个投资者各自实例化 `Stock1`、`Stock2`、`NationalDebt1`、`Realty1`，并对每个对象调用 `buy()`/`sell()`。一位同事顾韵梅总是买入刚涨过的股票，卖出即将上涨的股票；用代码的话来说，就是客户端在做基金经理的工作，却没有任何专业知识，而且每个客户端都重复了这套编排。

**哪里出了问题：** 耦合。投资者与许多具体的投资品种绑在一起；增加一个产品或改变配置规则，就要修改每一个投资者。

**重构后（投资基金）：** 引入持有这些投资品种的 `Fund`；暴露 `buyFund()` / `sellFund()`。客户端现在只持有一个引用。配置、时机和再平衡都成为 `Fund` 的职责，可以在不改动客户端的情况下变化。小菜在这个模式还没被命名之前，就立刻认出这是外观模式的基本形态。

**一般化：** 把投资品种换成 `SubSystemOne..Four`，把 `Fund` 换成 `Facade`，并记住结构图中的规则：子系统从不引用 Facade。

## 关键要点
1. 当客户端必须按特定顺序调用多个类时，把这套编排封装进一个 Facade 方法。
2. 尽早在层的边界处插入 Facade；这是让三层架构保持解耦的最廉价办法。
3. 大量重构产生许多小类之后，Facade 能在不撤销重构的前提下恢复可用性。
4. 用 Facade 包装遗留系统，并针对 Facade 而不是遗留代码来构建新功能。
5. 让子系统类不知道 Facade 的存在；依赖只朝一个方向。

## 关联章节
- **[ch11](ch11-law-of-demeter.md)**：Facade 是最少知识原则在结构上的实现——客户端只认识一个类。
- **[ch05](ch05-dependency-inversion.md)**：客户端依赖高层接口，而不是具体的子系统细节。
- **[ch25](ch25-mediator.md)**：中介者模式（Mediator）同样集中交互，但针对的是会相互回应的对等方；外观模式是单向的。
- **[ch17](ch17-adapter.md)**：适配器模式（Adapter）把一个接口改成另一个接口；外观模式把多个接口简化为一个。
- **[ch29](ch29-pattern-summary.md)**：外观模式因其清晰和无处不在，是模式大赛的决赛选手。
