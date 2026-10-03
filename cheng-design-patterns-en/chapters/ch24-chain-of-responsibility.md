# Chapter 24: 加薪非要老总批？——职责链模式 — Chain of Responsibility

## Core Idea
A request (leave, raise) climbs manager → director → general manager until someone has authority to decide; the requester never knows who answers. Replace one fat `Manager.getResult()` full of level/type branches with a chain of handler subclasses, each holding a reference to its successor.

## Frameworks Introduced
- **职责链模式 (Chain of Responsibility)** — “使多个对象都有机会处理请求，从而避免请求的发送者和接收者之间的耦合关系。将这个对象连成一条链，并沿着这条链传递该请求，直到有一个对象处理它为止。”[DP]
  - Key property: “当客户提交一个请求时，请求是沿链传递直至有一个ConcreteHandler对象负责处理它。”[DP] The client does not know which object ends up handling it, so responsibilities can be re-organised without touching the client.
  - When to use: several objects *may* handle a request, the handler is decided at run time, and the set or order of handlers is likely to change (new management levels, different approval routes).
  - How: (1) abstract `Handler` with `protected Handler successor`, `setSuccessor()`, and abstract `handleRequest()`; (2) each `ConcreteHandler` handles what it is authorised for, otherwise forwards to `successor` if non-null; (3) the client builds the handlers, links them with `setSuccessor`, and submits requests to the head.
  - Structure: `Client` → `Handler` (`+setSuccessor(Handler)`, `+handleRequest(int)`) ⟵ `ConcreteHandler1`, `ConcreteHandler2`, …; each concrete handler owns a range (0–9, 10–19, 20–29) and forwards the rest.

## Key Concepts
- **后继者 (successor)**: the single reference each handler keeps; no handler knows the whole chain.
- **推卸责任**: the forwarding branch; each handler decides "handle" or "pass up".
- **Request (申请)**: `requestType` (请假 / 加薪), `requestContent`, `number` (days or yuan).
- **链的结构在客户端定义**: `manager.setSuperior(director); director.setSuperior(generalManager);` — reorderable at any time.
- **末端未处理风险**: a request may reach the end of the chain unhandled or be misconfigured; design for it up front.
- **简化对象连接**: handlers hold one successor reference instead of references to every candidate receiver.[DP]

## Mental Models
- Think of the chain as **mailing a letter up the org chart**: each office either signs or forwards; a wrong address means the letter never lands, so check the chain end.
- Use the "branch smell" trigger: a long method switching on *who* is handling and *what* is requested is two dimensions of change in one place; split the *who* into subclasses and let polymorphism replace the outer branch.
- Prefer configuring the chain at the client over hard-coding it; 小菜's manager "跳过了总监直接找总经理" is a chain restructure, not a code change.
- Each handler answers exactly two questions: can I handle this? if not, who is next?

## Anti-patterns
- **One `Manager` class with `getResult(managerLevel, request)`**: long method, nested branches on level and request type; every new management title edits it (violates 开放-封闭原则) and it carries every level's rules (violates 单一职责原则).
- **Client calling every manager in turn**: `manager.getResult(); director.getResult(); generalManager.getResult();` couples the requester to all receivers and their order.
- **Chain with no terminal handler**: requests silently fall off the end.
- **Comparing strings with `==`**: the book's listings do this; use `.equals()` in real code.

## Code Examples
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
- **What it demonstrates**: the client submits everything to `h1`; each request is handled by whichever handler owns its range.

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
- **What it demonstrates**: the branches of the old `getResult` are distributed one level per subclass; the client only knows the first manager.

## Worked Example
1. **Naive**: `Request` (type, content, number) plus one `Manager` class whose `getResult(String managerLevel, Request request)` nests `if (managerLevel == "经理") … else if ("总监") … else if ("总经理")` with inner tests on type and number. Client creates three `Manager` objects and calls `getResult` on each with the level string.
2. **What's wrong** (小菜's own diagnosis): the method is long with too many branches; adding 项目经理 / 部门经理 / 副总经理 means editing it → violates 开放-封闭原则; the class knows every level's rules → violates 单一职责原则.
3. **Refactor**: make `Manager` abstract with `name`, `superior`, `setSuperior()`, abstract `requestApplications()`. `CommonManager` approves leave ≤ 2 days, `Director` ≤ 5 days, `GeneralManager` approves any leave, raises ≤ 5000, and defers raises > 5000 ("再说吧"). Anything a level cannot approve goes to `superior.requestApplications(request)`.
4. **Client**: builds the three managers, links `manager → director → generalManager`, and submits four requests (leave 1 day, leave 4 days, raise 5000, raise 10000) *only to `manager`*; each is answered at the right level.
5. **Why**: the big branch is dissolved into polymorphic subclasses plus a successor link; a new 集团总裁 class only requires the general manager to forward — no other class changes. The epilogue shows chain flexibility in life: the manager skipped the director and went straight to the general manager, and the raise was approved.

## Key Takeaways
1. Use Chain of Responsibility when multiple objects could handle a request and the handler should be found at run time without coupling sender to receiver.
2. Each handler keeps exactly one successor reference; nobody holds the whole chain, which is what keeps coupling low.
3. Two things must be set up: every handler's successor, and every handler's "handle or forward" test.
4. Configure the chain in the client so it can be re-ordered or shortened without code changes.
5. Guard the chain's end; an unhandled request that falls off the tail is a silent failure.
6. Long methods branching on "who" plus "what" are a smell pointing to this pattern (and to SRP/OCP violations).

## Connects To
- **[ch03](ch03-single-responsibility.md)** and **[ch04](ch04-open-closed.md)**: the refactor is driven by SRP and OCP violations in the monolithic manager.
- **[ch16](ch16-state.md)**: State also replaces branch-heavy methods with polymorphic classes, but transitions state rather than forwarding a request.
- **[ch23](ch23-command.md)**: both decouple sender from receiver; Command objectifies the request, Chain routes it.
- **[ch25](ch25-mediator.md)**: Mediator centralises coordination in one hub, whereas Chain distributes it along a linked sequence.
- **[ch29](ch29-pattern-summary.md)**: contest summary places Chain of Responsibility among the behavioural patterns.
