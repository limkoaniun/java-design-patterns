# 第13章：好菜每回味不同——建造者模式（Builder）

## 核心思想
当一个对象必须通过一套稳定的步骤来组装、而各步骤的细节随产品而异时，把构建过程（Director）与部件构建（Builder）分离，这样任何一步都不会被遗漏，客户端也看不到这些步骤。麦当劳在哪儿味道都一样，因为流程是固定的；路边摊忘了放盐。

## 引入的框架
- **建造者模式（Builder），又叫生成器模式** — “将一个复杂对象的构建与它的表示分离，使得同样的构建过程可以创建不同的表示。”[DP]
  - 结构：`Builder`（抽象接口，声明每个部件步骤 `buildPartA()`、`buildPartB()` 以及 `getResult()`）→ `ConcreteBuilder`（实现这些步骤，组装并返回一个 `Product`）；`Director`（通过 `construct(Builder)` 按固定顺序调用建造者的各个步骤）；`Product`（复杂对象，例如部件列表）。
  - 何时使用：“主要用于创建一些复杂的对象，这些对象内部子对象的建造顺序通常是稳定的，但每个子对象本身的构建通常面临着复杂的变化。” 另外：“当创建复杂对象的算法应该独立于该对象的组成部分以及它们的装配方式时”。
  - 做法：(1) 列出必需的部件（头、身体、两条手臂、两条腿）。(2) 在 `Builder` 中为每个部件声明一个抽象方法。(3) 每个 `ConcreteBuilder`（瘦、胖、高）实现所有部件——编译器会拒绝漏了一条腿的建造者。(4) `Director.construct()` 按顺序调用各步骤。(5) 客户端挑选一个建造者，交给 Director，然后调用 `getResult()`。
  - 为何有效：流程被锁定在一处（Director），因此变化被限制在部件细节上；增加一种产品表示只需新增一个 ConcreteBuilder。失效模式：建造者的步骤过于针对某个产品——作者提醒 Builder 的方法“必须要足够普遍”，这样所有具体建造者才都能实现它们。

## 关键概念
- **构建 vs. 表示（construction vs. representation）**：组装部件的*过程*，与组装好的部件*长什么样*。
- **指挥者（Director）**：控制建造顺序，并把客户端与之隔离；“也用它来隔离用户与建造过程的关联”。
- **稳定的过程，变化的细节**：过程（头、身体、手臂、腿）是稳定的；细节（胖、瘦、高）是变化的。
- **产品 Product**：由多个部件组装而成；在基础代码中是一个持有 `ArrayList<String> parts` 的 `Product`。
- **抽象方法强制完整性**：由于每个部件都是抽象方法，漏掉一个的具体建造者无法通过编译——即「盐是必需的」这一保证。
- **粒度权衡（granularity trade-off）**：只有当*每个*具体产品都需要时，才增加更细的步骤（五官、上臂/前臂）。

## 心智模型
- 把 Director 看作快餐店的标准作业流程：盐多少克、加热多少分钟。客户端点的是「一个汉堡」，从不接触配方。
- 当客户端应当说出*要什么*（瘦小人/胖小人）而不应触及*怎么做*（绘制调用的顺序）时，使用建造者模式。
- 当变化的部件构建应当是注入的对象，而不是流程所有者的子类时，优先选建造者模式而非模板方法模式（Template Method）。
- 问一句「漏掉一个步骤会是 bug 吗？」如果是，这个步骤就应该放进由编译器强制检查的 Builder 接口。

## 反模式
- **所有绘制都塞在一个 `paint()` 里**（`Test.java` 中硬编码的 `drawOval`/`drawLine` 调用）：别处无法复用，而且第二份拷贝（胖小人）立刻掉了一条腿。
- **各产品一个类、没有共享流程**（`PersonThinBuilder`、`PersonFatBuilder` 各自带一个庞大的 `build()`）：可以复用，但没有任何机制阻止新的 `PersonTallBuilder` 漏掉一条手臂——盐的问题没有解决。
- **客户端自己调用部件方法**（`gThin.buildHead(); gThin.buildBody(); ...`）：客户端于是知道了流程；缺少 Director，意味着每个客户端都要重新编码这个顺序，也可能出错。
- **步骤列表过于通用或过于具体**：并非所有产品共有的步骤会让每个建造者臃肿；步骤过粗又会掩盖真实的变化。

