# 第9章：简历复印——原型模式（Prototype）

## 核心思想
当你需要许多大体相同的对象时，先创建一个，再克隆它并调整副本，而不是一遍遍地执行构造函数。故事是：复印一份简历打印二十份，而不是逐份手写。本章真正要讲的陷阱：Java 默认的 `clone()` 是浅复制，除非你把被引用的对象也一并克隆，否则它们会被共享。

## 引入的框架
- **原型模式（Prototype）** — “用原型实例指定创建对象的种类，并且通过复制这些原型创建新的对象。”[DP]
  - 结构：`Prototype { +clone() }`（声明自我克隆的接口）；`ConcretePrototype1/2 { +clone() }`（自行实现克隆）。在 Java 中抽象的 `Prototype` 并不必要：实现 `Cloneable` 并重写 `clone()` 即可。
  - 适用场景：对象初始化代价高昂，或初始状态稳定而你需要多个近乎相同的实例；你想捕获对象的运行时状态并重现它（"不用重新初始化对象，而是动态地获得对象运行时的状态"）。
  - 做法：(1) `class X implements Cloneable`；(2) 重写 `public X clone()`，在 `try/catch(CloneNotSupportedException)` 中调用 `super.clone()`；(3) 如果 `X` 持有必须相互独立的引用类型字段，就在 `clone()` 中把它们也克隆一份（深复制）；(4) 客户端调用 `x.clone()`，然后调整副本。
  - 为什么有效：`super.clone()` 绕过构造函数并按位复制字段，所以重复创建时不必再次执行昂贵的初始化。失败模式：浅复制共享被引用的对象，所以编辑一个副本会悄悄地编辑所有副本。
- **浅复制（shallow copy）**："被复制对象的所有变量都含有与原来的对象相同的值，而所有的对其他对象的引用都仍然指向原来的对象。" 这就是 `super.clone()` 给你的结果。
- **深复制（deep copy）**："把引用对象的变量指向复制过的新对象，而不是原有的被引用的对象." 你通过在 `clone()` 中克隆每个被引用的对象来实现它。要事先决定深度，并留意循环引用。

## 关键概念
- **Cloneable**：Java 的标记接口；没有它，`super.clone()` 会抛出 `CloneNotSupportedException`。
- **super.clone()**：按位复制值类型字段，复制引用时并不复制被引用的对象。
- **传引用 vs 传值**：`resume2 = resume1` 只是给同一个对象起了第二个名字，而不是第二份简历；这是本章第一个错误的捷径。
- **String 的特殊地位**：String 是引用类型，但在克隆时表现得像值，这就是第一版 `Resume` 碰巧「能用」的原因。
- **WorkExperience**：一旦 `Resume` 持有它，就会暴露浅复制缺陷的那个被引用对象。
- **深复制的层数**：要克隆多少层引用；事先决定，当心循环。

## 心智模型
- 把 `clone()` 想成复印：快，没有构造开销，但复印一页写着「见附页」的纸，指向的仍然是同一张附页。
- 对每个引用字段都问一句「副本需要自己的 X 吗？」；如果需要，就在 `clone()` 中克隆 X。
- 当初始化稳定且昂贵时，优先用 clone 而不是 `new`：每次 `new` 都会重新执行构造函数。
- 在代码里使用原型模式，但求职时别这么做：作者的收尾观点是，手写的求职信之所以显眼，恰恰因为大家都在复制。

## 反模式
- **N 个近乎相同的对象就实例化 N 次**：三份简历就是三次 `new Resume(...)`，附带相同的 setter 调用；一个笔误要改 N 次。
- **用赋值代替复制**：`Resume resume2 = resume1;` 共享同一个对象；三份「简历」都显示最后一次编辑。
- **带引用字段的浅克隆**：加入 `WorkExperience` 之后，三份克隆出的简历都显示最后一次 `setWorkExperience` 的内容，因为它们共享同一个 `WorkExperience` 实例。
- **无限制的深复制**：简历 → 经历 → 公司 → 职位 …；盲目克隆每一层代价高昂，还可能在循环引用上死循环。

## 代码示例
Java 中的教科书式原型：

```java
abstract class Prototype implements Cloneable {
    private String id;
    public Prototype(String id) { this.id = id; }
    public String getID() { return id; }
    public Object clone() {                       // the key of the pattern
        Object object = null;
        try { object = super.clone(); }
        catch (CloneNotSupportedException e) { System.err.println("Clone异常。"); }
        return object;
    }
}
class ConcretePrototype extends Prototype {
    public ConcretePrototype(String id) { super(id); }
}

ConcretePrototype p1 = new ConcretePrototype("编号123456");
ConcretePrototype c1 = (ConcretePrototype) p1.clone();   // no constructor run
```
- **演示了什么**：基于克隆的创建；在 Java 中，`Cloneable` + `clone()` 就是你所需要的全部。

