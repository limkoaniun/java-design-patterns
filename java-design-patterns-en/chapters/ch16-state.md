# Chapter 16: 无尽加班何时休——状态模式 — State

## Core Idea
When an object's behaviour depends on its state and the state-transition logic has become a long chain of `if/else`, move each state into its own class and let the states hand control to each other. The "Long Method" smell is the trigger; the pattern is the cure.

## Frameworks Introduced
- **状态模式 (State)** — “当一个对象的内在状态改变时允许改变其行为，这个对象看起来像是改变了其类。”[DP]
  - Structure: `Context` (holds `state`, exposes `request()` which calls `state.handle(this)`) ↔ `State` (abstract `handle(Context)`) ← `ConcreteStateA`, `ConcreteStateB` (each implements one state's behaviour and sets the *next* state on the context).
  - When to use: "当一个对象的行为取决于它的状态，并且它必须在运行时刻根据状态改变它的行为时"; or when a business object has several enumerated states driven by large multi-branch conditionals.
  - How: (1) find the `Long Method` full of state checks; (2) make an abstract `State` with the behaviour method taking the context; (3) one subclass per state, each doing its work *or* switching the context to the next state and re-dispatching; (4) `Context` keeps `current`, delegates, and exposes the data states need (`hour`, `workFinished`).
- **Long Method 坏味道** — Martin Fowler's smell from 《重构》; a long method with many branches "责任过大", violating 单一职责 and 开放-封闭 at once.

## Key Concepts
- **State (抽象状态类)**: "定义一个接口以封装与Context的一个特定状态相关的行为".
- **ConcreteState (具体状态)**: "每一个子类实现一个与Context的一个状态相关的行为".
- **Context**: "维护一个ConcreteState子类的实例，这个实例定义当前的状态".
- **状态转移逻辑分布 (distributed transition logic)**: each ConcreteState decides its own successor, so no single place knows the whole state machine.
- **行为局部化 (localised behaviour)**: "将与特定状态相关的行为局部化，并且将不同状态的行为分割开来"[DP].
- **活字 vs 刻版**: the author's recurring image — a big `if` block is a carved printing plate; state classes are movable type.
- **Re-dispatch after transition**: `w.setState(new NoonState()); w.writeProgram();` — the new state immediately handles the same request.

## Mental Models
- Think of each state class as **one row of the state table**, owning both "what I do" and "when I hand off".
- Use State when the *same* method call must behave differently over time; use Strategy when the *caller* picks the algorithm up front.
- If the state test is a single simple `if`, do not use the pattern: "如果这个状态判断很简单，那就没必要用状态模式了".
- Ask "which lines change when the rule changes?" — with State the answer is one class, not one giant method.

## Anti-patterns
- **Procedural first draft**: static `hour`/`workFinished` globals plus a static `writeProgram()` — no object at all.
- **One class, one giant method**: `Work.writeProgram()` with nested `if (hour < 12) … else if … else { if (workFinished) … }` — every rule change edits the whole method and risks breaking unrelated branches.
- **Encoding a new rule by adding another branch**: the "must leave by 20:00" requirement should touch only the evening state, not the method that handles all hours.
- **Applying State to a two-branch conditional**: over-engineering; the pattern earns its cost only when the conditional is complex.

## Code Examples
Generic structure:
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
- **What it demonstrates**: the context never branches; each state names its successor.

The overtime program, state-pattern version:
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
- **What it demonstrates**: the client code is unchanged from the branchy version, but each rule lives in one small class.

## Worked Example
小菜 describes his day: sharp in the morning, sleepy at noon, recovering in the afternoon, exhausted on overtime, asleep after 21:00 unless the task is done.

1. **Version 1 (函数版)**: static fields `hour` and `workFinished`, one static `writeProgram()` with nested conditionals. 大鸟: "怎么还在写面向过程的代码？"
2. **Version 2 (分类版)**: wrap it in `class Work` with `hour`/`workFinished` properties. Same `writeProgram()` body — object-oriented in form only.
3. **Diagnosis**: `writeProgram` is a Long Method. It owns every state and every transition, so it violates 单一职责; a new rule ("everyone leaves by 20:00") forces edits to the whole method, so it violates 开放-封闭.
4. **Version 3 (状态模式版)**: `State` with abstract `writeProgram(Work)`; six concrete states (`Forenoon`, `Noon`, `Afternoon`, `Evening`, `Sleeping`, `Rest`); `Work` holds `current`, initialised to `ForenoonState`, and delegates. Each state either prints or transitions and re-dispatches.
5. **Payoff check**: the 20:00 rule now means adding a `ForcedOffState` and editing only `EveningState`'s condition. No other state is touched, and the client code did not change at all.

Why it works: transitions are spread across the states ("把各种状态转移逻辑分布到State的子类之间"), so each class is small, and adding or reordering states is local.

## Key Takeaways
1. A long method whose branches test the object's own state is the signal for State — not merely "there is an `if`".
2. Give the abstract state the *behaviour* method (`writeProgram`), not a generic `handle`, and pass the context so states can read data and set the next state.
3. Let states re-dispatch after a transition so one call resolves to the right behaviour regardless of the starting state.
4. The context initialises the first state and delegates; it must not branch on state itself.
5. Verify the design with a new requirement: if it touches one state class only, the pattern is doing its job.
6. Skip the pattern when the conditional is simple; State adds classes and is only worth it against real complexity.

## Connects To
- **[ch03](ch03-single-responsibility.md)**, **[ch04](ch04-open-closed.md)**: the Long Method is diagnosed by exactly these two principles.
- **[ch02](ch02-strategy.md)**: same class shape (context + abstract + concretes); the difference is who chooses — the client (Strategy) or the states themselves (State).
- **[ch24](ch24-chain-of-responsibility.md)**: also passes a request along a sequence of objects, but the chain is fixed by the client, whereas states choose their own successors.
- **[ch29](ch29-pattern-summary.md)**: the contest's behavioural group compares State with its siblings.
- **Refactoring (Fowler)**: "Long Method" and "Replace Conditional with State/Strategy" are the named refactorings behind this chapter.
