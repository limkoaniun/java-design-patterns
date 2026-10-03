# 第20章：想走？可以！先买票——迭代器模式（Iterator）

## 核心思想
把*如何遍历集合*与*集合本身是什么*分离：售票员用同一套 first/next/isDone/current 流程走遍公交车上的每位乘客（行李、老外、内部员工，甚至小偷），从不关心每个乘客是什么。Java 已经内置了这一模式（`Iterator`、`ListIterator`、`foreach`），所以它如今的价值更多在于学习而非实用。

## 引入的框架
- **迭代器模式（Iterator）** — “提供一种方法顺序访问一个聚合对象中的各个元素，而又不暴露该对象的内部表示。”[DP]
  - 适用场景：无论元素类型如何，都必须访问聚合对象中的每个元素；或者需要对同一聚合提供*多种*遍历顺序（从前往后、从后往前、排序）；或者希望不同聚合结构拥有统一的 start / next / done / current 接口。
  - 做法：(1) 声明抽象的 `Iterator`，包含 `first()`、`next()`、`isDone()`、`currentItem()`；(2) 声明抽象的 `Aggregate`，包含 `createIterator()`；(3) 每个 `ConcreteAggregate` 存放元素，并交出一个与自身绑定的 `ConcreteIterator`；(4) 客户端驱动迭代器，从不接触聚合的内部。
  - 结构：`Aggregate` ⟵ `ConcreteAggregate`；`Iterator` ⟵ `ConcreteIterator`、`ConcreteIteratorDesc`；`Client` 只与这两个抽象打交道。具体迭代器持有对具体聚合的引用以及一个游标索引。

## 关键概念
- **聚集（Aggregate）**：被遍历的容器；暴露 `createIterator()` 和元素访问方法，隐藏其存储方式。
- **具体迭代器（ConcreteIterator）**：持有指向某个聚合的游标（`current`），并实现四个遍历操作。
- **多种遍历方式**：把 `ConcreteIterator` 换成 `ConcreteIteratorDesc`，客户端只改一行就能反转顺序。
- **java.util.Iterator**：`hasNext()` / `next()`；简单的正向迭代。
- **java.util.ListIterator**：增加 `hasPrevious()` / `previous()`；双向迭代；通过 `list.listIterator(list.size())` 获取即可从末尾开始。
- **foreach**：对 `iterator()` + `hasNext()`/`next()` 的编译器语法糖；你看不到迭代器，但确实用到了一个。
- **不暴露内部表示**：客户端看到的是元素，而不是背后的 `ArrayList`（或数组、数据库游标）。

## 心智模型
- 把迭代器想象成**公交车售票员**：乘客是聚合；售票员的流程（从前面开始、下一个、查完了吗、我前面是谁）无论车上是什么都一样。
- 需要第二种遍历顺序时，就用第二个具体迭代器；客户端只改一处 `new`。
- 把 GoF 的迭代器模式当作**值得研究的历史**：“研究历史是为了更好地迎接未来” —— 现代语言已将它折叠进 `foreach`，所以要学习它的结构，才能理解语言替你做了什么。
- 优先使用语言自带的 `Iterator`/`ListIterator` 接口，而不是手写抽象类；它们更精简、支持泛型，GoF 版本能做的它们都能做。

## 反模式
- **暴露集合的内部**（向客户端返回原始 `ArrayList`，或在客户端里做索引运算）：每个客户端都因此依赖于存储选择，存储一变就会出错。
- **以「一个具体迭代器就够了」为由跳过抽象**：一旦需要反向或带过滤的遍历，就必须重写客户端，而不是换一个迭代器。
- **在生产环境的 Java 中手写迭代器模式**：Martin Fowler 甚至提议让该模式退役；请使用 `Iterable`/`Iterator` 和 `foreach`。

## 代码示例
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
- **演示内容**：正序与倒序遍历的客户端循环完全相同；只有所构造的迭代器不同，而且客户端从未见过 `ArrayList`。

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
- **演示内容**：`foreach`、`Iterator` 和 `ListIterator` 就是已经内置于 `java.util` 的该模式。

## 实战示例
1. **朴素做法**：客户端用索引循环直接遍历乘客列表，因此它知道这个列表是 `ArrayList`，并且要为反向顺序重写循环。
2. **问题所在**：售票员的职责（访问每个人、不漏一个、知道何时结束）在每个遍历处都重复一遍，存储或顺序的任何变化都会波及每一个循环。
3. **重构**：引入 `Aggregate`/`Iterator` 抽象；`ConcreteAggregate` 把 `ArrayList` 藏在 `getCount()`/`getCurrentItem(i)` 之后；`ConcreteIterator` 持有游标；客户端调用 `first()`，检测 `isDone()`，读取 `currentItem()`，再调用 `next()`。
4. **扩展**：反向遍历只需新增一个 `ConcreteIteratorDesc`，并在客户端改一行（`new ConcreteIteratorDesc(bus)`）。
5. **原因**：遍历行为被分离到独立的类中，因此聚合的内部保持隐藏，客户端可以透明地访问元素。随后作者指出，Java 的 `Iterator`/`ListIterator`/`foreach` 正是同一设计的改进版和泛型版。

## 关键要点
1. 当必须遍历聚合而不关心元素是什么，或者需要多种遍历顺序时，使用迭代器模式。
2. 四个操作（first、next、isDone、currentItem）构成统一接口；具体迭代器只在游标逻辑上有所不同。
3. 即使只有一个实现也要保留迭代器抽象；这样反向或过滤顺序只需增加一个类和一处 `new`。
4. 在 Java 中，使用 `Iterable`/`Iterator`/`ListIterator` 和 `foreach`；编译器会为你生成迭代器协议。
5. 学习 GoF 的结构是为了理解语言特性，而不是去重新实现它。

## 关联章节
- **[ch19](ch19-composite.md)**：组合模式（Composite）的树是迭代器模式统一遍历的经典聚合。
- **[ch29](ch29-pattern-summary.md)**：作者的比赛总结把迭代器模式列入行为型模式，并指出其实用价值在下降。
- **[ch00](ch00-oo-basics.md)**：泛型和集合（`ArrayList<T>`）是内置实现的基础。
- **Java Collections Framework**：`Iterable`、`Iterator`、`ListIterator` 是该模式的生产化形态。
