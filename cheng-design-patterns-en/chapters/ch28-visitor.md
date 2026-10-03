# Chapter 28: 男人和女人——访问者模式 — Visitor

## Core Idea
When the set of element types is stable but the operations on them keep changing, move the operations out of the elements into visitor classes; double dispatch lets you add a new operation as one new visitor without touching any element.

## Frameworks Introduced
- **访问者模式 (Visitor)** — “表示一个作用于某对象结构中的各元素的操作。它使你可以在不改变各元素的类的前提下定义作用于这些元素的新操作。”[DP]
  - Structure: `Visitor` (declares one `visitConcreteElementX` per concrete element) → `ConcreteVisitor1/2` (each implements every visit operation, one fragment of an algorithm per element class); `Element` (declares `accept(Visitor)`) → `ConcreteElementA/B` (implement `accept` by calling `visitor.visitConcreteElementX(this)`); `ObjectStructure` enumerates its elements and offers a high-level interface for a visitor to traverse them.
  - When to use: “访问者模式适用于数据结构相对稳定的系统”; the data structure is stable and the algorithms over it change often. The author's precondition: humanity has exactly two sexes, so the `Visitor` method list (`getManConclusion`, `getWomanConclusion`) will not change.
  - How: (1) confirm the element types are fixed; (2) give `Visitor` one abstract method per element type; (3) each element's `accept` calls back the visitor with `this`; (4) put related behaviour for one operation into one `ConcreteVisitor`; (5) add an `ObjectStructure` to run a visitor over all elements.
  - Why it works / failure mode: the purpose is “把处理从数据结构分离出来”; adding an operation means adding one visitor. But adding an element type forces a new method on `Visitor` and every subclass, which violates 开放-封闭. GoF's own line, quoted by 大鸟: most of the time you do not need Visitor, but when you do, you really do.

## Key Concepts
- **双分派 (double dispatch)**: the executed operation depends on both the request kind and two receivers' types. Client passes a concrete `Action` to `Man.accept` (first dispatch); `Man` calls `visitor.getManConclusion(this)` (second dispatch).
- **Element / ConcreteElement**: the stable data types (`Person` → `Man`, `Woman`).
- **Visitor / ConcreteVisitor**: the changing operations (`Action` → `Success`, `Failing`, `Amativeness`, `Marriage`).
- **ObjectStructure**: holds the elements and applies a visitor to each (`attach`, `detach`, `display`).
- **稳定的数据结构**: the single precondition that decides whether Visitor is safe.
- **处理与数据结构分离**: the pattern's stated purpose; operations evolve freely while structure stays put.

## Mental Models
- Ask "which axis changes?": new operations often, new element types never → Visitor. New element types often → do not.
- Think of `accept` as "here I am, do your thing with me": the element hands its concrete self to the visitor.
- Think of a `ConcreteVisitor` as one complete operation spread across all element types, developed separately from the elements.
- Treat `if (action == "成功") ... else if ...` inside element classes as the smell: behaviour and data structure tightly coupled, every new state edits every element.

## Anti-patterns
- **State branches inside elements**: `Man.getConclusion` with `if/else` on `action`; adding 结婚 means editing `Man` and `Woman`.
- **Visitor over an unstable structure**: a third element type forces a method on `Visitor` and all its subclasses.
- **Visitor as a showpiece**: the author notes programmers misuse it to display OO prowess; use it only when truly needed.
- **Avoiding it because it is obscure**: 小菜's counterpoint, most people skip Visitor not from fear of misuse but from not understanding it.

## Code Examples
Men and women reacting to life states, refactored to Visitor:

