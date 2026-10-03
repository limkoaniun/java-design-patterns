# 第1章：代码无错就是优？——简单工厂模式（"Bug-free equals good?": Simple Factory）

## 核心思想
输出正确只是最低要求。面试中的计算器程序被拒，是因为它不是可维护、可复用、可扩展、灵活性好：这四条是作者对好的面向对象代码的定义。简单工厂模式（Simple Factory）是达成这一目标的第一个工具：把*该实例化哪个对象*隔离到一个类中，使业务类、工厂和界面可以各自独立变化。

## 引入的框架
- **面向对象的四大好处（The four payoffs of OO）** — 可维护、可复用、可扩展、灵活性好。通过活字印刷的故事来讲解：改一个字、跨书复用字、增加字、重新排版。雕版印刷（朴素的计算器）一样也做不到，因为所有内容都刻在同一块板上：这就是耦合。
  - 何时使用：在问「能不能运行」之前，把它作为评估任何代码的检查清单。
- **业务逻辑与界面逻辑分离（Separate business logic from UI logic）** — 提取一个 `Operation` 类，让同一套运算同时服务于控制台、桌面、Web 和移动端客户端。这就是封装，是面向对象三大特性中的第一个。
- **紧耦合 vs 松耦合（Tight vs loose coupling）** — 一个 `switch` 包含加减乘除，意味着新增 `pow` 会迫使其他四个重新编译，并使它们暴露在意外（或恶意）修改之下：工资单的故事里，维护者偷偷把 `salary *= 1.1` 塞进月薪分支。把每个算法拆成抽象类 `Operation` 的独立子类（继承 + 多态）。
- **简单工厂模式（Simple Factory）** — 一个独立的类，唯一的职责是决定实例化哪个具体的 `Operation`，并以抽象父类型返回。
  - 结构：`Operation`（抽象产品）← `Add`/`Sub`/`Mul`/`Div`（具体产品）；`OperationFactory.createOperate(String)`（工厂，静态 switch）；客户端只看到 `Operation` 和工厂。
  - 何时使用：*选择*实例化哪个类这件事本身很可能变化或增长。
  - 做法：(1) 带有运算方法的抽象产品；(2) 每个算法一个子类；(3) 一个工厂，其 `switch` 把输入标记映射为 `new Concrete()`；(4) 客户端调用工厂，再调用多态方法。
- **UML类图（UML class diagram basics）** — 类的方框（类名 / 字段和属性 / 方法；`+` 公有，`-` 私有，`#` 保护；斜体类名 = 抽象类）；`<<interface>>` 方框或棒棒糖表示法；继承用空心三角形加实线；实现接口用空心三角形加虚线；关联用实线箭头，表示「知道」（`Penguin` 持有一个 `Climate`）；聚合用空心菱形，弱拥有关系（雁群有大雁）；合成（组合）用实心菱形，整体与部分共享生命周期（鸟有翅膀，基数 1–2）；依赖用虚线箭头（Animal 的新陈代谢依赖 Oxygen、Water，作为参数传入）。

## 关键概念
- **可维护（Maintainable）**：只改需要改的部分。
- **可复用（Reusable）**：同一个类服务于多个前端。
- **可扩展（Extensible）**：靠新增来添加，而不是靠修改。
- **灵活性（Flexible）**：无需重建即可重新排列。
- **封装（Encapsulation）**：隐藏引擎，只露出踏板。
- **多态（Polymorphism）**：工厂返回 `Operation`；调用 `oper.getResult()` 时运行的是子类的代码。
- **基数（Cardinality）**：关联两端的 `1`/`2`/`n`。

## 心智模型
- **把朴素的计算器看作雕版印刷。** 每次改动都要重新刻板。把面向对象的版本看作活字印刷。
- **用「新增一个功能是否迫使我交出无关的代码？」来判断耦合的坏味道。** 如果新增 `pow` 需要拿到 `add` 的源码，这个设计就是紧耦合。
- **当实例化是变化点时使用工厂。** "到底要实例化谁，将来会不会增加实例化的对象……应该考虑用一个单独的类来做这个创造实例的过程."
- **初学者按计算机的步骤思考；面向对象按职责思考。** 「输入两个数，按运算符分支」是 CPU 的视角；`Operation`、`Add`、工厂、界面才是领域的视角。

## 反模式
- **变量名 `A`、`B`、`C`、`D`**：没有描述性；大鸟第一个指出的问题。
- **对运算符使用没有 `else` 的链式 `if`**：每个分支都会被求值；应使用 `switch`。
- **没有除零检查，重复调用 `Double.parseDouble`**：正确性和重复问题，暴露出「在我的输入上能跑」的心态。
- **为了在不同界面复用而复制粘贴**："初级程序员的工作就是Ctrl+C和Ctrl+V"；重复会让维护变成灾难。
- **一个 `switch` 包含所有算法**：新增一个就迫使全部重新编译；任何一个算法的维护者都可能破坏其他所有算法。
- **忘记工厂也要修改**：只增加一个子类还不够；工厂的 `switch` 还要多一个分支。这是该模式已知的弱点，将在 ch08 再次讨论。

