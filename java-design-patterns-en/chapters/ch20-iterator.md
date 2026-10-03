# Chapter 20: 想走？可以！先买票——迭代器模式 — Iterator

## Core Idea
Separate *how a collection is traversed* from *what the collection is*: a conductor walks every passenger on the bus (luggage, foreigner, staff, even the thief) with the same first/next/isDone/current routine, never caring what each one is. Java already ships this pattern (`Iterator`, `ListIterator`, `foreach`), so its value today is more educational than practical.

## Frameworks Introduced
- **迭代器模式 (Iterator)** — “提供一种方法顺序访问一个聚合对象中的各个元素，而又不暴露该对象的内部表示。”[DP]
  - When to use: you must visit every element of an aggregate regardless of element type; or you need *several* traversal orders (front-to-back, back-to-front, sorted) over the same aggregate; or you want a uniform start / next / done / current interface across different aggregate structures.
  - How: (1) declare an abstract `Iterator` with `first()`, `next()`, `isDone()`, `currentItem()`; (2) declare an abstract `Aggregate` with `createIterator()`; (3) each `ConcreteAggregate` stores items and hands out a `ConcreteIterator` bound to itself; (4) the client drives the iterator and never touches the aggregate's internals.
  - Structure: `Aggregate` ⟵ `ConcreteAggregate`; `Iterator` ⟵ `ConcreteIterator`, `ConcreteIteratorDesc`; `Client` talks only to the two abstractions. The concrete iterator holds a reference to the concrete aggregate plus a cursor index.

## Key Concepts
- **聚集 (Aggregate)**: the container being traversed; exposes `createIterator()` and item access, hides its storage.
- **具体迭代器 (ConcreteIterator)**: owns a cursor (`current`) into one aggregate and implements the four traversal operations.
- **多种遍历方式**: swapping `ConcreteIterator` for `ConcreteIteratorDesc` reverses order with a one-line client change.
- **java.util.Iterator**: `hasNext()` / `next()`; simple forward iteration.
- **java.util.ListIterator**: adds `hasPrevious()` / `previous()`; bidirectional iteration; obtain via `list.listIterator(list.size())` to start from the end.
- **foreach**: compiler sugar over `iterator()` + `hasNext()`/`next()`; you never see the iterator but one is used.
- **不暴露内部表示**: the client sees elements, not the `ArrayList` (or array, or DB cursor) behind them.

## Mental Models
- Think of the iterator as the **bus conductor**: the passengers are the aggregate; the conductor's routine (start at the front, next, are we done, who is in front of me) is the same whatever is on the bus.
- Use a second concrete iterator when you need a second traversal order; the client changes one `new`.
- Treat GoF Iterator as **history worth studying**: “研究历史是为了更好地迎接未来” — modern languages folded it into `foreach`, so learn the structure to understand what the language does for you.
- Prefer the language's `Iterator`/`ListIterator` interfaces over hand-rolled abstract classes; they are leaner, generic, and do everything the GoF version does.

## Anti-patterns
- **Exposing the collection's internals** (returning the raw `ArrayList` or index arithmetic in the client): every client now depends on the storage choice and breaks when it changes.
- **Skipping the abstraction “because one concrete iterator is enough”**: the moment a reverse or filtered traversal is needed, the client must be rewritten instead of swapping an iterator.
- **Re-implementing Iterator by hand in production Java**: Martin Fowler even proposed retiring the pattern; use `Iterable`/`Iterator` and `foreach`.

