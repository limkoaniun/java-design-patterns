# 第10章：考题抄错会做也白搭——模板方法模式（Template Method）

## 核心思想
当多个子类共享同一串步骤、只在少数细节上不同，就把整个步骤序列提升到父类中作为模板方法，让有差异的步骤保持抽象。试卷由老师印一次，学生只需填写答案。

## 引入的框架
- **模板方法模式（Template Method）** — “定义一个操作中的算法的骨架，而将一些步骤延迟到子类中。模板方法使得子类可以不改变一个算法的结构即可重定义该算法的某些特定步骤。”[DP]
  - 结构：`AbstractClass`（持有具体的 `templateMethod()`，给出顶层骨架并调用抽象的 `primitiveOperation1()`、`primitiveOperation2()`）→ `ConcreteClass`（实现这些原语操作；每个抽象类可以有任意多个具体类）。
  - 适用场景：“当我们要完成在某一细节层次一致的一个过程或一系列步骤，但其个别步骤在更详细的层次上的实现可能不同时”。流程在高层相同，但部分步骤因子类而异。
  - 做法：(1) 在超类中把共享流程写成一个具体方法，只写一次。(2) 把子类之间的每个差异点提取为模板所调用的抽象（或可重写）方法。(3) 子类只重写这些钩子。(4) 客户端把变量声明为超类类型，让多态分派到正确的钩子。
  - 为何有效 / 失效模式：它把不变行为集中到一处，所以流程变化只需改一次。失效模式：把太多东西塞进模板（处处都设钩子）会重新造成它本要消除的僵化；只为真正变化的步骤设钩子。

## 关键概念
- **算法骨架（algorithm skeleton）**：步骤的固定顺序，由超类拥有。
- **templateMethod**：超类中的具体方法，按顺序调用各原语操作；子类不重写它。
- **primitiveOperation（钩子步骤）**：代表一个可变步骤的抽象方法；每个子类提供自己的实现。
- **不变行为搬移到超类**：作者对该模式价值的一句话总结：把不变行为上移，消除子类中的重复代码。
- **顶级逻辑**：顶层逻辑；它也可以调用普通的具体方法，不限于抽象方法。

## 心智模型
- 把模板想成印好的试卷：每个人拿到相同的题目，答案是唯一的空白。
- 当「流程相同，但某一步的内容不同」，且你已经有了有意义的继承关系时，使用模板方法模式。
- 一旦选择了继承，父类就应当是其子类的*模板*：凡是在多个子类中重复的代码都属于父类。
- Java 类库就是这样把共同行为提取到抽象类中的；你很可能已经在不知不觉中用过这个模式。

## 反模式
- **复制粘贴的兄弟类**（`TestPaperA`、`TestPaperB` 各自打印完整题目文本）：重复 = 易错 + 难改。如果老师改了一道题，两份副本都要改，而且会有学生抄错。
- **只提升一半的继承**：子类先调用 `super.testQuestion1()` 再打印自己的答案。共享的那行 `System.out.println("答案：...")` 仍在重复，只有字母不同。当子类中*只剩*真正变化的内容时才停手。
- **把客户端变量声明为子类**（`TestPaperA studentA = new TestPaperA()`）：这会丢掉多态复用；应声明为 `TestPaper`。

