# 第25章：世界需要和平——中介者模式（Mediator）

## 核心思想
当许多对象必须彼此了解时，相互引用形成的网使系统变成不可分割的一团。把所有交互都通过一个中介者转发，同事只认识中介者，网状结构就变成以中介者为中心的星状结构。

## 引入的框架
- **中介者模式（Mediator）** — “用一个中介对象来封装一系列的对象交互。中介者使各对象不需要显式地相互引用，从而使其耦合松散，而且可以独立地改变它们之间的交互。”[DP]
  - 结构：`Mediator`（抽象类，声明 `send(message, colleague)`）→ `ConcreteMediator`（认识每个 `ConcreteColleague`，接收消息并发出命令）；`Colleague`（抽象类，持有一个 `Mediator` 引用）→ `ConcreteColleague1/2`（只知道自己的行为和中介者）。
  - 适用场景：一组对象以定义良好但复杂的方式通信（作者的例子：Form/aspx 页面上的每个控件都通过窗体通信），或者想定制分散在多个类中的行为而不想生成大量子类。
  - 做法：(1) 给每个同事一个接收中介者的构造函数；(2) 同事调用 `mediator.send(msg, this)`，而不是互相调用；(3) 具体中介者决定调用哪个同事的 `notify`；(4) 如果预见不到会有多个中介者，就把 `Mediator` 和 `ConcreteMediator` 合并成一个类。
  - 为何有效 / 失败模式：耦合从 N×N 的同事连接变成 N 条通向中介者的连接。代价是所有交互的复杂性都落在 `ConcreteMediator` 上；同事很多时，它会成为系统中最复杂、最脆弱的类。

## 关键概念
- **网状 → 星状**：中介者带来的结构效果，每个节点都连向中心而不是彼此相连。
- **Colleague（同事类）**：只知道自己的行为和中介者、对其他同事一无所知的参与者。
- **ConcreteMediator**：必须认识所有具体同事；交互规则所在之处。
- **集中控制（centralised control）**：既是该模式的优点，也是它的弱点。
- **Form / aspx 作为中介者**：作者的日常例子，控件之间从不互相引用，由窗体的事件处理程序居中协调。
- **迪米特法则（Law of Demeter）**：中介者模式所实现的原则；两个无需直接通信的类应通过第三方转发（[ch11](ch11-law-of-demeter.md)）。

## 心智模型
- 把中介者想成联合国：各国（同事）不进行双边谈判，而是通过安理会发表声明，新增一个成员不会迫使其他成员都做修改。
- 当你发现自己在 `Button` 里编写设置 `TextBox.text` 的代码时，就该使用中介者；这种跨控件的知识应当属于窗体。
- 把中介者想成一面透镜，把你的视角从「每个对象做什么」提升到「对象之间如何交互」，设计的重心从个体行为转向协作。
- 不要一看到多对多的交互就立刻使用中介者模式；先问问设计本身是不是有问题。作者警告说它既容易用，也容易误用。

## 反模式
- **同事类直接互相引用**：每增加一个对象，每个同伴都得修改；系统无法逐步改动。
- **上帝中介者**：把所有规则都堆进 `ConcreteMediator`，直到它比任何同事都复杂，并成为单点故障（「安理会出了问题，整个世界都有问题」）。
- **过早引入中介者**：把该模式用在一团纠缠的对象上，而不去追问这组对象为什么会纠缠。

## 代码示例
作者的练习：美国和伊拉克只通过联合国安理会交谈。