```java
// Visitor: one method per stable element type
abstract class Action {
    public abstract void getManConclusion(Man concreteElementA);
    public abstract void getWomanConclusion(Woman concreteElementB);
}
// Element
abstract class Person {
    public abstract void accept(Action visitor);
}
// ConcreteVisitor
class Success extends Action {
    public void getManConclusion(Man m) {
        System.out.println(m.getClass().getSimpleName() + " " + this.getClass().getSimpleName()
            + "时，背后多半有一个伟大的女人。");
    }
    public void getWomanConclusion(Woman w) {
        System.out.println(w.getClass().getSimpleName() + " " + this.getClass().getSimpleName()
            + "时，背后大多有一个不成功的男人。");
    }
}
class Failing extends Action { /* 代码类似，省略 */ }
class Amativeness extends Action { /* 代码类似，省略 */ }
// ConcreteElement: second dispatch happens here
class Man extends Person {
    public void accept(Action visitor) { visitor.getManConclusion(this); }
}
class Woman extends Person {
    public void accept(Action visitor) { visitor.getWomanConclusion(this); }
}
// ObjectStructure
class ObjectStructure {
    private ArrayList<Person> elements = new ArrayList<Person>();
    public void attach(Person element) { elements.add(element); }
    public void detach(Person element) { elements.remove(element); }
    public void display(Action visitor) {
        for (Person e : elements) e.accept(visitor);
    }
}
// Client
ObjectStructure o = new ObjectStructure();
o.attach(new Man());
o.attach(new Woman());
o.display(new Success());
o.display(new Failing());
o.display(new Amativeness());
// New operation = one new class, nothing else changes
class Marriage extends Action {
    public void getManConclusion(Man m) { /* 恋爱游戏终结时，'有妻徒刑'遥无期 */ }
    public void getWomanConclusion(Woman w) { /* 爱情长跑路漫漫，婚姻保险保平安 */ }
}
o.display(new Marriage());
```
- **What it demonstrates**: `Man.accept` receives an `Action` (dispatch 1) and calls `getManConclusion(this)` (dispatch 2); adding `Marriage` touches no existing class. The GoF skeleton uses `Visitor.visitConcreteElementA/B`, `Element.accept`, `ObjectStructure.accept(visitor)` with the same shape.

## Worked Example
1. **Version 1**: six `System.out.println` lines printing the men/women contrasts. 大鸟: no better than Hello World.
2. **Version 2 (plain OO)**: `Person` with an `action` field and abstract `getConclusion`; `Man` and `Woman` branch on `action == "成功" / "失败" / "恋爱"`. The client builds six persons and loops. It works, but adding a 结婚 state means editing both `Man` and `Woman`; 小菜 wants states as classes but cannot see how to dispatch.
3. **Version 3 (Visitor)**: 大鸟 flips the axes. The sex classification is stable (only two), so `Action` can safely declare exactly `getManConclusion` and `getWomanConclusion`. `Person.accept(Action)` passes `this` back. Each state becomes a `ConcreteVisitor`. `ObjectStructure` holds a `Man` and a `Woman` and runs any visitor over both.
4. **Test of the claim**: add `Marriage extends Action`, call `o.display(new Marriage())`. No other file changes. 小菜: this is 开放-封闭 done perfectly.
5. **The precondition, stated explicitly**: if there were more than two sexes, every new one would add a method to `Action` and all subclasses. The reason 大鸟 was happy to use this example is that human sex is a data structure that does not change.
6. **Sobering close**: it is GoF's most complex pattern, a double-edged sword. Use it only when you actually need it.

## Key Takeaways
1. Use Visitor when the element types are fixed and the operations over them keep growing; it makes adding an operation one new class.
2. Never use Visitor when new element types are likely; each one ripples through every visitor.
3. Implement `accept` as `visitor.visitX(this)`; that callback is the second dispatch that selects behaviour by both element and visitor type.
4. Gather all behaviour for one operation into one visitor; it can be developed apart from the elements, raising their independence.
5. Provide an `ObjectStructure` so a visitor can be applied across the whole collection with one call.
6. Recognise the smell: type-or-state `if/else` chains inside data classes are operations glued to structure.

## Connects To
- **[ch04](ch04-open-closed.md)**: the payoff (open to new operations) and the limit (closed only if elements do not change).
- **[ch16](ch16-state.md)**: State also removes state branches, but by letting the object's own behaviour change; Visitor moves behaviour out entirely.
- **[ch19](ch19-composite.md)**: `ObjectStructure` is often a Composite; visitors traverse it.
- **[ch20](ch20-iterator.md)**: traversal in `ObjectStructure.display` is an iteration concern.
- **[ch29](ch29-pattern-summary.md)**: 访问者's contest answer, adding elements is hard, adding operations is easy.
