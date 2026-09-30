# Chapter 14: 老板回来，我不知道——观察者模式 — Observer

## Core Idea
When one object's state change must trigger updates in an unknown number of other objects, make both sides depend on abstractions (Subject, Observer) so the notifier never knows who listens and the listeners never know who else exists. The receptionist calls everyone when the boss returns; the one colleague she could not reach got caught.

## Frameworks Introduced
- **观察者模式 (Observer)，又叫作发布-订阅 (Publish/Subscribe) 模式** — “定义了一种一对多的依赖关系，让多个观察者对象同时监听某一个主题对象。这个主题对象在状态发生变化时，会通知所有观察者对象，使它们能够自动更新自己。”[DP]
  - Structure: `Subject` (abstract notifier; keeps a collection of `Observer` refs; `attach()`, `detach()`, `notify()`) → `ConcreteSubject` (holds `subjectState`; notifies registered observers when it changes); `Observer` (abstract; `update()`) → `ConcreteObserver` (implements `update()`; may hold a ref to the concrete subject to read its state).
  - Motivation [DP]: “将一个系统分割成一系列相互协作的类有一个很不好的副作用，那就是需要维护相关对象间的一致性。我们不希望为了维持一致性而使各类紧密耦合”.
  - When to use: “当一个对象的改变需要同时改变其他对象的时候，而且它不知道具体有多少对象有待改变时”; also when “一个抽象模型有两个方面，其中一方面依赖于另一方面” and you want each side to vary independently.
  - How: (1) Define `Observer` with `update()`. (2) Define `Subject` with a list of observers and `attach/detach/notify`. (3) Concrete subjects set state then call `notify()`. (4) Concrete observers implement `update()` and read the subject through the abstract type. (5) Client wires them with `attach()`.
  - Why it works: “观察者模式所做的工作其实就是在解除耦合。让耦合的双方都依赖于抽象，而不是依赖于具体。” Failure mode: a concrete observer that casts back to a concrete subject (`(Boss) o`) silently restores the coupling.
- **Java 内置支持: `java.util.Observable` / `java.util.Observer`** — `Observable` already provides `addObserver`, `deleteObserver`, `setChanged`, `notifyObservers`; the observer implements `update(Observable o, Object arg)`. Limitation the author stresses: `Observable` is a *class*, Java has no multiple inheritance, so your subject cannot extend anything else — and `javac` warns `[deprecation] java.util中的Observable已过时`. Use it knowingly, or write your own abstract `Subject`.

