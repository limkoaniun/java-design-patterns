# Chapter 0: 楔子 培训实习生——面向对象基础 — Prologue: OO Fundamentals via the "Animal Sports Meet"

## Core Idea
Object-oriented programming is not syntax; it is a discipline for locating behaviour in the right place so that duplication disappears and change stays local. The author teaches encapsulation, inheritance, polymorphism, abstract classes and interfaces by evolving one tiny program (a cat that meows) into a polymorphic "动物运动会" (animal sports meet), refactoring at every step of duplication.

## Frameworks Introduced
- **类与实例 (Class and Instance)** — “类就是具有相同的属性和功能的对象的抽象的集合”; an instance is “一个真实的对象”, created with `new`.
  - When to use: whenever a function (e.g. `shout()`) lives in a place it does not belong ("the neighbourhood TV in your living room"), extract a class.
  - How: class name capitalised; expose only `public` members; instantiate then call.
- **构造方法 (Constructor)** — same name as class, no return type, runs on `new`; every class gets an empty default one until you define your own.
- **方法重载 (Method overloading)** — “创建同名的多个方法的能力，但这些方法需使用不同的参数类型”. Use it to add capability without touching an existing method (e.g. `Cat()` and `Cat(String name)`).
- **属性与修饰符 (Properties and modifiers)** — a field is private storage; a property is the `get/set` pair that guards it. `public` = anyone, `private` = same class only, `protected` = subclasses too. Doors and windows (public) versus walls (private).
- **封装 (Encapsulation)** — “每个对象都包含它能进行操作所需要的所有信息”. Three payoffs: lower coupling, freedom to change internals, a clear public interface.
- **继承 (Inheritance)** — models an **is-a** relationship. Three rules: a subclass owns the parent's non-private members; it can add its own; it can override the parent's behaviour. Cost: “父类变，则子类不得不变”, and it exposes parent internals (strong coupling). Only inherit for is-a, never for has-a (a hand does not inherit a person).
- **多态 (Polymorphism)** — “不同的对象可以执行相同的动作，但要通过它们自己的实现代码来执行”. The Peking-opera analogy: the son performs *as* the father (subclass appears as parent type), in his own way (override), and may not show his own tricks while doing so (subclass-only members are invisible through the parent reference). Declare as parent, instantiate as child; binding is by runtime type [AMNFP].
- **抽象类 (Abstract class)** — cannot be instantiated; abstract methods must be overridden; any class with an abstract method is abstract. Rule of thumb: “抽象类拥有尽可能多的共同代码，拥有尽可能少的数据” [J&DP]; in an inheritance tree “树叶节点应当是具体类，而树枝节点均应当是抽象类” [J&DP].
- **接口 (Interface)** — “把隐式公共方法和属性组合起来，以封装特定功能的一个集合”; no fields, no constructors, no bodies; a class may implement many.
- **集合与泛型 (Collections and generics)** — `ArrayList` grows on demand but is not type-safe and boxes value types; `ArrayList<T>` fixes both. Prefer generic collections.

## Key Concepts
- **字段 vs 属性 (field vs property)**: a field stores data privately; a property is the controlled public access to it.
- **耦合 (Coupling)**: "藕断丝连", two classes whose changes drag each other. Inheritance is a strongly coupled relationship.
- **方法重写 (Override)**: subclass replaces the parent's implementation with its own.
- **is-a vs has-a**: is-a justifies inheritance; has-a calls for composition.
- **装箱/拆箱 (Boxing/unboxing)**: wrapping a value type into `Object` and back; expensive, avoided by generics.
- **重构 (Refactoring)**: improve existing code's design when duplication appears, not before.

## Mental Models
- **Abstract classes are found bottom-up, interfaces are designed top-down.** Cat and Dog existed first; `Animal` was *generalised* out of them by refactoring. Interfaces (the power socket, the sports-meet event list) are defined before any implementer exists.
- **Use an abstract class for similar things, an interface for a behaviour that crosses unrelated things.** Cats and dogs share an `Animal` parent; a plane, a sparrow and Superman share only `IFly`.
- **Think of `protected` as "family-only".** Data the subclass needs (name, shoutNum) is protected; everything else stays private.
- **Designing `Animal` when you only have `Cat` is over-design.** Wait for the second class, then extract.

## Anti-patterns
- **Dog extends Cat because the code looks similar**: now every future cat behaviour (climb trees, catch mice) leaks into Dog. Similarity of code is not an is-a relationship.
- **Ctrl+C / Ctrl+V reuse**: five animal classes with 90% identical bodies; a one-word change to the shout format means five edits.
- **Putting "变出东西" on `Animal` so polymorphism works**: forces every animal to own a behaviour only three special ones have. Use an interface instead.
- **Public fields instead of properties**: "windows without screens": anyone can write anything at any time.
- **Fixed-size arrays for a growing roster**: `new Animal[5]` caps registration arbitrarily; use a generic list.

## Code Examples
The end state of the refactoring: an abstract parent holding all shared behaviour, subclasses supplying only what differs.

```java
public abstract class Animal {
    protected String name = "";
    protected int shoutNum = 3;

    public Animal(String name) { this.name = name; }
    public Animal()            { this.name = "无名"; }

    public void setShoutNum(int value) { this.shoutNum = value; }
    public int  getShoutNum()          { return this.shoutNum; }

    // Template: shared loop, varying sound supplied by subclass
    public String shout() {
        String result = "";
        for (int i = 0; i < this.shoutNum; i++) {
            result += getShoutSound() + ", ";
        }
        return "我的名字叫" + name + " " + result;
    }
    protected abstract String getShoutSound();
}

public class Cat extends Animal {
    public Cat()            { super(); }
    public Cat(String name) { super(name); }
    protected String getShoutSound() { return "喵"; }
}

public class Dog extends Animal {
    public Dog()            { super(); }
    public Dog(String name) { super(name); }
    protected String getShoutSound() { return "汪"; }
}
```
- **What it demonstrates**: inheritance removes duplication; polymorphism lets `Animal` references dispatch to `Cat`/`Dog`; the abstract `getShoutSound()` is the seed of the Template Method pattern (ch10).

