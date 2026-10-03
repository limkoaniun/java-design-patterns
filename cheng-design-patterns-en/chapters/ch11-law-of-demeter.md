# Chapter 11: 无熟人难办事？——迪米特法则 — Law of Demeter (Least Knowledge)

## Core Idea
A class should talk only to the classes it must talk to, through the narrowest interface possible. Route requests through an intermediary (the "IT 部主管") instead of depending on whichever concrete colleague you happen to know.

## Frameworks Introduced
- **迪米特法则 (Law of Demeter, LoD)，也叫最少知识原则** — “如果两个类不必彼此直接通信，那么这两个类就不应当发生直接的相互作用。如果其中一个类需要调用另一个类的某一个方法的话，可以通过第三者转发这个调用。”[J&DP]
  - Premise the author stresses first: “在类的结构设计上，每一个类都应当尽量降低成员的访问权限”[J&DP] — wrap private state; expose nothing other classes do not need.
  - Root idea: “迪米特法则其根本思想，是强调了类之间的松耦合。” The weaker the coupling, the easier reuse; modifying a weakly coupled class does not ripple. “信息的隐藏促进了软件的复用。”
  - Story analogy: 小菜's first day at work — he only knew 小张 in the IT 部 (introduced by HR 小杨); when 小张 was called away nobody else would install his PC, because "有事只能找认识的人，对方无空就办不了事". With an IT 部主管 (or simply "call the IT department"), any free technician gets assigned and 小菜 need not know anyone.
  - When to use: whenever a class reaches into another class's collaborators, or when a caller must know *which* concrete object does the work.
  - How: (1) Make fields and helpers `private` by default; expose only what callers need. (2) Insert a coordinator/abstraction (department, manager, facade) between a caller and a set of workers. (3) Let callers depend on the abstraction ("IT 部"), not on a person ("小张").

## Key Concepts
- **最少知识 (least knowledge)**: a class knows as little as possible about the structure of other classes.
- **第三者转发 (forwarding via a third party)**: if A must invoke B, an intermediary can relay the call so A and B are not directly coupled.
- **降低成员访问权限**: keep state `private`; publish only what must be public, usually through properties/getters.
- **松耦合 (loose coupling)**: the principle's underlying goal; weak coupling means a change in one class does not propagate to its neighbors.
- **信息隐藏 (information hiding)**: promotes reuse; the principle and encapsulation reinforce each other rather than conflicting.
- **IT 部 as abstraction**: the department is the abstract class/interface; 小张 and 小李 are concrete classes. Callers should address the abstraction.

## Mental Models
- Think of every direct dependency on a concrete collaborator as "needing to know someone personally"; if that person is busy or leaves, you are stuck.
- Use a "department" (interface, manager, facade) when a caller would otherwise need to know several interchangeable workers.
- "Don't talk to strangers": a method should call methods on itself, its fields, its parameters, or objects it created — not on objects fetched from those.
- If a class exposes internals that other classes then navigate, you have a coupling chain; hide the internals and offer a single operation instead.

## Anti-patterns
- **靠关系办事 (depending on personal acquaintance)**: `小菜 → 小张` hard-coded. When 小张 is unavailable, the request fails even though 小李 could do it. In code: a class depending on one concrete implementation when any implementation of the abstraction would do.
- **No coordinator among workers**: "一个和尚挑水吃，两个和尚抬水吃，三个和尚没水吃" — with two or more interchangeable workers and no manager/abstraction, callers must pick one, leading to pushing work around.
- **Over-exposed members**: public fields and helper methods invite other classes to depend on your internals, which locks your implementation in place.

## Code Examples
The chapter is diagram-driven and contains no listing; the two figures are reconstructed here in sketch form.

```java
// Before: caller coupled to a specific worker
class XiaoCai {
    private XiaoZhang zhang;                 // knows a person
    void getPc() { zhang.installPc(); }      // fails if zhang is busy
}

// After: caller talks to the department; the department assigns work
interface ItDepartment { void installPc(Employee who); }

class ItManager implements ItDepartment {    // the third party that forwards the call
    private List<Technician> staff;          // 小张, 小李 ...
    public void installPc(Employee who) {
        staff.stream().filter(Technician::isFree).findFirst()
             .orElse(staff.get(0)).installPc(who);
    }
}

class XiaoCai {
    private ItDepartment it;                 // knows only the abstraction
    void getPc() { it.installPc(this); }
}
```
- **What it demonstrates**: the caller's knowledge shrinks to one abstraction; which technician does the job is decided behind it.

## Worked Example
**Situation:** 小菜 arrives, HR 小杨 introduces him to 小张 in IT. 小张 gets an urgent call and leaves. 小菜 spends the day waiting; 小李 refuses because the form names 小张, and 小杨 is too busy to re-route. The PC is installed half an hour before closing.

**Diagnosis (大鸟):** the failure is not bad luck but a missing layer. 小菜 depended on a *concrete* person; the company had no IT 主管 to allocate tasks and no rule for "whoever is free handles it and reports later".

**Fix, in three levels of coupling:**
1. Know both 小张 and 小李 — works, but 小菜 must maintain relationships with every worker (dependence on every concrete class).
2. Know only the IT 主管 — one dependency; the manager forwards to whoever is free (the "third party" in the LoD definition).
3. Know only "IT 部" — the abstraction; staff can change entirely and 小菜's request still works ("哪怕里面的人都离职换了新人，我的电脑出问题也还是可以找IT部解决").

Level 3 is both 依赖倒转 (program to the interface) and 迪米特 (know the minimum). The chapter ends with 小菜 realizing the two principles are complementary, not competing.

## Key Takeaways
1. Default every member to `private`; publish only what other classes genuinely need.
2. If A does not *have* to talk to B, it should not; route through an intermediary that owns the relationship.
3. Depend on the department, not the person: address abstractions, so concrete collaborators can change or be replaced.
4. Loose coupling is the goal; LoD is a practical rule for spotting where coupling is too tight.
5. LoD and encapsulation are the same instinct at two scales — hide state inside a class, hide collaborators behind an abstraction.

## Connects To
- **[ch05](ch05-dependency-inversion.md)**: 依赖倒转原则; "call IT 部 instead of 小张" is programming to an interface.
- **[ch12](ch12-facade.md)**: Facade is the pattern-shaped embodiment of LoD — one entry point that hides a subsystem's classes.
- **[ch25](ch25-mediator.md)**: Mediator applies LoD to a web of peers by making them talk only to a central coordinator.
- **[ch00](ch00-oo-basics.md)**: 封装 is the class-level foundation this principle builds on.
- **[ch29](ch29-pattern-summary.md)**: 迪米特 sits on the judging panel; several patterns cite her when explaining their decoupling.