简历的深复制（最终版本）：

```java
class WorkExperience implements Cloneable {
    private String timeArea, company;
    // getters/setters omitted
    public WorkExperience clone() {
        try { return (WorkExperience) super.clone(); }
        catch (CloneNotSupportedException e) { System.err.println("Clone异常。"); return null; }
    }
}

class Resume implements Cloneable {
    private String name, sex, age;
    private WorkExperience work;                 // reference-typed field
    public Resume(String name) { this.name = name; this.work = new WorkExperience(); }
    public void setPersonalInfo(String sex, String age) { this.sex = sex; this.age = age; }
    public void setWorkExperience(String timeArea, String company) {
        work.setTimeArea(timeArea); work.setCompany(company);
    }
    public void display() {
        System.out.println(name + " " + sex + " " + age);
        System.out.println("工作经历 " + work.getTimeArea() + " " + work.getCompany());
    }
    public Resume clone() {
        Resume object = null;
        try {
            object = (Resume) super.clone();
            object.work = this.work.clone();     // deep copy: give the copy its own WorkExperience
        } catch (CloneNotSupportedException e) { System.err.println("Clone异常。"); }
        return object;
    }
}

Resume resume1 = new Resume("大鸟");
resume1.setPersonalInfo("男", "29");
resume1.setWorkExperience("1998-2000", "XX公司");
Resume resume2 = resume1.clone();
resume2.setWorkExperience("2000-2003", "YY集团");
Resume resume3 = resume1.clone();
resume3.setPersonalInfo("男", "24");
resume3.setWorkExperience("2003-2006", "ZZ公司");
resume1.display(); resume2.display(); resume3.display();   // three different work histories
```
- **演示了什么**：一行代码（`object.work = this.work.clone()`）就把浅复制变成了深度为一层的深复制，这个示例只需要这些。

## 实战示例
1. **版本 1——手写时代**：`Resume` 只有 `String` 字段；客户端用相同的 setter 调用 `new Resume(...)` 三次。能用，但每次改动都要改 N 处。捷径 `resume2 = resume1` 被否决：那是传引用，三个名字指向同一个对象。
2. **版本 2——克隆**：`Resume implements Cloneable`，`clone()` 返回 `(Resume) super.clone()`。客户端每个副本克隆一次，只编辑不同的字段。能用，因为所有字段都是 `String`。
3. **出问题了——版本 3**：真实的设计会把 `WorkExperience` 提取为单独的类，以引用方式持有。客户端在每个克隆上设置不同的经历，但三者打印出的都是最后一个：浅复制共享了唯一的 `WorkExperience`。
4. **重构——版本 4（深复制）**：让 `WorkExperience` 可克隆，并在 `Resume.clone()` 内克隆它。同样的客户端代码现在打印出预期的三段经历。
5. **原因**：`super.clone()` 复制的是引用，而不是被引用者；深复制则把每个引用字段重新指向一个全新的副本。深度是一个设计决策：这里一层就够了。

## 关键要点
1. 当需要许多相似对象且初始化昂贵或稳定时，使用原型模式；克隆并调整，而不是重新执行构造函数。
2. 在 Java 中，原型 = `implements Cloneable` + 围绕 `super.clone()` 重写 `clone()`；不需要抽象的 `Prototype` 类。
3. `super.clone()` 是浅复制：值字段被复制，引用字段被共享。
4. 对每个引用字段，明确决定副本是否需要自己的实例；如果需要，就在 `clone()` 中克隆它。
5. 事先确定深复制的深度，并防范循环引用。
6. 赋值（`b = a`）绝不是复制。

## 关联章节
- **[ch08](ch08-factory-method.md)**：另一种创建型模式；工厂封装 `new`，原型则完全避免 `new`。
- **[ch18](ch18-memento.md)**：备忘录模式（Memento）同样捕获对象状态以备后用；原型模式复制整个对象，备忘录模式则把快照外部化。
- **[ch29](ch29-pattern-summary.md)**：原型小姐主张"建立相应数目的原型并克隆它们通常比每次用合适的状态手工实例化该类更方便"[DP]。
- **[ch00](ch00-oo-basics.md)**：值语义与引用语义是浅复制/深复制之分的基础。
