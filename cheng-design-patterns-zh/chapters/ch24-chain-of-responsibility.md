# 第24章：加薪非要老总批？——职责链模式（Chain of Responsibility）

## 核心思想
一个请求（请假、加薪）沿着经理 → 总监 → 总经理逐级上传，直到有人有权决定；请求者并不知道最终由谁回答。把塞满级别/类型分支的 `Manager.getResult()` 这一个臃肿方法，替换为一条由处理者子类组成的链，每个处理者持有其后继者的引用。

## 引入的框架
- **职责链模式（Chain of Responsibility）** — “使多个对象都有机会处理请求，从而避免请求的发送者和接收者之间的耦合关系。将这个对象连成一条链，并沿着这条链传递该请求，直到有一个对象处理它为止。”[DP]
  - 关键特性：“当客户提交一个请求时，请求是沿链传递直至有一个ConcreteHandler对象负责处理它。”[DP] 客户端不知道最终由哪个对象处理，因此可以重新组织职责而无需改动客户端。
  - 适用场景：多个对象*可能*处理某个请求、处理者在运行时才确定，且处理者的集合或顺序很可能变化（新增管理层级、不同的审批路线）。
  - 做法：(1) 抽象 `Handler`，含 `protected Handler successor`、`setSuccessor()` 和抽象的 `handleRequest()`；(2) 每个 `ConcreteHandler` 处理自己被授权的请求，否则在 `successor` 非空时转发给它；(3) 客户端创建处理者，用 `setSuccessor` 把它们连起来，并把请求提交给链头。
  - 结构：`Client` → `Handler`（`+setSuccessor(Handler)`、`+handleRequest(int)`）⟵ `ConcreteHandler1`、`ConcreteHandler2`……；每个具体处理者负责一个范围（0–9、10–19、20–29），其余的转发出去。

## 关键概念
- **后继者（successor）**：每个处理者持有的唯一引用；没有任何处理者知道整条链。
- **推卸责任**：转发分支；每个处理者决定是「处理」还是「上传」。
- **Request（申请）**：`requestType`（请假 / 加薪）、`requestContent`、`number`（天数或元数）。
- **链的结构在客户端定义**：`manager.setSuperior(director); director.setSuperior(generalManager);` — 可随时重新排序。
- **末端未处理风险**：请求可能到达链尾仍无人处理，或链被配置错误；要预先考虑。
- **简化对象连接**：处理者只持有一个后继者引用，而不是持有每个候选接收者的引用。[DP]

## 心智模型
- 把链想成**沿组织架构向上寄信**：每个办公室要么签字，要么转发；地址写错信就永远送不到，所以要检查链的末端。
- 使用「分支坏味道」触发器：一个按*谁*在处理、*什么*被请求来做分支切换的长方法，是把两个维度的变化放在了一处；把*谁*拆成子类，让多态替换外层分支。
- 优先在客户端配置链，而不是硬编码；小菜的经理「跳过了总监直接找总经理」是链的重组，而不是代码的改动。
- 每个处理者只回答两个问题：我能处理吗？不能的话，下一位是谁？

## 反模式
- **一个 `Manager` 类里放 `getResult(managerLevel, request)`**：方法很长，按级别和请求类型层层嵌套分支；每新增一个管理头衔都要修改它（违反开放-封闭原则（OCP）），而且它承载了每个级别的规则（违反单一职责原则（SRP））。
- **客户端依次调用每个经理**：`manager.getResult(); director.getResult(); generalManager.getResult();` 把请求者与所有接收者及其顺序耦合在一起。
- **没有终端处理者的链**：请求会悄无声息地从末端掉落。
- **用 `==` 比较字符串**：书中的代码清单这样写；真实代码中请用 `.equals()`。

## 代码示例
```java
// GoF 基本代码
abstract class Handler {
    protected Handler successor;
    public void setSuccessor(Handler successor) { this.successor = successor; }
    public abstract void handleRequest(int request);
}
class ConcreteHandler1 extends Handler {
    public void handleRequest(int request) {
        if (request >= 0 && request < 10) {
            System.out.println(getClass().getSimpleName() + " 处理请求 " + request);
        } else if (successor != null) {
            successor.handleRequest(request);          // 转移到下一位
        }
    }
}
// ConcreteHandler2 处理 10~19，ConcreteHandler3 处理 20~29，结构相同
Handler h1 = new ConcreteHandler1();
Handler h2 = new ConcreteHandler2();
Handler h3 = new ConcreteHandler3();
h1.setSuccessor(h2);
h2.setSuccessor(h3);                                   // 设置职责链上家与下家
int[] requests = { 2, 5, 14, 22, 18, 3, 27, 20 };
for (int request : requests) h1.handleRequest(request);
```
- **演示了什么**：客户端把所有请求都提交给 `h1`；每个请求由范围与之匹配的处理者处理。

