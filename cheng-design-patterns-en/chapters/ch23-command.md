# Chapter 23: 烤羊肉串引来的思考——命令模式 — Command

## Core Idea
Turn each request into an object so that a middle-man (the waiter) can queue it, log it, reject it, or cancel it without the requester ever meeting the executor (the grill cook). The street stall where customers shout directly at the cook is tight coupling; the restaurant with an order pad is the Command pattern.

## Frameworks Introduced
- **命令模式 (Command)** — “将一个请求封装为一个对象，从而使你可用不同的请求对客户进行参数化；对请求排队或记录请求日志，以及支持可撤销的操作。”[DP]
  - When to use: the '行为请求者' and '行为实现者' are tightly coupled and you need to **queue** requests, **log** them, let the receiver **veto** them, or support **undo/redo**.
  - How: (1) define abstract `Command` holding a `Receiver` and an abstract `excuteCommand()`; (2) one `ConcreteCommand` per receiver action, whose `excuteCommand()` calls that action; (3) an `Invoker` that stores commands (`setCommand`/`setOrder`) and fires them (`executeCommand`/`notifyCommand`); (4) the client builds receiver, commands, invoker and wires them.
  - Structure: `Invoker` (`-command`, `+setCommand()`, `+executeCommand()`) → `Command` (`-receiver`, `+excuteCommand()`) ⟵ `ConcreteCommand`; `ConcreteCommand` → `Receiver` (`+action()`). Client creates the ConcreteCommand and assigns its Receiver.
  - Role glossary from the author: `Command` declares the execution interface; `ConcreteCommand` binds a receiver to an action; `Invoker` asks the command to carry out the request; `Receiver` knows how to perform the operation — any class can be a receiver.

## Key Concepts
- **行为请求者 / 行为实现者**: customer vs grill cook; Command decouples them.
- **Invoker (服务员 Waiter)**: records orders and notifies execution; does not know how to cook.
- **Receiver (烤肉串者 Barbecuer)**: `bakeMutton()`, `bakeChickenWing()`; the only class that does real work.
- **命令队列**: `ArrayList<Command> orders` in the waiter; notify once after all ordering is done.
- **请求日志**: waiter prints "增加订单 … 时间" and "取消订单 … 时间"; this is what makes the bill correct (28 元 vs 24 元).
- **否决请求**: the waiter (or receiver) decides "鸡翅没有了", not the client.
- **撤销 (cancelOrder)**: remove a not-yet-executed command from the queue.
- **[R2P] 敏捷原则**: don't add speculative features; refactor *to* Command when undo/queueing is actually needed.

## Mental Models
- Think of a `Command` as a **written order slip**: it carries who (receiver) and what (action), so anyone can hold it, stack it, strike it through, or hand it to the kitchen later.
- Use the waiter test: if the requester must watch the implementer work to get what they want, you have street-stall coupling.
- Prefer "collect orders, then notify once" over "one request → one immediate execution"; batching is what makes queueing, logging and cancellation possible.
- Treat Command as a refactoring target, not a default: “只有在真正需要如撤销／恢复操作等功能时，把原来的代码重构为命令模式才有意义。”[R2P]

## Anti-patterns
- **Client calls the receiver directly** (`boy.bakeMutton()` ×n): "简单，但却极为僵化，有许许多多的隐患" — no record, no ordering, no cancellation, and the client bears the veto logic.
- **Waiter holding a single `Command` and notifying per order**: passes the first version of the code but "没有体现出命令模式的作用" — no queue, no log, no undo, client still judges stock.
- **Client deciding whether chicken wings are available**: the receiver/invoker owns that knowledge.
- **Implementing Command "just in case"**: speculative generality; the agile answer is to wait and refactor when needed.