## 代码示例
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
- **演示内容**：客户端指定产品；编译器保证完整性；Director 保证顺序。

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
- **演示内容**：结构图中的四个角色；同一个 `construct()` 配合不同的建造者产生不同的产品。

## 参考表
| 版本 | 流程在哪里 | 可复用？ | 部件会被遗漏吗？ |
|---|---|---|---|
| 1. `paint()` 中的绘制调用 | 客户端 | 否 | 会（胖小人丢了一条腿） |
| 2. 每个产品一个 `PersonThinBuilder.build()` | 各个产品类 | 是 | 会（没有任何机制强制六个部件） |
| 3. `PersonBuilder` + `PersonDirector` | 抽象建造者（部件）+ Director（顺序） | 是 | 不会（编译器 + Director） |

## 实战示例
**故事：** 大鸟点了蛋炒饭（没味道），又点了炒面（没放盐）。麦当劳/肯德基在哪儿味道都一样，因为流程是标准化的；路边摊的品质取决于厨师的心情。小菜把这件事联系到依赖倒转原则（DIP）：饭菜依赖厨师（细节）。而在快餐连锁店，饭菜依赖稳定的工作流程，具体的食材和时间则依赖这个工作流程。

**任务：** 画一个火柴人，有头、身体、两条手臂、两条腿。

1. **版本1：** 小菜把六个 `Graphics` 调用直接写进 `Test.paint()`。被要求画个胖的，他复制了这段代码，改了坐标，结果忘了一条腿。
2. **版本2：** 提取出 `PersonThinBuilder` 和 `PersonFatBuilder`，各自用 `build()` 完成全部六个调用。可以在任何地方复用，但将来的 `PersonTallBuilder` 仍然可能丢掉一条肢体。
3. **版本3：** `PersonBuilder` 声明六个抽象部件方法；具体建造者必须全部实现，否则编译失败。`PersonDirector.createPerson()` 按顺序调用它们。客户端写 `new PersonDirector(new PersonFatBuilder(g)).createPerson()`。

**扩展：** 高个和矮个的小人只是再多两个子类；客户端和 Director 都不用动。增加五官或前臂/上臂的细节需要判断——只有当每个小人都需要时，才往抽象建造者里加步骤。

## 关键要点
1. 把组装的*顺序*（Director）与每个部件的*内容*（ConcreteBuilder）分开。
2. 让每个必需的部件都成为抽象方法，这样不完整就是编译错误，而不是运行时的意外。
3. 客户端应当指定一个建造者并接收一个产品；它们永远不该自己调用部件方法。
4. 当构建顺序稳定而部件细节差异很大时，建造者模式最能发挥作用；如果顺序本身会变化，就去别处找办法。
5. 让建造者的步骤足够通用，使所有具体建造者都能实现；不要把某一个产品的怪癖编码进接口。

## 关联章节
- **[ch10](ch10-template-method.md)**：模板方法模式通过继承固定步骤顺序；建造者模式则通过驱动注入建造者的 Director 来固定。
- **[ch15](ch15-abstract-factory.md)**：抽象工厂模式（Abstract Factory）创建部件的产品系列；建造者模式则一步步组装一个复杂产品。
- **[ch05](ch05-dependency-inversion.md)**：「饭菜依赖厨师」这一观察就是依赖倒转原则——依赖流程抽象，而不是具体的执行者。
- **[ch08](ch08-factory-method.md)**：两者都是创建型；创建单个对象用工厂方法模式（Factory Method），对象有多个必需部件时用建造者模式。
- **[ch29](ch29-pattern-summary.md)**：建造者模式向评委解释了内聚/耦合——内部高内聚，外部接触少。