```java
// 加薪／请假：管理者职责链
abstract class Manager {
    protected String name;
    protected Manager superior;
    public Manager(String name) { this.name = name; }
    public void setSuperior(Manager superior) { this.superior = superior; }   // 设置上级
    public abstract void requestApplications(Request request);
}
class CommonManager extends Manager {                 // 经理：可批2天内假期
    public CommonManager(String name) { super(name); }
    public void requestApplications(Request request) {
        if (request.getRequestType().equals("请假") && request.getNumber() <= 2)
            System.out.println(name + ":" + request.getRequestContent() + " 数量:" + request.getNumber() + "天，被批准");
        else if (superior != null)
            superior.requestApplications(request);
    }
}
class Director extends Manager {                      // 总监：可批5天内假期
    public Director(String name) { super(name); }
    public void requestApplications(Request request) {
        if (request.getRequestType().equals("请假") && request.getNumber() <= 5)
            System.out.println(name + ":" + request.getRequestContent() + " 数量:" + request.getNumber() + "天，被批准");
        else if (superior != null)
            superior.requestApplications(request);
    }
}
class GeneralManager extends Manager {                // 总经理：全部处理
    public GeneralManager(String name) { super(name); }
    public void requestApplications(Request request) {
        if (request.getRequestType().equals("请假"))
            System.out.println(name + ":" + request.getRequestContent() + " 数量:" + request.getNumber() + "天，被批准");
        else if (request.getRequestType().equals("加薪") && request.getNumber() <= 5000)
            System.out.println(name + ":" + request.getRequestContent() + " 数量:" + request.getNumber() + "元，被批准");
        else if (request.getRequestType().equals("加薪") && request.getNumber() > 5000)
            System.out.println(name + ":" + request.getRequestContent() + " 数量:" + request.getNumber() + "元，再说吧");
    }
}
// 客户端：链在这里装配
CommonManager manager = new CommonManager("金利");
Director director = new Director("宗剑");
GeneralManager generalManager = new GeneralManager("钟精励");
manager.setSuperior(director);
director.setSuperior(generalManager);
Request r = new Request();
r.setRequestType("加薪"); r.setRequestContent("小菜请求加薪"); r.setNumber(10000);
manager.requestApplications(r);     // 客户端不知道最终由谁处理 → 总经理："再说吧"
```
- **演示了什么**：旧的 `getResult` 的各个分支被分摊到每个子类一个级别；客户端只认识第一个经理。

## 实战示例
1. **朴素做法**：`Request`（类型、内容、数量）加一个 `Manager` 类，其 `getResult(String managerLevel, Request request)` 嵌套 `if (managerLevel == "经理") … else if ("总监") … else if ("总经理")`，内部再按类型和数量判断。客户端创建三个 `Manager` 对象，并用级别字符串对每个对象调用 `getResult`。
2. **问题所在**（小菜自己的诊断）：方法太长、分支太多；新增项目经理 / 部门经理 / 副总经理意味着要修改它 → 违反开放-封闭原则；该类知道每个级别的规则 → 违反单一职责原则。
3. **重构**：让 `Manager` 成为抽象类，含 `name`、`superior`、`setSuperior()` 和抽象的 `requestApplications()`。`CommonManager` 批准 ≤ 2 天的假期，`Director` 批准 ≤ 5 天，`GeneralManager` 批准任意假期、≤ 5000 的加薪，并推迟 > 5000 的加薪（「再说吧」）。某个级别批不了的一切请求都交给 `superior.requestApplications(request)`。
4. **客户端**：创建三个经理，把 `manager → director → generalManager` 连起来，并把四个请求（请假 1 天、请假 4 天、加薪 5000、加薪 10000）*只提交给 `manager`*；每个请求都在恰当的级别得到答复。
5. **原因**：庞大的分支被拆解成多态子类加后继者链接；新增一个集团总裁类，只需要总经理转发即可，其他类都不用改。尾声展示了现实中链的灵活性：经理跳过了总监直接找总经理，加薪获批。

## 关键要点
1. 当多个对象都可能处理某个请求，且需要在运行时找到处理者而不把发送者与接收者耦合时，使用职责链模式。
2. 每个处理者恰好持有一个后继者引用；没有谁持有整条链，这正是耦合保持较低的原因。
3. 必须设置两件事：每个处理者的后继者，以及每个处理者的「处理还是转发」判断。
4. 在客户端配置链，这样无需改代码就能重新排序或缩短。
5. 守住链的末端；掉出链尾的未处理请求是一种静默失败。
6. 按「谁」加「什么」来分支的长方法是指向本模式的坏味道（同时也指向对单一职责原则和开放-封闭原则的违反）。

## 关联章节
- **[ch03](ch03-single-responsibility.md)** 与 **[ch04](ch04-open-closed.md)**：这次重构由单体经理类中违反单一职责原则和开放-封闭原则所驱动。
- **[ch16](ch16-state.md)**：状态模式（State）同样用多态类替换分支密集的方法，但它是迁移状态，而不是转发请求。
- **[ch23](ch23-command.md)**：两者都解耦发送者与接收者；命令模式把请求对象化，职责链模式负责路由请求。
- **[ch25](ch25-mediator.md)**：中介者模式（Mediator）把协调集中在一个枢纽中，而职责链模式把协调分布在一条链接的序列上。
- **[ch29](ch29-pattern-summary.md)**：比赛总结把职责链模式归入行为型模式。