## 代码示例
```java
public abstract class Operation {
    public double getResult(double numberA, double numberB) { return 0d; }
}

public class Add extends Operation {
    public double getResult(double numberA, double numberB) { return numberA + numberB; }
}
public class Sub extends Operation {
    public double getResult(double numberA, double numberB) { return numberA - numberB; }
}
public class Mul extends Operation {
    public double getResult(double numberA, double numberB) { return numberA * numberB; }
}
public class Div extends Operation {
    public double getResult(double numberA, double numberB) {
        if (numberB == 0) {
            System.out.println("除数不能为0");
            throw new ArithmeticException();
        }
        return numberA / numberB;
    }
}

// 简单运算工厂类
public class OperationFactory {
    public static Operation createOperate(String operate) {
        Operation oper = null;
        switch (operate) {
            case "+": oper = new Add(); break;
            case "-": oper = new Sub(); break;
            case "*": oper = new Mul(); break;
            case "/": oper = new Div(); break;
        }
        return oper;
    }
}

// 客户端
Operation oper = OperationFactory.createOperate(strOperate);
double result = oper.getResult(numberA, numberB);
```
- **演示内容**：客户端从不指名具体类；修改 `Add` 只涉及一个文件；新增 `Pow` 意味着一个新子类加上工厂的一个分支，界面完全不动。

## 参考表
| UML 关系 | 表示法 | 含义 | 书中示例 |
|---|---|---|---|
| 继承 Inheritance | 空心三角形，实线 | is-a | 鸟 → 动物 |
| 实现 Realisation | 空心三角形，虚线 | 实现接口 | 大雁 → IFly |
| 关联 Association | 实线箭头 | 知道（字段引用） | 企鹅 → 气候 |
| 聚合 Aggregation | 空心菱形 | 弱 has-a，部分比整体活得久 | 雁群 ◇→ 大雁 |
| 合成/组合 Composition | 实心菱形，基数 | 强 has-a，生命周期相同 | 鸟 ◆→ 翅膀 (1:2) |
| 依赖 Dependency | 虚线箭头 | 作为参数/临时对象使用 | 动物 --> 氧气, 水 |

## 实战示例
面试题目："用任意一种面向对象语言实现一个计算器控制台程序，输入两个数和运算符号，得到结果."

**v1（被拒）**：一切都写在 `main` 里；`String A, B, C; double D;`，对运算符做四个相互独立的 `if`，`parseDouble` 重复八次，没有除零检查。运行结果正确。却没有回答真正的问题，即「证明你会写面向对象代码」。

**v2（代码规范）**：`numberA`、`strOperate`、`numberB`，一个 `switch`，一个 `try/catch`。仍然是过程式的：它把问题理解成计算机的步骤。

**v3（封装）**：`Operation.getResult(numberA, numberB, operate)` 持有 `switch`；`main` 只做输入输出。现在 Windows 或 Web 计算器可以复用 `Operation`。大鸟的结论：三大面向对象特性只用到了一个。

**v4（继承 + 多态）**：问「如果我新增 `pow`，必须改动什么？」答案是：共享的 `switch`，因此也就是每一个算法。工资单的类比：为了加入时薪而把月薪代码交给外包人员，就是 `salary *= 1.1` 被偷偷塞进去的方式。拆成抽象类 `Operation` 和 `Add`/`Sub`/`Mul`/`Div`。新问题：谁来决定 `new` 哪个子类？

**v5（简单工厂模式）**：`OperationFactory.createOperate("+")` 返回一个 `Operation`。小测验：改加法 → 编辑 `Add`；加 sqrt/sin → 新子类**加上**工厂的一个分支；改界面 → 只编辑界面。

为什么有效：变化的三个维度（算法内部、算法集合、展示）现在分别位于三个地方。为什么它不是终点：工厂里仍有一个随每个算法增长的 `switch`（见 ch02、ch08）。

## 关键要点
1. 用可维护、可复用、可扩展、灵活性好来评判代码，而不是「能运行」。
2. 先把业务逻辑与界面分离；仅此一步就能获得跨前端的复用。
3. 当新增一个变体迫使你修改兄弟变体时，设计就是紧耦合；把变体拆成某个抽象的子类。
4. 把「实例化哪个类」的决策放进工厂；客户端只使用抽象类型。
5. 简单工厂模式的代价是不断增长的 `switch`；选用之前要了解这一点。
6. 学会 UML类图：它们是全书传达结构的方式。

## 关联章节
- **[ch00](ch00-oo-basics.md)**：前置章节；作者说如果 v4 读起来吃力，就回到序章。
- **[ch02](ch02-strategy.md)**：同样的形状（抽象父类、子类）在策略模式（Strategy）中再次出现，而工厂被并入 Context（上下文）。
- **[ch04](ch04-open-closed.md)**：v1→v5 的演进被重述为开放-封闭原则（OCP）的教科书式例证。
- **[ch08](ch08-factory-method.md)**：用每个产品一个工厂子类来取代工厂的 `switch`。
- **[ch15](ch15-abstract-factory.md)**：反射彻底去掉了 `switch`。