```java
// Colleague
abstract class Country {
    protected UnitedNations unitedNations;
    public Country(UnitedNations unitedNations) { this.unitedNations = unitedNations; }
}
class USA extends Country {
    public USA(UnitedNations un) { super(un); }
    public void declare(String message) { this.unitedNations.declare(message, this); }
    public void getMessage(String message) { System.out.println("美国获得对方信息:" + message); }
}
class Iraq extends Country {
    public Iraq(UnitedNations un) { super(un); }
    public void declare(String message) { this.unitedNations.declare(message, this); }
    public void getMessage(String message) { System.out.println("伊拉克获得对方信息:" + message); }
}
// Mediator
abstract class UnitedNations {
    public abstract void declare(String message, Country country);
}
// ConcreteMediator: must know every concrete colleague
class UnitedNationsSecurityCouncil extends UnitedNations {
    private USA countryUSA;
    private Iraq countryIraq;
    public void setUSA(USA value) { this.countryUSA = value; }
    public void setIraq(Iraq value) { this.countryIraq = value; }
    public void declare(String message, Country country) {
        if (country == this.countryUSA) this.countryIraq.getMessage(message);
        else if (country == this.countryIraq) this.countryUSA.getMessage(message);
    }
}
// Client
UnitedNationsSecurityCouncil UNSC = new UnitedNationsSecurityCouncil();
USA c1 = new USA(UNSC);
Iraq c2 = new Iraq(UNSC);
UNSC.setUSA(c1);
UNSC.setIraq(c2);
c1.declare("不准研制核武器，否则要发动战争!");
c2.declare("我们没有核武器，也不怕侵略。");
```
- **它展示了什么**：同事只持有一个中介者引用；路由决策（`if country == USA → notify Iraq`）集中在一处，而通用模板（`Colleague`/`ConcreteColleague1,2`/`Mediator`/`ConcreteMediator`，带 `send`/`notify`）除了名字之外完全相同。

## 实战示例
1. **朴素的图景**：作者把各国画成一张网，每个国家都有双边联系。在代码中，每个对象都需要引用其他所有对象；增加一个对象意味着要改动所有对象，而且缺了其余对象，没有哪个对象能独立工作。
2. **应用迪米特法则**：小菜想起 ch11 中的迪米特法则。如果两个类无需直接通信，就通过第三方转发。联合国正是这个第三方。
3. **设计问题**：联合国是 `Mediator` 还是 `ConcreteMediator`？答案取决于中介者是否会增多。联合国有许多机构（安理会、WHO、WTO……），所以 `UnitedNations` 是抽象类，`UnitedNationsSecurityCouncil` 是具体类。如果预见不到扩展，就把它们合并成一个类。
4. **结果**：`USA` 和 `Iraq` 从不互相引用；增加一个国家只需修改中介者。
5. **小菜发现的问题**：`ConcreteMediator` 必须认识每个同事，因此职责不断累积。大鸟确认：该模式是用中介者自身的复杂性换取交互的复杂性。当交互确实复杂且定义明确时（带菜单、文本框、按钮的 Form）它很合适，若不假思索地使用则很糟糕。

## 关键要点
1. 当一组对象以复杂但定义明确的方式交互，并且你希望独立于这些对象来改变它们的交互时，使用中介者模式。
2. 同事只认识中介者和自己，从不认识彼此；增加一个同事应当只触及中介者。
3. 中介者是你从宏观角度审视系统的地方：它为协作建模，而不是为参与者建模。
4. 预期 `ConcreteMediator` 会是最复杂的类；如果它被同事淹没，该模式的代价就已超过收益。
5. 在把中介者模式用于多对多的混乱局面之前，先重新考虑设计；该模式很容易被误用。
6. 你其实已经在使用它了：GUI 窗体和网页通过事件在各控件之间居中协调。

## 关联章节
- **[ch11](ch11-law-of-demeter.md)**：中介者模式是迪米特法则在结构上的实现。
- **[ch12](ch12-facade.md)**：外观模式（Facade）同样降低耦合，但是从外部面向子系统；中介者模式则从内部协调同伴（对比见 [ch29](ch29-pattern-summary.md)）。
- **[ch14](ch14-observer.md)**：以 Form 作为中介者的例子依靠事件通知运行，这是一种观察者模式（Observer）机制。
- **[ch23](ch23-command.md)**：两者都解耦发送者与接收者；命令模式（Command）把请求具体化，中介者模式则集中路由。