Interfaces for a behaviour that crosses unrelated classes, plus the generic-collection client:

```java
public interface IChange {
    String changeThing(String thing);
}

public class MachineCat extends Cat implements IChange {
    public MachineCat(String name) { super(name); }
    public String changeThing(String thing) {
        return super.shout() + "，我有万能的口袋，我可变出" + thing;
    }
}

// Client: declare as parent/interface, instantiate as child
ArrayList<Animal> arrayAnimal = new ArrayList<Animal>();
arrayAnimal.add(new Cat("小花"));
arrayAnimal.add(new Dog("阿毛"));
for (Animal item : arrayAnimal) {
    System.out.println(item.shout());   // runtime type decides 喵 or 汪
}

IChange[] array = { new MachineCat("叮当"), new StoneMonkey("孙悟空") };
System.out.println(array[0].changeThing("各种各样的东西"));
```
- **What it demonstrates**: `ArrayList<Animal>` rejects `add(123)` at compile time and needs no cast in the loop; `IChange` lets a cat and a monkey be treated uniformly without polluting `Animal`.

## Reference Tables
| | 抽象类 Abstract class | 接口 Interface |
|---|---|---|
| Can hold implementation | Yes (partial) | No |
| Multiple per class | One | Many |
| Abstracts | The whole class (fields, properties, methods) | A behaviour (a slice of the class) |
| Design direction | Bottom-up: generalised from existing subclasses by refactoring | Top-down: defined before implementers are known |
| Use when | Objects are similar kinds (cat, dog → animal) | Unrelated objects share a behaviour (plane, sparrow, Superman → IFly) |

| | 数组 Array | `ArrayList` | `ArrayList<T>` |
|---|---|---|---|
| Size | Fixed at creation | Grows on demand | Grows on demand |
| Type safety | Yes | No (everything is `Object`) | Yes |
| Boxing cost | None | Boxes value types | None |
| Verdict | Fine for fixed sets | "太老土" once generics exist | Default choice |

## Worked Example
The author walks one program through eight refactorings:
1. **Naive**: `System.out.println("喵")` inline in `main`. Needing a second meow means copy-paste.
2. **Function**: extract `shout()`. Still lives in `Test`, the wrong home.
3. **Class**: `Cat` with `public String shout()`; client does `Cat cat = new Cat(); cat.shout();`.
4. **Constructor + overload**: `Cat(String name)` so the cat is born named; add `Cat()` defaulting to "无名" so unnamed cats are still possible.
5. **Property**: `shoutNum` as a private field with `setShoutNum`/`getShoutNum`, letting the setter clamp values (`if (value <= 10) ... else 10`): the "screen on the window".
6. **Second class breaks it**: `Dog` is a copy of `Cat` with one string changed. Extract `Animal` (name, shoutNum, property methods) and have both `extends Animal`, calling `super(name)`.
7. **Polymorphism for the sports meet**: `Animal[] arrayAnimal` filled with cats and dogs; `arrayAnimal[i].shout()` dispatches per runtime type. Add `Cattle` and `Sheep` and the loop still needs no change.
8. **Remaining duplication**: the loop inside each `shout()` is identical. Move `shout()` up to `Animal`, leave only `getShoutSound()` abstract, declare `Animal` abstract because "an animal" cannot be instantiated. Subclasses shrink to a constructor and one line.

Then two extensions: `IChange` for 叮当/孙悟空 (behaviour that must not live on `Animal`), and `ArrayList<Animal>` replacing the five-slot array so registrations and withdrawals (`remove(1)`) work without index arithmetic surprises (after one removal, later elements shift, so removing index 1 twice removes two consecutive dogs).

Why it matters: every step was triggered by a concrete duplication or a concrete new need. Nothing was abstracted speculatively.

## Key Takeaways
1. Extract a class when a function has no natural home; extract a parent when two classes share a body.
2. Inherit only for is-a; for has-a, compose. "Dog extends Cat" is the canonical mistake.
3. Declare variables as the parent or interface type, instantiate the concrete type: that is what makes polymorphism work.
4. Leaf classes concrete, branch classes abstract; an abstract class carries maximum shared code and minimum data.
5. Abstract classes emerge from refactoring; interfaces are designed ahead of their implementers.
6. Default to `ArrayList<T>`; raw `ArrayList` trades type safety and boxing cost for nothing.
7. Without design patterns, understanding of polymorphism "多半都是肤浅和片面的": this chapter is the entry ticket, not the destination.

## Connects To
- **[ch01](ch01-simple-factory.md)**: the calculator applies these same three features (encapsulation, inheritance, polymorphism) to a business problem.
- **[ch10](ch10-template-method.md)**: the `shout()`/`getShoutSound()` split in step 8 *is* Template Method; the author says so explicitly.
- **[ch05](ch05-dependency-inversion.md)**: "declare as parent, instantiate as child" becomes the formal principle of programming to abstractions.
- **[ch22](ch22-bridge.md)**: the is-a versus has-a warning here becomes the 合成/聚合复用原则.
- **GoF / UML**: class, interface, generalisation and realisation notation is formalised in ch01 §1.11.