## Key Concepts
- **主题 / 抽象通知者 (Subject)**: keeps observer references in a collection; offers attach/detach.
- **观察者 (Observer)**: the update interface; usually one `update()` method, "更新方法".
- **具体通知者 (ConcreteSubject)**: stores state; on change, notifies every registered observer.
- **具体观察者 (ConcreteObserver)**: syncs its own state with the subject; may keep a reference to the subject.
- **双向耦合 (bidirectional coupling)**: the initial bug — `Secretary` lists `StockObserver`s and `StockObserver` holds a `Secretary`.
- **抽象类 vs. 接口 for Observer**: an abstract class when observers share code; an interface when observers are unrelated classes (“风马牛不相及的类”) that only need `update()`.
- **setChanged / notifyObservers**: the two calls an `Observable` subclass makes to fire notifications.
- **事件委托 / 控件通知**: UI toolkits (Word's 样式窗格, Swing, Android) work this way — controls implement an observer-like interface and react to notifications from a toggle.

## Mental Models
- Think of `attach()` as "group-texting the class list" (the 石守吉 phone-number story): iterate every registered contact, send once, nobody is missed.
- Use Observer whenever "when X changes, Y and Z must react" and the set of Y/Z is open-ended.
- The subject broadcasts blind: it must not know who or how many listen; if it does, you have a dependency, not a subscription.
- Prefer interface-based `Observer` in real code; abstract-class `Observer` only when concrete observers genuinely share implementation.

## Anti-patterns
- **Subject typed to a concrete observer** (`ArrayList<StockObserver>`): adding an `NBAObserver` forces editing `Secretary` — violates 开放-封闭.
- **Observer typed to a concrete subject** (`protected Secretary sub;`): when the notifier becomes the `Boss`, every observer changes. 小菜's second version fixed only one side; 大鸟 calls it "只完成一半".
- **Casting inside `update(Observable o, ...)`** (`Boss b = (Boss) o;`): the JDK signature invites this, and it re-couples the concrete observer to the concrete subject; cast to your abstract `Subject` instead.
- **Extending `Observable` when your class needs another parent**: impossible in Java; the JDK class is deprecated for exactly this reuse limitation.
- **Forgetting `detach()`**: a subject that cannot remove observers (the receptionist who is angry at one colleague) leaks notifications and references.

## Code Examples
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
- **What it demonstrates**: both directions depend on abstractions; swapping `Secretary` for `Boss` or adding an observer type touches no existing class.

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
- **What it demonstrates**: `Observable` removes attach/detach/notify boilerplate; the intermediate `Subject` keeps observers off the concrete `Boss`. Note the deprecation warning and single-inheritance cost.

## Reference Tables
| Version | Subject side | Observer side | Result |
|---|---|---|---|
| 1. 双向耦合 | `Secretary` holds `List<StockObserver>` | `StockObserver` holds `Secretary` | Adding NBA watcher edits both classes |
| 2. 解耦实践一 | `Secretary` holds `List<Observer>` | `Observer` (abstract) holds `Secretary` | Half done: observers still tied to concrete notifier |
| 3. 解耦实践二 | `Subject` (abstract) holds `List<Observer>` | `Observer` holds `Subject` | Both sides abstract; Boss/Secretary interchangeable |
| 4. JDK `Observable` | `Subject extends Observable` | `implements Observer`, cast to `Subject` | Less code; single-inheritance limit; deprecated |

## Worked Example
**Story:** colleagues watch stock prices while the boss is out. Receptionist 童子喆 phones one of them when the boss returns; everyone scrambles. One day the boss walks in with 童子喆 in tow (she never got to phone), and 魏关姹, facing away, shouts "我的股票涨停了哦" straight into the boss's face.

**Version 1:** `Secretary` with `attach(StockObserver)`, `notifyEmployee()`, and `setAction("老板回来了")`; `StockObserver` holds a `Secretary` and prints her action on `update()`. Works, but the two classes reference each other concretely. Adding an NBA-watching colleague means modifying `Secretary`.

**Version 2:** introduce abstract `Observer` with `update()`; `StockObserver` and `NBAObserver` extend it; `Secretary` now holds `List<Observer>` and gains `detach()`. 大鸟: only half the job — `Observer` still holds a `Secretary`. What if the *boss* is the one who notifies?

**Version 3:** abstract `Subject` with `attach/detach/notifyEmployee/getAction/setAction`; `Boss` and `Secretary` both extend it. `Observer.sub` becomes `Subject`. Client: register three colleagues with `boss1`, `detach(employee1)` (魏关姹 is not reached), set the action, notify. Output shows two warnings; 魏关姹 gets none and is caught.

**Refinement:** the author then shows the pure structure (`subjectState`, `notifyObserver()`), argues an interface is the better `Observer` in practice, and demonstrates the JDK route — with an intermediate `Subject extends Observable` so `StockObserver` never sees `Boss`.

## Key Takeaways
1. Decouple *both* sides: subject → abstract observer *and* observer → abstract subject. Half a decoupling is still a coupling.
2. The subject must not know who or how many observers exist; it only iterates a list of the abstraction.
3. Provide `detach()`; subscriptions that can't be removed become leaks and stale notifications.
4. Use an interface for `Observer` when observers are unrelated classes; an abstract class only for shared code.
5. `java.util.Observable` saves boilerplate but costs your single inheritance slot and is deprecated; wrap it behind your own `Subject` or write your own.
6. Observer is 依赖倒转 in its purest form — the mechanism behind UI event handling in Swing/Android/Word.

## Connects To
- **[ch05](ch05-dependency-inversion.md)**: “这实在是依赖倒转原则的最佳体现” — both parties depend on abstractions.
- **[ch04](ch04-open-closed.md)**: the trigger for refactoring was that adding an `NBAObserver` required modifying `Secretary`.
- **[ch25](ch25-mediator.md)**: Mediator centralizes many-to-many communication; Observer handles one-to-many broadcast.
- **[ch16](ch16-state.md)**: state changes are often what a subject broadcasts.
- **[ch23](ch23-command.md)**: commands are frequently what observers enqueue in response to notifications.
- **[ch29](ch29-pattern-summary.md)**: Observer reaches the final five; MVC is mentioned as its most famous host.