## Code Examples
```java
// 聚集抽象类
abstract class Aggregate {
    public abstract Iterator createIterator();
}
// 迭代器抽象类
abstract class Iterator {
    public abstract Object first();
    public abstract Object next();
    public abstract boolean isDone();
    public abstract Object currentItem();
}
// 具体聚集类
class ConcreteAggregate extends Aggregate {
    private ArrayList<Object> items = new ArrayList<Object>();
    public Iterator createIterator() { return new ConcreteIterator(this); }
    public int getCount() { return items.size(); }
    public void add(Object object) { items.add(object); }
    public Object getCurrentItem(int index) { return items.get(index); }
}
// 具体迭代器类（正序）
class ConcreteIterator extends Iterator {
    private ConcreteAggregate aggregate;
    private int current = 0;
    public ConcreteIterator(ConcreteAggregate aggregate) { this.aggregate = aggregate; }
    public Object first() { return aggregate.getCurrentItem(0); }
    public Object next() {
        Object ret = null;
        current++;
        if (current < aggregate.getCount()) ret = aggregate.getCurrentItem(current);
        return ret;
    }
    public boolean isDone() { return current >= aggregate.getCount(); }
    public Object currentItem() { return aggregate.getCurrentItem(current); }
}
// 倒序迭代器：只改 first/next/isDone 的方向
class ConcreteIteratorDesc extends Iterator {
    private ConcreteAggregate aggregate;
    private int current;
    public ConcreteIteratorDesc(ConcreteAggregate aggregate) {
        this.aggregate = aggregate;
        current = aggregate.getCount() - 1;
    }
    public Object first() { return aggregate.getCurrentItem(aggregate.getCount() - 1); }
    public Object next() {
        Object ret = null;
        current--;
        if (current >= 0) ret = aggregate.getCurrentItem(current);
        return ret;
    }
    public boolean isDone() { return current < 0; }
    public Object currentItem() { return aggregate.getCurrentItem(current); }
}
// 客户端：售票员遍历公交车
ConcreteAggregate bus = new ConcreteAggregate();
bus.add("大鸟"); bus.add("小菜"); bus.add("行李");
bus.add("老外"); bus.add("公交内部员工"); bus.add("小偷");
Iterator conductor = new ConcreteIterator(bus);      // 换成 new ConcreteIteratorDesc(bus) 即倒序
conductor.first();
while (!conductor.isDone()) {
    System.out.println(conductor.currentItem() + "，请买车票!");
    conductor.next();
}
```
- **What it demonstrates**: the client loop is identical for forward and reverse traversal; only the iterator constructed changes, and the client never sees the `ArrayList`.

```java
// Java 内置实现
ArrayList<String> bus = new ArrayList<String>();
bus.add("大鸟"); bus.add("小菜"); bus.add("行李"); bus.add("老外");
for (String item : bus) {                              // foreach = 隐式 Iterator
    System.out.println(item + "，请买车票!");
}
Iterator<String> conductor = bus.iterator();           // 显式正序
while (conductor.hasNext()) System.out.println(conductor.next() + "，请买车票!");
ListIterator<String> desc = bus.listIterator(bus.size()); // 逆向
while (desc.hasPrevious()) System.out.println(desc.previous() + "，请买车票!");
```
- **What it demonstrates**: `foreach`, `Iterator`, and `ListIterator` are the pattern already built into `java.util`.

## Worked Example
1. **Naive**: the client walks the passenger list directly with an index loop, so it knows the list is an `ArrayList` and rewrites the loop for reverse order.
2. **What broke**: the conductor's job (visit everyone, skip nobody, know when done) is duplicated wherever traversal happens, and any change in storage or order ripples into every loop.
3. **Refactor**: introduce `Aggregate`/`Iterator` abstractions; `ConcreteAggregate` hides the `ArrayList` behind `getCount()`/`getCurrentItem(i)`; `ConcreteIterator` owns the cursor; the client asks `first()`, tests `isDone()`, reads `currentItem()`, calls `next()`.
4. **Extend**: reverse traversal is a new `ConcreteIteratorDesc` and a one-line change in the client (`new ConcreteIteratorDesc(bus)`).
5. **Why**: traversal behaviour is separated into its own class, so the aggregate's internals stay hidden and clients access elements transparently. The author then shows that Java's `Iterator`/`ListIterator`/`foreach` are the same design already improved and generified.

## Key Takeaways
1. Use Iterator when you must traverse an aggregate without caring what the elements are, or when multiple traversal orders are needed.
2. The four operations (first, next, isDone, currentItem) are the uniform interface; concrete iterators vary only the cursor logic.
3. Keep the iterator abstraction even with one implementation; a reverse/filtered order then costs one class and one `new`.
4. In Java, use `Iterable`/`Iterator`/`ListIterator` and `foreach`; the compiler generates the iterator protocol for you.
5. Learn the GoF structure to understand the language feature, not to reimplement it.

## Connects To
- **[ch19](ch19-composite.md)**: Composite trees are the classic aggregate that Iterator walks uniformly.
- **[ch29](ch29-pattern-summary.md)**: the author's contest summary lists Iterator among the behavioural patterns and notes its declining practical value.
- **[ch00](ch00-oo-basics.md)**: generics and collections (`ArrayList<T>`) underpin the built-in implementation.
- **Java Collections Framework**: `Iterable`, `Iterator`, `ListIterator` are the productionised form of this pattern.
