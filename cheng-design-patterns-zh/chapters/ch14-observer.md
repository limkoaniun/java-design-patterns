# 第14章：老板回来，我不知道——观察者模式（Observer）

## 核心思想
当一个对象的状态变化必须触发数量未知的其他对象更新时，让双方都依赖于抽象（Subject、Observer），这样通知者永远不知道谁在监听，监听者也永远不知道还有谁存在。老板回来时前台逐个打电话通知同事；唯一没来得及通知到的那位同事被抓了现行。

## 引入的框架
- **观察者模式（Observer），又叫作发布-订阅（Publish/Subscribe）模式** — “定义了一种一对多的依赖关系，让多个观察者对象同时监听某一个主题对象。这个主题对象在状态发生变化时，会通知所有观察者对象，使它们能够自动更新自己。”[DP]
  - 结构：`Subject`（抽象通知者；持有一组 `Observer` 引用；`attach()`、`detach()`、`notify()`）→ `ConcreteSubject`（持有 `subjectState`；状态变化时通知已注册的观察者）；`Observer`（抽象；`update()`）→ `ConcreteObserver`（实现 `update()`；可持有具体主题的引用以读取其状态）。
  - 动机 [DP]：“将一个系统分割成一系列相互协作的类有一个很不好的副作用，那就是需要维护相关对象间的一致性。我们不希望为了维持一致性而使各类紧密耦合”.
  - 适用场景：“当一个对象的改变需要同时改变其他对象的时候，而且它不知道具体有多少对象有待改变时”；另外，当“一个抽象模型有两个方面，其中一方面依赖于另一方面”并且希望两方面各自独立变化时，也适用。
  - 做法：(1) 定义带有 `update()` 的 `Observer`。(2) 定义持有观察者列表并带有 `attach/detach/notify` 的 `Subject`。(3) 具体主题先设置状态，再调用 `notify()`。(4) 具体观察者实现 `update()`，并通过抽象类型读取主题。(5) 客户端用 `attach()` 把它们连接起来。
  - 为何有效：“观察者模式所做的工作其实就是在解除耦合。让耦合的双方都依赖于抽象，而不是依赖于具体。” 失效情形：具体观察者若回头强制转换为具体主题（`(Boss) o`），会悄悄恢复耦合。
- **Java 内置支持: `java.util.Observable` / `java.util.Observer`** — `Observable` 已经提供了 `addObserver`、`deleteObserver`、`setChanged`、`notifyObservers`；观察者实现 `update(Observable o, Object arg)`。作者强调的限制：`Observable` 是一个*类*，而 Java 没有多重继承，所以你的主题无法再继承其他类——并且 `javac` 会给出警告 `[deprecation] java.util中的Observable已过时`。要在了解这一点的前提下使用，或者自己写抽象的 `Subject`。

## 关键概念
- **主题 / 抽象通知者（Subject）**：用集合保存观察者引用；提供 attach/detach。
- **观察者（Observer）**：更新接口；通常只有一个 `update()` 方法，即「更新方法」。
- **具体通知者（ConcreteSubject）**：保存状态；状态变化时通知每一个已注册的观察者。
- **具体观察者（ConcreteObserver）**：让自身状态与主题同步；可持有主题的引用。
- **双向耦合（bidirectional coupling）**：最初的缺陷——`Secretary` 列出 `StockObserver`，而 `StockObserver` 又持有 `Secretary`。
- **抽象类 vs. 接口（用于 Observer）**：观察者之间共享代码时用抽象类；观察者是只需要 `update()` 的互不相关的类（“风马牛不相及的类”）时用接口。
- **setChanged / notifyObservers**：`Observable` 子类触发通知所调用的两个方法。
- **事件委托 / 控件通知**：UI 工具包（Word 的样式窗格、Swing、Android）都是这样工作的——控件实现类似观察者的接口，并对开关发出的通知作出反应。

## 心智模型
- 把 `attach()` 想成「给全班群发通知」（石守吉的电话号码故事）：遍历每一个已登记的联系人，各发一次，一个都不漏。
- 只要是「X 变化时，Y 和 Z 必须作出反应」，并且 Y/Z 的集合是开放的，就用观察者模式。
- 主题是盲目广播的：它不能知道谁在监听、有多少在监听；如果知道，那就是依赖，而不是订阅。
- 实际代码中优先使用基于接口的 `Observer`；只有具体观察者确实共享实现时才用抽象类 `Observer`。

