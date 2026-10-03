# 第16章：无尽加班何时休——状态模式（State）

## 核心思想
当对象的行为取决于它的状态，而状态转移逻辑已经变成一长串 `if/else` 时，把每个状态放进各自的类，让这些状态彼此交接控制权。「Long Method」坏味道是触发信号，该模式是解药。

## 引入的框架
- **状态模式（State）** — “当一个对象的内在状态改变时允许改变其行为，这个对象看起来像是改变了其类。”[DP]
  - 结构：`Context`（持有 `state`，暴露 `request()`，其内部调用 `state.handle(this)`）↔ `State`（抽象的 `handle(Context)`）← `ConcreteStateA`、`ConcreteStateB`（各自实现一个状态的行为，并在上下文上设置*下一个*状态）。
  - 适用场景："当一个对象的行为取决于它的状态，并且它必须在运行时刻根据状态改变它的行为时"；或者业务对象有若干枚举状态，且由庞大的多分支条件语句驱动时。
  - 做法：(1) 找出充满状态判断的 `Long Method`；(2) 建立抽象的 `State`，其行为方法接收上下文；(3) 每个状态一个子类，各自要么完成工作，要么把上下文切换到下一个状态并重新分派；(4) `Context` 持有 `current`，负责委托，并暴露各状态需要的数据（`hour`、`workFinished`）。
- **Long Method 坏味道** — Martin Fowler 在《重构》中提出的坏味道；一个分支众多的长方法"责任过大"，同时违反单一职责原则（SRP）和开放-封闭原则（OCP）。

## 关键概念
- **State（抽象状态类）**："定义一个接口以封装与Context的一个特定状态相关的行为"。
- **ConcreteState（具体状态）**："每一个子类实现一个与Context的一个状态相关的行为"。
- **Context**："维护一个ConcreteState子类的实例，这个实例定义当前的状态"。
- **状态转移逻辑分布（distributed transition logic）**：每个 ConcreteState 自己决定它的后继状态，因此没有任何单一位置了解整个状态机。
- **行为局部化（localised behaviour）**："将与特定状态相关的行为局部化，并且将不同状态的行为分割开来"[DP]。
- **活字 vs 刻版**：作者反复使用的比喻——庞大的 `if` 块是雕好的印版，状态类则是活字。
- **转移后重新分派**：`w.setState(new NoonState()); w.writeProgram();` ——新状态立即处理同一个请求。

## 心智模型
- 把每个状态类看作**状态表中的一行**，同时负责「我做什么」和「何时交接」。
- 当*同一个*方法调用必须随时间表现出不同行为时，用状态模式；当*调用方*预先选定算法时，用策略模式（Strategy）。
- 如果状态判断只是一个简单的 `if`，就不要用这个模式："如果这个状态判断很简单，那就没必要用状态模式了"。
- 问一句「规则变化时哪些行会变？」——用状态模式，答案是一个类，而不是一个庞大的方法。

## 反模式
- **面向过程的初稿**：静态的 `hour`/`workFinished` 全局变量加一个静态的 `writeProgram()`——根本没有对象。
- **一个类，一个庞大的方法**：`Work.writeProgram()` 里嵌套 `if (hour < 12) … else if … else { if (workFinished) … }`——每次规则变化都要改整个方法，并可能破坏不相关的分支。
- **用再加一个分支来编码新规则**：「必须在 20:00 前离开」这条需求应当只触及晚间状态，而不是处理所有时段的那个方法。
- **对只有两个分支的条件使用状态模式**：过度设计；只有条件复杂时，这个模式才值回它的成本。

## 代码示例
通用结构：
```java
abstract class State { public abstract void handle(Context context); }

class ConcreteStateA extends State {
    public void handle(Context context) { context.setState(new ConcreteStateB()); }
}
class ConcreteStateB extends State {
    public void handle(Context context) { context.setState(new ConcreteStateA()); }
}

class Context {
    private State state;
    public Context(State state) { this.state = state; }
    public void setState(State value) {
        this.state = value;
        System.out.println("当前状态:" + this.state.getClass().getName());
    }
    public void request() { this.state.handle(this); }
}

Context c = new Context(new ConcreteStateA());
c.request(); c.request(); c.request();   // A→B→A→B
```
- **演示内容**：上下文从不做分支判断；每个状态自己指明后继状态。

