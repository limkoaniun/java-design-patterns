# 第28章：男人和女人——访问者模式（Visitor）

## 核心思想
当元素类型集合稳定、而作用于它们的操作不断变化时，把操作从元素中移出，放进访问者类；借助双分派，新增一个操作只需新增一个访问者，无需改动任何元素。

## 引入的框架
- **访问者模式（Visitor）** — “表示一个作用于某对象结构中的各元素的操作。它使你可以在不改变各元素的类的前提下定义作用于这些元素的新操作。”[DP]
  - 结构：`Visitor`（为每个具体元素声明一个 `visitConcreteElementX`）→ `ConcreteVisitor1/2`（各自实现全部访问操作，即算法在每个元素类上的一个片段）；`Element`（声明 `accept(Visitor)`）→ `ConcreteElementA/B`（通过调用 `visitor.visitConcreteElementX(this)` 实现 `accept`）；`ObjectStructure` 枚举其元素，并提供一个高层接口供访问者遍历这些元素。
  - 适用场景：“访问者模式适用于数据结构相对稳定的系统”；数据结构稳定，而作用于它的算法经常变化。作者的前提是：人类恰好只有两种性别，因此 `Visitor` 的方法列表（`getManConclusion`、`getWomanConclusion`）不会改变。
  - 做法：(1) 确认元素类型是固定的；(2) 让 `Visitor` 为每种元素类型提供一个抽象方法；(3) 每个元素的 `accept` 以 `this` 回调访问者；(4) 把同一个操作的相关行为放进同一个 `ConcreteVisitor`；(5) 增加一个 `ObjectStructure`，对所有元素运行访问者。
  - 为何有效 / 失效模式：其目的是“把处理从数据结构分离出来”；新增操作就是新增一个访问者。但新增元素类型会迫使 `Visitor` 及其所有子类都增加一个新方法，这违反了开放-封闭原则（OCP）。大鸟引用的 GoF 原话：大多数时候你并不需要访问者模式，但当你需要时，你是真的需要。

## 关键概念
- **双分派（double dispatch）**：被执行的操作同时取决于请求的种类和两个接收者的类型。客户端把一个具体的 `Action` 传给 `Man.accept`（第一次分派）；`Man` 调用 `visitor.getManConclusion(this)`（第二次分派）。
- **Element / ConcreteElement**：稳定的数据类型（`Person` → `Man`、`Woman`）。
- **Visitor / ConcreteVisitor**：不断变化的操作（`Action` → `Success`、`Failing`、`Amativeness`、`Marriage`）。
- **ObjectStructure**：持有各元素，并对每个元素应用访问者（`attach`、`detach`、`display`）。
- **稳定的数据结构**：决定访问者模式是否安全的唯一前提。
- **处理与数据结构分离**：该模式明确声明的目的；操作可以自由演化，而结构保持不动。

## 心智模型
- 问「哪个维度在变化？」：新增操作频繁、新增元素类型从不发生，则用访问者模式；新增元素类型频繁，则不要用。
- 把 `accept` 看作「我在这儿，你想怎么处理我都行」：元素把它具体的自己交给访问者。
- 把 `ConcreteVisitor` 看作一个完整的操作，分布在所有元素类型之上，与元素分开开发。
- 把元素类内部的 `if (action == "成功") ... else if ...` 视为坏味道：行为与数据结构紧耦合，每新增一个状态就要修改每一个元素。

## 反模式
- **元素内部的状态分支**：`Man.getConclusion` 对 `action` 做 `if/else`；新增结婚状态就得修改 `Man` 和 `Woman`。
- **在不稳定的结构上使用访问者模式**：出现第三种元素类型，就要给 `Visitor` 及其所有子类增加一个方法。
- **把访问者模式当作炫技**：作者指出程序员会滥用它来显摆面向对象功力；只在确实需要时才使用。
- **因其晦涩而回避它**：小菜的反方观点，多数人跳过访问者模式并非出于对滥用的担心，而是因为没有理解它。

## 代码示例
男人和女人对人生各种状态的反应，重构为访问者模式：

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
- **演示内容**：`Man.accept` 接收一个 `Action`（分派 1）并调用 `getManConclusion(this)`（分派 2）；新增 `Marriage` 不触动任何已有的类。GoF 的骨架使用 `Visitor.visitConcreteElementA/B`、`Element.accept`、`ObjectStructure.accept(visitor)`，形态相同。

## 实战示例
1. **版本 1**：六行 `System.out.println`，打印男女对比。大鸟：不比 Hello World 好多少。
2. **版本 2（朴素的面向对象）**：`Person` 带一个 `action` 字段和抽象的 `getConclusion`；`Man` 和 `Woman` 对 `action == "成功" / "失败" / "恋爱"` 做分支。客户端创建六个人并循环处理。它能工作，但新增结婚状态就要同时修改 `Man` 和 `Woman`；小菜希望把状态做成类，却看不出如何分派。
3. **版本 3（访问者模式）**：大鸟把两个维度对调。性别分类是稳定的（只有两种），所以 `Action` 可以放心地恰好声明 `getManConclusion` 和 `getWomanConclusion`。`Person.accept(Action)` 把 `this` 传回去。每个状态变成一个 `ConcreteVisitor`。`ObjectStructure` 持有一个 `Man` 和一个 `Woman`，并对两者运行任意访问者。
4. **对这一论断的检验**：新增 `Marriage extends Action`，调用 `o.display(new Marriage())`。其他文件都不用改。小菜：这就是把开放-封闭原则做到了极致。
5. **明确说出前提**：如果性别多于两种，每新增一种就要给 `Action` 及其所有子类增加一个方法。大鸟乐于用这个例子，原因在于人类的性别是一种不会变化的数据结构。
6. **清醒的收尾**：它是 GoF 中最复杂的模式，是一把双刃剑。只在确实需要时才使用。

## 关键要点
1. 当元素类型固定、而作用于它们的操作不断增多时，使用访问者模式；它让新增一个操作只需新增一个类。
2. 当很可能新增元素类型时，绝不要使用访问者模式；每新增一种都会波及每一个访问者。
3. 把 `accept` 实现为 `visitor.visitX(this)`；这个回调就是第二次分派，按元素类型和访问者类型两者共同选择行为。
4. 把一个操作的全部行为收拢到一个访问者中；它可以脱离元素独立开发，提高元素的独立性。
5. 提供一个 `ObjectStructure`，使访问者可以通过一次调用作用于整个集合。
6. 识别这种坏味道：数据类内部按类型或状态写的 `if/else` 链，就是与结构粘在一起的操作。

## 关联章节
- **[ch04](ch04-open-closed.md)**：收益（对新增操作开放）与局限（只有在元素不变时才是封闭的）。
- **[ch16](ch16-state.md)**：状态模式（State）同样消除状态分支，但方式是让对象自身的行为发生改变；访问者模式则把行为整个移出去。
- **[ch19](ch19-composite.md)**：`ObjectStructure` 常常就是一个组合模式（Composite）；访问者遍历它。
- **[ch20](ch20-iterator.md)**：`ObjectStructure.display` 中的遍历属于迭代关注点。
- **[ch29](ch29-pattern-summary.md)**：访问者模式在比赛中的答案，新增元素难，新增操作易。