## 反模式
- **主题绑定到具体观察者**（`ArrayList<StockObserver>`）：新增一个 `NBAObserver` 就得修改 `Secretary`——违反开放-封闭原则（OCP）。
- **观察者绑定到具体主题**（`protected Secretary sub;`）：当通知者变成 `Boss` 时，每个观察者都要修改。小菜的第二版只修复了一边；大鸟称之为「只完成一半」。
- **在 `update(Observable o, ...)` 内部做强制转换**（`Boss b = (Boss) o;`）：JDK 的签名诱导你这么做，而这会让具体观察者与具体主题重新耦合；应当转换为你自己的抽象 `Subject`。
- **需要另一个父类时仍继承 `Observable`**：在 Java 中不可能；JDK 的这个类正是因为这种复用上的限制而被弃用。
- **忘记 `detach()`**：无法移除观察者的主题（对某个同事生气的前台）会泄漏通知和引用。

## 代码示例
```java
// Abstract notifier
abstract class Subject {
    protected String name;
    private List<Observer> list = new ArrayList<>();   // programmed against the abstract Observer
    private String action;
    public Subject(String name) { this.name = name; }
    public void attach(Observer observer) { list.add(observer); }
    public void detach(Observer observer) { list.remove(observer); }
    public void notifyEmployee() { for (Observer item : list) item.update(); }
    public String getAction() { return action; }
    public void setAction(String value) { action = value; }
}
class Boss extends Subject      { public Boss(String name) { super(name); } }
class Secretary extends Subject { public Secretary(String name) { super(name); } }

// Abstract observer (interface is equally valid: interface Observer { void update(); })
abstract class Observer {
    protected String name;
    protected Subject sub;          // was Secretary — now the abstraction
    public Observer(String name, Subject sub) { this.name = name; this.sub = sub; }
    public abstract void update();
}
class StockObserver extends Observer {
    public StockObserver(String name, Subject sub) { super(name, sub); }
    public void update() {
        System.out.println(sub.name + ": " + sub.getAction() + "! " + name + "，请关闭股票行情，赶紧工作。");
    }
}
class NBAObserver extends Observer {
    public NBAObserver(String name, Subject sub) { super(name, sub); }
    public void update() {
        System.out.println(sub.name + ": " + sub.getAction() + "! " + name + "，请关闭NBA直播，赶紧工作。");
    }
}

// Client
Subject boss1 = new Boss("胡汉三");
Observer employee1 = new StockObserver("魏关姹", boss1);
Observer employee2 = new StockObserver("易管查", boss1);
Observer employee3 = new NBAObserver("霍华德", boss1);
boss1.attach(employee1); boss1.attach(employee2); boss1.attach(employee3);
boss1.detach(employee1);            // 魏关姹 was never reached — and got caught
boss1.setAction("我胡汉三回来了");
boss1.notifyEmployee();
```
- **演示了什么**：两个方向都依赖于抽象；把 `Secretary` 换成 `Boss`，或者新增一种观察者，都不会触及任何已有的类。

```java
// Using the JDK's Observable, without re-coupling to the concrete subject
class Subject extends Observable {
    protected String name;
    private String action;
    public Subject(String name) { this.name = name; }
    public String getAction() { return action; }
    public void setAction(String value) {
        action = value;
        setChanged();            // mark state changed
        notifyObservers();       // JDK iterates registered observers
    }
}
class Boss extends Subject { public Boss(String name) { super(name); } }

class StockObserver implements java.util.Observer {
    protected String name;
    public StockObserver(String name) { this.name = name; }
    public void update(Observable o, Object arg) {   // signature fixed by the JDK
        Subject b = (Subject) o;                      // cast to the abstraction, not to Boss
        System.out.println(b.name + ": " + b.getAction() + "! " + name + "，请关闭股票行情，赶紧工作。");
    }
}
Boss boss1 = new Boss("胡汉三");
boss1.addObserver(new StockObserver("魏关姹"));
boss1.setAction("我胡汉三回来了");
```
- **演示了什么**：`Observable` 省去了 attach/detach/notify 的样板代码；中间层 `Subject` 让观察者远离具体的 `Boss`。注意弃用警告以及单继承的代价。

