# Chapter 13: 好菜每回味不同——建造者模式 — Builder

## Core Idea
When an object must be assembled through a stable sequence of steps whose details vary by product, separate the construction process (Director) from the part-building (Builder) so no step can be forgotten and the client never sees the steps. McDonald's tastes the same everywhere because the process is fixed; the street stall forgot the salt.

## Frameworks Introduced
- **建造者模式 (Builder)，又叫生成器模式** — “将一个复杂对象的构建与它的表示分离，使得同样的构建过程可以创建不同的表示。”[DP]
  - Structure: `Builder` (abstract interface declaring each part step `buildPartA()`, `buildPartB()` and `getResult()`) → `ConcreteBuilder` (implements the steps, assembles and returns a `Product`); `Director` (calls the builder's steps in the fixed order via `construct(Builder)`); `Product` (the complex object, e.g. a list of parts).
  - When to use: “主要用于创建一些复杂的对象，这些对象内部子对象的建造顺序通常是稳定的，但每个子对象本身的构建通常面临着复杂的变化。” Also: “当创建复杂对象的算法应该独立于该对象的组成部分以及它们的装配方式时”.
  - How: (1) List the mandatory parts (head, body, two arms, two legs). (2) Declare one abstract method per part in `Builder`. (3) Each `ConcreteBuilder` (thin, fat, tall) implements every part — the compiler rejects a builder that forgets a leg. (4) `Director.construct()` calls the steps in order. (5) Client picks a builder, hands it to the Director, then calls `getResult()`.
  - Why it works: the process is locked in one place (Director), so variation is confined to part details; adding a product representation is one new ConcreteBuilder. Failure mode: builder steps that are too product-specific — the author warns the Builder's methods “必须要足够普遍” so all concrete builders can implement them.

## Key Concepts
- **构建 vs. 表示 (construction vs. representation)**: the *process* of assembling parts versus what the assembled parts look like.
- **指挥者 (Director)**: controls the build order and isolates the client from it; “也用它来隔离用户与建造过程的关联”.
- **稳定的过程，变化的细节**: the process (head, body, arms, legs) is stable; the details (fat, thin, tall) vary.
- **产品 Product**: assembled from multiple parts; in the base code a `Product` holding an `ArrayList<String> parts`.
- **抽象方法强制完整性**: because every part is an abstract method, a concrete builder that omits one fails to compile — the "salt is mandatory" guarantee.
- **粒度权衡 (granularity trade-off)**: add finer steps (五官, 上臂/前臂) only if *every* concrete product needs them.

## Mental Models
- Think of the Director as the fast-food SOP: grams of salt, minutes of heat. The client orders "a burger", never the recipe.
- Use Builder when the client should say *what* (瘦小人/胖小人) and never *how* (the sequence of draw calls).
- Prefer Builder over Template Method when the varying part-building should be an injected object rather than a subclass of the process owner.
- Ask "would forgetting a step be a bug?" If yes, that step belongs in a Builder interface enforced by the compiler.

## Anti-patterns
- **All drawing in one `paint()`** (`Test.java` with hard-coded `drawOval`/`drawLine` calls): not reusable anywhere else, and the second copy (胖小人) immediately dropped a leg.
- **Per-product classes without a shared process** (`PersonThinBuilder`, `PersonFatBuilder` each with a monolithic `build()`): reusable, but nothing stops a new `PersonTallBuilder` from omitting an arm — the salt problem is unsolved.
- **Client calling part methods itself** (`gThin.buildHead(); gThin.buildBody(); ...`): the client now knows the process; a missing Director means every client re-encodes the order and can get it wrong.
- **Over-generic or over-specific step lists**: steps not shared by all products bloat every builder; steps too coarse hide real variation.

## Code Examples
```java
// Abstract builder: the mandatory parts of a 小人
abstract class PersonBuilder {
    protected Graphics g;
    public PersonBuilder(Graphics g) { this.g = g; }
    public abstract void buildHead();
    public abstract void buildBody();
    public abstract void buildArmLeft();
    public abstract void buildArmRight();
    public abstract void buildLegLeft();
    public abstract void buildLegRight();
}

class PersonThinBuilder extends PersonBuilder {
    public PersonThinBuilder(Graphics g) { super(g); }
    public void buildHead()     { g.drawOval(150, 120, 30, 30); }
    public void buildBody()     { g.drawRect(160, 150, 10, 50); }
    public void buildArmLeft()  { g.drawLine(160, 150, 140, 200); }
    public void buildArmRight() { g.drawLine(170, 150, 190, 200); }
    public void buildLegLeft()  { g.drawLine(160, 200, 145, 250); }
    public void buildLegRight() { g.drawLine(170, 200, 185, 250); }   // omit this and it won't compile
}
// PersonFatBuilder: same six methods, drawOval(245,150,40,50) for the body, wider limbs

// Director: owns the order, hides it from the client
class PersonDirector {
    private PersonBuilder pb;
    public PersonDirector(PersonBuilder pb) { this.pb = pb; }
    public void createPerson() {
        pb.buildHead(); pb.buildBody();
        pb.buildArmLeft(); pb.buildArmRight();
        pb.buildLegLeft(); pb.buildLegRight();
    }
}

// Client (inside JFrame.paint)
public void paint(Graphics g) {
    new PersonDirector(new PersonThinBuilder(g)).createPerson();
    new PersonDirector(new PersonFatBuilder(g)).createPerson();
}
```
- **What it demonstrates**: the client names a product; the compiler guarantees completeness; the Director guarantees order.

```java
// Generic base code
class Product {
    private List<String> parts = new ArrayList<>();
    public void add(String part) { parts.add(part); }
    public void show() { parts.forEach(System.out::println); }
}
abstract class Builder {
    public abstract void buildPartA();
    public abstract void buildPartB();
    public abstract Product getResult();
}
class ConcreteBuilder1 extends Builder {
    private Product product = new Product();
    public void buildPartA() { product.add("部件A"); }
    public void buildPartB() { product.add("部件B"); }
    public Product getResult() { return product; }
}
class Director {
    public void construct(Builder builder) { builder.buildPartA(); builder.buildPartB(); }
}
// client
Director director = new Director();
Builder b1 = new ConcreteBuilder1();
director.construct(b1);
Product p1 = b1.getResult();
p1.show();
```
- **What it demonstrates**: the four roles of the structure diagram; the same `construct()` yields different products from different builders.

## Reference Tables
| Version | Where the process lives | Reusable? | Can a part be forgotten? |
|---|---|---|---|
| 1. Draw calls in `paint()` | Client | No | Yes (the fat man lost a leg) |
| 2. `PersonThinBuilder.build()` per product | Each product class | Yes | Yes (nothing enforces the six parts) |
| 3. `PersonBuilder` + `PersonDirector` | Abstract builder (parts) + Director (order) | Yes | No (compiler + Director) |

## Worked Example
**Story:** 大鸟 orders fried rice (bland), then fried noodles (no salt). McDonald's/KFC taste identical everywhere because the process is standardized; the street stall's quality depends on the cook's mood. 小菜 links this to 依赖倒转: the meal depends on the cook (a detail). At the fast-food chain, the meal depends on a stable workflow, and the concrete ingredients/times depend on that workflow.

**Task:** draw a stick figure with head, body, two arms, two legs.

1. **Version 1:** 小菜 writes the six `Graphics` calls straight into `Test.paint()`. Asked for a fat one, he copies the block, changes coordinates, and forgets a leg.
2. **Version 2:** extract `PersonThinBuilder` and `PersonFatBuilder`, each with `build()` doing all six calls. Reusable from anywhere, but a future `PersonTallBuilder` can still lose a limb.
3. **Version 3:** `PersonBuilder` declares six abstract part methods; concrete builders must implement all six or fail compilation. `PersonDirector.createPerson()` calls them in order. The client writes `new PersonDirector(new PersonFatBuilder(g)).createPerson()`.

**Extending:** tall and short figures are two more subclasses; the client and Director are untouched. Adding facial features or forearm/upper-arm detail is a judgment call — add steps to the abstract builder only if every figure needs them.

## Key Takeaways
1. Separate the *order* of assembly (Director) from the *content* of each part (ConcreteBuilder).
2. Make every mandatory part an abstract method so incompleteness is a compile error, not a runtime surprise.
3. Clients should specify a builder and receive a product; they should never call part methods themselves.
4. Builder shines when the build sequence is stable but part details vary widely; if the sequence itself varies, look elsewhere.
5. Keep builder steps general enough for all concrete builders; don't encode one product's quirks in the interface.

## Connects To
- **[ch10](ch10-template-method.md)**: Template Method fixes a step order via inheritance; Builder fixes it via a Director that drives an injected builder.
- **[ch15](ch15-abstract-factory.md)**: Abstract Factory creates families of parts; Builder assembles a complex product step by step.
- **[ch05](ch05-dependency-inversion.md)**: the "meal depends on the cook" observation is 依赖倒转 — depend on the process abstraction, not the concrete worker.
- **[ch08](ch08-factory-method.md)**: both are creational; use Factory Method for one object, Builder when the object has several mandatory parts.
- **[ch29](ch29-pattern-summary.md)**: 建造者 explains 内聚/耦合 to the judges — high internal cohesion, small external contact.