加班程序的状态模式版本：
```java
abstract class State { public abstract void writeProgram(Work w); }

class ForenoonState extends State {
    public void writeProgram(Work w) {
        if (w.getHour() < 12) System.out.println("当前时间: " + w.getHour() + "点 上午工作，精神百倍");
        else { w.setState(new NoonState()); w.writeProgram(); }   // hand off and re-dispatch
    }
}
class NoonState extends State {      // < 13: 犯困；else → AfternoonState
    public void writeProgram(Work w) {
        if (w.getHour() < 13) System.out.println("当前时间: " + w.getHour() + "点 饿了，午饭；犯困，午休。");
        else { w.setState(new AfternoonState()); w.writeProgram(); }
    }
}
class AfternoonState extends State { // < 17: 状态不错；else → EveningState
    public void writeProgram(Work w) {
        if (w.getHour() < 17) System.out.println("当前时间: " + w.getHour() + "点 下午状态还不错，继续努力");
        else { w.setState(new EveningState()); w.writeProgram(); }
    }
}
class EveningState extends State {
    public void writeProgram(Work w) {
        if (w.getWorkFinished()) { w.setState(new RestState()); w.writeProgram(); }
        else if (w.getHour() < 21) System.out.println("当前时间: " + w.getHour() + "点 加班哦，疲累之极");
        else { w.setState(new SleepingState()); w.writeProgram(); }
    }
}
class SleepingState extends State { public void writeProgram(Work w) { System.out.println("当前时间: " + w.getHour() + "点 不行了，睡着了。"); } }
class RestState     extends State { public void writeProgram(Work w) { System.out.println("当前时间: " + w.getHour() + "点 下班回家了"); } }

class Work {
    private State current = new ForenoonState();
    private int hour; private boolean workFinished = false;
    public void setState(State value) { this.current = value; }
    public void writeProgram() { this.current.writeProgram(this); }
    // getHour/setHour, getWorkFinished/setWorkFinished omitted
}

Work emergencyProjects = new Work();
emergencyProjects.setHour(9);  emergencyProjects.writeProgram();
emergencyProjects.setHour(17); emergencyProjects.setWorkFinished(false); emergencyProjects.writeProgram();
emergencyProjects.setHour(22); emergencyProjects.writeProgram();
```
- **演示内容**：客户端代码与多分支版本相比没有变化，但每条规则都落在一个小类里。

## 实战示例
小菜描述了他的一天：早上精神百倍，中午犯困，下午恢复，加班时疲惫不堪，除非任务完成，否则 21:00 之后就睡着了。

1. **版本 1（函数版）**：静态字段 `hour` 和 `workFinished`，一个静态的 `writeProgram()`，里面是嵌套条件。大鸟："怎么还在写面向过程的代码？"
2. **版本 2（分类版）**：把它包进 `class Work`，带上 `hour`/`workFinished` 属性。`writeProgram()` 方法体不变——只是形式上面向对象。
3. **诊断**：`writeProgram` 是一个 Long Method。它拥有每一个状态和每一次转移，因此违反单一职责原则；新规则（「所有人 20:00 前离开」）迫使整个方法被修改，因此违反开放-封闭原则。
4. **版本 3（状态模式版）**：`State` 带抽象的 `writeProgram(Work)`；六个具体状态（`Forenoon`、`Noon`、`Afternoon`、`Evening`、`Sleeping`、`Rest`）；`Work` 持有 `current`，初始化为 `ForenoonState`，并负责委托。每个状态要么输出，要么转移并重新分派。
5. **收益检验**：20:00 这条规则现在意味着新增一个 `ForcedOffState`，并只修改 `EveningState` 的条件。其他状态都不用动，客户端代码也完全没有变化。

为什么有效：转移逻辑分散在各个状态之间（"把各种状态转移逻辑分布到State的子类之间"），所以每个类都很小，增加或重排状态都只是局部改动。

## 关键要点
1. 一个长方法的分支在测试对象自身的状态，这才是使用状态模式的信号——而不仅仅是「有一个 `if`」。
2. 给抽象状态一个*行为*方法（`writeProgram`），而不是泛泛的 `handle`，并传入上下文，让各状态能读取数据并设置下一个状态。
3. 让各状态在转移之后重新分派，这样无论从哪个状态开始，一次调用都能落到正确的行为上。
4. 上下文负责初始化第一个状态并委托；它自己绝不能对状态做分支判断。
5. 用一条新需求来验证设计：如果它只触及一个状态类，说明这个模式在起作用。
6. 条件简单时就跳过这个模式；状态模式会增加类，只有面对真实的复杂度才值得。

## 关联章节
- **[ch03](ch03-single-responsibility.md)**、**[ch04](ch04-open-closed.md)**：Long Method 恰恰是用这两条原则诊断出来的。
- **[ch02](ch02-strategy.md)**：类的形状相同（上下文 + 抽象类 + 具体类）；区别在于谁来选择——客户端（策略模式）还是状态自己（状态模式）。
- **[ch24](ch24-chain-of-responsibility.md)**：同样是沿着一系列对象传递请求，但职责链模式（Chain of Responsibility）的链由客户端固定，而状态会自己选择后继。
- **[ch29](ch29-pattern-summary.md)**：比赛中的行为型分组把状态模式与其同类模式做了比较。
- **重构（Fowler）**：「Long Method」和「Replace Conditional with State/Strategy」是本章背后的具名重构手法。