## 参考表
| 版本 | 主题一侧 | 观察者一侧 | 结果 |
|---|---|---|---|
| 1. 双向耦合 | `Secretary` 持有 `List<StockObserver>` | `StockObserver` 持有 `Secretary` | 新增 NBA 观察者要修改两个类 |
| 2. 解耦实践一 | `Secretary` 持有 `List<Observer>` | `Observer`（抽象）持有 `Secretary` | 只完成一半：观察者仍绑定在具体通知者上 |
| 3. 解耦实践二 | `Subject`（抽象）持有 `List<Observer>` | `Observer` 持有 `Subject` | 两边都是抽象；Boss/Secretary 可互换 |
| 4. JDK `Observable` | `Subject extends Observable` | `implements Observer`，转换为 `Subject` | 代码更少；受单继承限制；已弃用 |

## 实战示例
**故事：** 老板不在时，同事们在看股票行情。前台童子喆在老板回来时给其中一位同事打电话；大家手忙脚乱。有一天老板带着童子喆走进来（她根本没来得及打电话），背对着门的魏关姹冲着老板的脸大喊「我的股票涨停了哦」。

**第一版：** `Secretary` 带有 `attach(StockObserver)`、`notifyEmployee()` 和 `setAction("老板回来了")`；`StockObserver` 持有一个 `Secretary`，并在 `update()` 中打印她的动作。能工作，但这两个类彼此具体引用。新增一位看 NBA 的同事就意味着要修改 `Secretary`。

**第二版：** 引入带有 `update()` 的抽象 `Observer`；`StockObserver` 和 `NBAObserver` 继承它；`Secretary` 现在持有 `List<Observer>` 并新增 `detach()`。大鸟：只完成了一半——`Observer` 仍然持有一个 `Secretary`。如果通知者是*老板*呢？

**第三版：** 抽象 `Subject` 带有 `attach/detach/notifyEmployee/getAction/setAction`；`Boss` 和 `Secretary` 都继承它。`Observer.sub` 变成 `Subject`。客户端：向 `boss1` 注册三位同事，`detach(employee1)`（魏关姹没被通知到），设置动作，发出通知。输出显示两条警告；魏关姹没有收到，于是被抓了现行。

**改进：** 作者随后展示了纯粹的结构（`subjectState`、`notifyObserver()`），论证了实践中接口是更好的 `Observer`，并演示了 JDK 的做法——通过继承 `Observable` 的中间层 `Subject`，使 `StockObserver` 永远看不到 `Boss`。

## 关键要点
1. 两边都要解耦：主题 → 抽象观察者，*并且*观察者 → 抽象主题。只解耦一半仍然是耦合。
2. 主题不能知道有哪些观察者、有多少观察者；它只遍历一个抽象类型的列表。
3. 提供 `detach()`；无法移除的订阅会变成泄漏和过期通知。
4. 观察者是互不相关的类时，`Observer` 用接口；只有为了共享代码才用抽象类。
5. `java.util.Observable` 省去了样板代码，但会占掉你唯一的继承名额并且已被弃用；把它包在你自己的 `Subject` 后面，或者自己写。
6. 观察者模式是依赖倒转原则（DIP）最纯粹的形态——是 Swing/Android/Word 中 UI 事件处理背后的机制。

## 关联章节
- **[ch05](ch05-dependency-inversion.md)**：“这实在是依赖倒转原则的最佳体现”——双方都依赖于抽象。
- **[ch04](ch04-open-closed.md)**：触发重构的原因是新增 `NBAObserver` 需要修改 `Secretary`。
- **[ch25](ch25-mediator.md)**：中介者模式（Mediator）集中处理多对多通信；观察者模式处理一对多广播。
- **[ch16](ch16-state.md)**：主题广播的往往就是状态变化。
- **[ch23](ch23-command.md)**：命令往往是观察者收到通知后放入队列的东西。
- **[ch29](ch29-pattern-summary.md)**：观察者模式进入最终五强；MVC 被提及为它最著名的宿主。