## Code Examples
```java
// Receiver：烤肉串者
class Barbecuer {
    public void bakeMutton()      { System.out.println("烤羊肉串!"); }
    public void bakeChickenWing() { System.out.println("烤鸡翅!"); }
}
// 抽象命令类
abstract class Command {
    protected Barbecuer receiver;
    public Command(Barbecuer receiver) { this.receiver = receiver; }
    public abstract void excuteCommand();
}
// 具体命令类：每个受理者动作一个命令
class BakeMuttonCommand extends Command {
    public BakeMuttonCommand(Barbecuer receiver) { super(receiver); }
    public void excuteCommand() { receiver.bakeMutton(); }
}
class BakeChickenWingCommand extends Command {
    public BakeChickenWingCommand(Barbecuer receiver) { super(receiver); }
    public void excuteCommand() { receiver.bakeChickenWing(); }
}
// Invoker：服务员（第三版——队列、日志、否决、撤销）
class Waiter {
    private ArrayList<Command> orders = new ArrayList<Command>();
    public void setOrder(Command command) {
        String className = command.getClass().getSimpleName();
        if (className.equals("BakeChickenWingCommand")) {
            System.out.println("服务员：鸡翅没有了，请点别的烧烤。");   // 由服务员否决
        } else {
            this.orders.add(command);
            System.out.println("增加订单: " + className + " 时间: " + getNowTime());   // 日志
        }
    }
    public void cancelOrder(Command command) {
        String className = command.getClass().getSimpleName();
        orders.remove(command);
        System.out.println("取消订单: " + className + " 时间: " + getNowTime());
    }
    public void notifyCommand() {                     // 一次性通知厨房
        for (Command command : orders) command.excuteCommand();
    }
    private String getNowTime() {
        return new SimpleDateFormat("HH:mm:ss").format(new Date());
    }
}
// 客户端
Barbecuer boy = new Barbecuer();
Command bakeMuttonCommand1      = new BakeMuttonCommand(boy);
Command bakeChickenWingCommand1 = new BakeChickenWingCommand(boy);
Waiter girl = new Waiter();
System.out.println("开门营业，顾客点菜");
girl.setOrder(bakeMuttonCommand1);
girl.setOrder(bakeMuttonCommand1);
girl.setOrder(bakeMuttonCommand1);
girl.cancelOrder(bakeMuttonCommand1);        // 撤销一串
girl.setOrder(bakeChickenWingCommand1);      // 被否决
System.out.println("点菜完毕，通知厨房烧菜");
girl.notifyCommand();
```
- **What it demonstrates**: the invoker queues, logs, vetoes and cancels commands; the receiver only cooks; the client never touches the receiver after wiring.

```java
// GoF 基本代码
abstract class Command {
    protected Receiver receiver;
    public Command(Receiver receiver) { this.receiver = receiver; }
    public abstract void excuteCommand();
}
class ConcreteCommand extends Command {
    public ConcreteCommand(Receiver receiver) { super(receiver); }
    public void excuteCommand() { receiver.action(); }
}
class Invoker {
    private Command command;
    public void setCommand(Command command) { this.command = command; }
    public void executeCommand() { command.excuteCommand(); }
}
class Receiver { public void action() { System.out.println("执行请求!"); } }
Receiver receiver = new Receiver();
Command command = new ConcreteCommand(receiver);
Invoker invoker = new Invoker();
invoker.setCommand(command);
invoker.executeCommand();
```
- **What it demonstrates**: the minimal Invoker → Command → Receiver chain.

## Worked Example
1. **Street stall (紧耦合)**: `Barbecuer boy` and the client calls `boy.bakeMutton()`, `boy.bakeChickenWing()` directly. With many customers the cook forgets who paid, who wanted no chilli, who was first.
2. **Restaurant v1**: introduce `Command`/`BakeMuttonCommand`/`BakeChickenWingCommand` and a `Waiter` with one `command` field; client does `setOrder` then `notifyCommand` per item. Correct structure, but 大鸟 lists four gaps: orders should be batched then sent once; the client should not judge stock; orders must be logged for billing; uncooked items must be cancellable.
3. **Restaurant v2**: replace `private Command command` with `ArrayList<Command> orders`; `setOrder` vetoes chicken wings and logs additions with a timestamp; `cancelOrder` removes and logs; `notifyCommand` executes the whole queue once.
4. **Why it pays off**: at the till the bill says 28 元 for 10 skewers; the log shows the change to 6, so the correct 24 元 is recovered. Without the record "大家都说不清楚了".
5. **Author's five benefits** (小菜 + 大鸟): easy command queue; easy logging; receiver may veto; easy undo/redo; new concrete commands don't affect other classes. Plus the key one: “命令模式把请求一个操作的对象与知道怎么执行一个操作的对象分割开。”[DP]

## Key Takeaways
1. Use Command when requests must be queued, logged, vetoed, or undone; that is the pattern's stated intent, not a side effect.
2. One `ConcreteCommand` per receiver action; the command carries its receiver so the invoker stays ignorant of how work is done.
3. Give the invoker a collection of commands and notify once; single-command invokers throw away most of the pattern's value.
4. Put veto and logging logic in the invoker (or receiver), never in the client.
5. Don't pre-build Command speculatively; refactor to it when undo or queueing is genuinely required.
6. Adding a new command type is a new class; nothing existing changes (开放-封闭).

## Connects To
- **[ch04](ch04-open-closed.md)**: new commands extend without modifying existing classes.
- **[ch18](ch18-memento.md)**: Memento supplies the state snapshot that makes Command's undo genuinely reversible.
- **[ch24](ch24-chain-of-responsibility.md)**: both decouple sender from receiver; Chain passes a request along handlers, Command wraps it as an object for an invoker.
- **[ch25](ch25-mediator.md)**: the waiter is a mediating middle-man in spirit; Mediator generalises hub-style coordination among colleagues.
- **[ch29](ch29-pattern-summary.md)**: Command appears in the behavioural group of the contest summary.
- **Refactoring to Patterns [R2P]**: the source of the "don't add speculative Command" guidance.
