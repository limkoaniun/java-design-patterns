# 第23章：烤羊肉串引来的思考——命令模式（Command）

## 核心思想
把每个请求变成一个对象，这样中间人（服务员）就能对请求排队、记录日志、拒绝或撤销，而请求者无需与执行者（烤肉师傅）见面。顾客直接对着师傅喊的路边摊是紧耦合；用点菜单的餐馆就是命令模式。

## 引入的框架
- **命令模式（Command）** — “将一个请求封装为一个对象，从而使你可用不同的请求对客户进行参数化；对请求排队或记录请求日志，以及支持可撤销的操作。”[DP]
  - 适用场景：「行为请求者」与「行为实现者」紧耦合，而你需要对请求**排队**、**记录日志**、让接收者**否决**请求，或支持**撤销/重做**。
  - 做法：(1) 定义抽象的 `Command`，持有一个 `Receiver` 和一个抽象的 `excuteCommand()`；(2) 每个接收者动作对应一个 `ConcreteCommand`，其 `excuteCommand()` 调用该动作；(3) 一个 `Invoker` 保存命令（`setCommand`/`setOrder`）并触发执行（`executeCommand`/`notifyCommand`）；(4) 客户端创建接收者、命令和调用者，并把它们连接起来。
  - 结构：`Invoker`（`-command`、`+setCommand()`、`+executeCommand()`）→ `Command`（`-receiver`、`+excuteCommand()`）⟵ `ConcreteCommand`；`ConcreteCommand` → `Receiver`（`+action()`）。客户端创建 ConcreteCommand 并为其指定 Receiver。
  - 作者给出的角色说明：`Command` 声明执行操作的接口；`ConcreteCommand` 把一个接收者与一个动作绑定；`Invoker` 要求命令执行请求；`Receiver` 知道如何实施与执行请求相关的操作，任何类都可以作为接收者。

## 关键概念
- **行为请求者 / 行为实现者**：顾客与烤肉师傅；命令模式把二者解耦。
- **Invoker（服务员 Waiter）**：记录订单并通知执行；不知道怎么烤。
- **Receiver（烤肉串者 Barbecuer）**：`bakeMutton()`、`bakeChickenWing()`；唯一真正干活的类。
- **命令队列**：服务员里的 `ArrayList<Command> orders`；点完菜后统一通知一次。
- **请求日志**：服务员打印「增加订单 … 时间」和「取消订单 … 时间」；账单能算对（28 元对 24 元）靠的就是它。
- **否决请求**：由服务员（或接收者）决定「鸡翅没有了」，而不是客户端。
- **撤销（cancelOrder）**：把尚未执行的命令从队列中移除。
- **[R2P] 敏捷原则**：不要添加臆测的功能；真正需要撤销或排队时，再重构*为*命令模式。

## 心智模型
- 把 `Command` 看作一张**书面点菜单**：上面写着谁（接收者）和做什么（动作），所以任何人都可以拿着它、叠起来、划掉，或稍后递给厨房。
- 用服务员检验法：如果请求者必须盯着实现者干活才能得到想要的东西，那就是路边摊式的耦合。
- 与其「一个请求 → 立即执行一次」，不如「先收集订单，再统一通知」；批处理才使排队、记录日志和撤销成为可能。
- 把命令模式当作重构目标，而不是默认选择：“只有在真正需要如撤销／恢复操作等功能时，把原来的代码重构为命令模式才有意义。”[R2P]

## 反模式
- **客户端直接调用接收者**（`boy.bakeMutton()` ×n）："简单，但却极为僵化，有许许多多的隐患"——没有记录、没有顺序、不能撤销，而且否决逻辑由客户端承担。
- **服务员只持有一个 `Command`，每个订单通知一次**：能通过第一版代码，但"没有体现出命令模式的作用"——没有队列、没有日志、不能撤销，客户端仍要判断库存。
- **由客户端判断鸡翅是否有货**：这份知识属于接收者/调用者。
- **「以防万一」而实现命令模式**：臆测的通用性；敏捷的做法是等到需要时再重构。

## 代码示例
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
- **演示内容**：调用者对命令排队、记录日志、否决和撤销；接收者只负责烤；连接完成后客户端不再接触接收者。

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
- **演示内容**：最小的 Invoker → Command → Receiver 链条。

## 实战示例
1. **路边摊（紧耦合）**：`Barbecuer boy`，客户端直接调用 `boy.bakeMutton()`、`boy.bakeChickenWing()`。顾客一多，师傅就记不清谁付了钱、谁不要辣、谁先来。
2. **餐馆第一版**：引入 `Command`/`BakeMuttonCommand`/`BakeChickenWingCommand` 和只有一个 `command` 字段的 `Waiter`；客户端对每一项先 `setOrder` 再 `notifyCommand`。结构正确，但大鸟列出四个缺口：订单应先批量收集再一次发出；客户端不应判断库存；订单必须记录日志以便结账；未烤的东西必须可以撤销。
3. **餐馆第二版**：把 `private Command command` 换成 `ArrayList<Command> orders`；`setOrder` 否决鸡翅并带时间戳记录添加；`cancelOrder` 移除并记录；`notifyCommand` 一次执行整个队列。
4. **为什么划算**：收银时账单显示 10 串是 28 元；日志里显示改成了 6 串，于是找回正确的 24 元。没有记录就是"大家都说不清楚了"。
5. **作者总结的五个好处**（小菜 + 大鸟）：容易设计命令队列；容易记录日志；接收者可以否决请求；容易实现撤销和重做；加入新的具体命令不影响其他类。再加上最关键的一条：“命令模式把请求一个操作的对象与知道怎么执行一个操作的对象分割开。”[DP]

## 关键要点
1. 当请求必须排队、记录日志、被否决或被撤销时，使用命令模式；这是该模式明确的意图，而不是副作用。
2. 每个接收者动作对应一个 `ConcreteCommand`；命令携带其接收者，所以调用者无需知道活是怎么干的。
3. 给调用者一个命令集合并统一通知一次；只持有单个命令的调用者会丢掉该模式的大部分价值。
4. 把否决和日志逻辑放在调用者（或接收者）里，绝不放在客户端。
5. 不要臆测地预先构建命令模式；真正需要撤销或排队时再重构过去。
6. 新增命令类型就是新增一个类，现有代码都不用改（开放-封闭原则）。

## 关联章节
- **[ch04](ch04-open-closed.md)**：新命令通过扩展实现，无需修改现有类。
- **[ch18](ch18-memento.md)**：备忘录模式提供状态快照，使命令的撤销真正可逆。
- **[ch24](ch24-chain-of-responsibility.md)**：二者都解耦发送者与接收者；职责链沿处理者传递请求，命令模式则把请求包装成对象交给调用者。
- **[ch25](ch25-mediator.md)**：服务员在精神上就是一个居中协调的中间人；中介者模式把这种枢纽式协调推广到同事对象之间。
- **[ch29](ch29-pattern-summary.md)**：命令模式出现在比赛总结的行为型分组中。
- **Refactoring to Patterns [R2P]**：「不要添加臆测的命令模式」这一指导的来源。