## 代码示例
```java
// 金庸小说考题试卷 — the template
abstract class TestPaper {
    public void testQuestion1() {
        System.out.println("杨过得到，后来给了郭靖，炼成倚天剑、屠龙刀的玄铁可能是[ ] "
            + "a.球磨铸铁 b.马口铁 c.高速合金钢 d.碳素纤维");
        System.out.println("答案: " + this.answer1());
    }
    protected abstract String answer1();   // only this varies per student

    public void testQuestion2() { /* question text */ System.out.println("答案: " + this.answer2()); }
    protected abstract String answer2();

    public void testQuestion3() { /* question text */ System.out.println("答案: " + this.answer3()); }
    protected abstract String answer3();
}

class TestPaperA extends TestPaper {
    protected String answer1() { return "b"; }
    protected String answer2() { return "a"; }
    protected String answer3() { return "c"; }
}

class TestPaperB extends TestPaper {
    protected String answer1() { return "d"; }
    protected String answer2() { return "b"; }
    protected String answer3() { return "a"; }
}

// client: declare as the parent type
TestPaper studentA = new TestPaperA();
studentA.testQuestion1(); studentA.testQuestion2(); studentA.testQuestion3();
TestPaper studentB = new TestPaperB();
studentB.testQuestion1(); studentB.testQuestion2(); studentB.testQuestion3();
```
- **演示内容**：每个 `testQuestionN()` 都是模板方法；`answerN()` 是被延迟的原语操作。

```java
// Generic structure
abstract class AbstractClass {
    public void templateMethod() {       // skeleton, shared by all subclasses
        this.primitiveOperation1();
        this.primitiveOperation2();
    }
    public abstract void primitiveOperation1();   // subclass-specific behavior
    public abstract void primitiveOperation2();
}
class ConcreteClassA extends AbstractClass {
    public void primitiveOperation1() { System.out.println("具体类A方法1实现"); }
    public void primitiveOperation2() { System.out.println("具体类A方法2实现"); }
}
```
- **演示内容**：结构图中经典的 `AbstractClass` / `ConcreteClass` 角色。

## 实战示例
**版本1（抄试卷）：** 两个互不相关的类 `TestPaperA` 和 `TestPaperB`，各自带有 `testQuestion1..3()`，打印完整题目文本再打印自己的答案。除了三个字母之外，其余全部重复。抄错一道题（大鸟小时候把「3 看成 8」）会让整份答案作废，而且任何题目变更都必须在每个类里修改。

**版本2（初步泛化）：** 提取一个持有题目文本的父类 `TestPaper`；`TestPaperA`/`B` 继承它，各自的重写方法先调用 `super.testQuestion1()` 再打印 `"答案: b"`。有所改善，但 `super` 调用和 `"答案:"` 打印行仍然在每个子类里重复，客户端也仍然声明子类类型。

**版本3（模板方法）：** 把 `TestPaper` 改为抽象类；每个 `testQuestionN()` 打印题目*以及* `"答案: " + answerN()`，其中 `answerN()` 是 `protected abstract`。子类缩减为三个单行的 `return "b";` 方法。客户端只需把声明类型改为 `TestPaper`，即可获得多态复用。增加第三个学生只需一个很小的类；修改一道题只需在父类中改一处。

为何有效：不变部分（题目 + 打印格式）现在只存在于一处，而且编译器会强制每个学生填写每一道题的答案。

## 关键要点
1. 如果两个子类除了几行之外长得一样，共享的那些行就属于父类，并包装成模板方法。
2. 持续抽象，直到子类里*只剩*变化的内容；残留的 `super.x()` 调用说明你停得太早。
3. 把客户端变量声明为抽象类型，让模板以多态方式分派。
4. 模板方法模式是继承最常见的价值所在；类库正是用它来共享行为。
5. 模板的步骤顺序由父类固定；子类可以改变某一步*做什么*，但不能改变它*是否*运行或*何时*运行。

## 关联章节
- **[ch13](ch13-builder.md)**：建造者模式（Builder）的 `Director` 同样固定一个步骤序列，但是通过合成一个建造者对象，而不是通过继承钩子。
- **[ch08](ch08-factory-method.md)**：工厂方法模式（Factory Method）是一种模板方法，其被延迟的步骤是「创建哪个对象」。
- **[ch22](ch22-bridge.md)** / **合成/聚合复用原则（CARP）**：当变化的行为应当能在运行时替换时，优先选择策略模式（Strategy，见 [ch02](ch02-strategy.md)）而不是子类钩子。
- **[ch29](ch29-pattern-summary.md)**：行为型模式第一组；评委把模板方法模式评为最简单的复用平台。
