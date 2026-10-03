# 第0章：楔子 培训实习生——面向对象基础（Prologue: OO Fundamentals via the "Animal Sports Meet"）

## 核心思想
面向对象编程不是语法，而是一种把行为放到正确位置的方法，使重复消失、变化保持局部。作者通过演进一个极小的程序（一只会喵喵叫的猫），把封装（Encapsulation）、继承（Inheritance）、多态（Polymorphism）、抽象类（Abstract class）和接口（Interface）逐一讲清，最终得到一个多态的「动物运动会」，每一步都针对重复做重构（Refactoring）。

## 引入的框架
- **类与实例 (Class and Instance)** — “类就是具有相同的属性和功能的对象的抽象的集合”；实例是“一个真实的对象”，用 `new` 创建。
  - 何时使用：当某个函数（例如 `shout()`）所处的位置不合适（「你家客厅里的邻居电视机」）时，提取成类。
  - 做法：类名首字母大写；只暴露 `public` 成员；先实例化再调用。
- **构造方法 (Constructor)** — 与类同名，没有返回类型，在 `new` 时运行；在你自己定义之前，每个类都有一个空的默认构造方法。
- **方法重载 (Method overloading)** — “创建同名的多个方法的能力，但这些方法需使用不同的参数类型”。用它在不改动已有方法的前提下增加能力（例如 `Cat()` 和 `Cat(String name)`）。
- **属性与修饰符 (Properties and modifiers)** — 字段是私有的存储；属性是保护字段的 `get/set` 对。`public` = 任何人可访问，`private` = 仅同一个类，`protected` = 子类也可访问。门窗（public）与墙壁（private）。
- **封装 (Encapsulation)** — “每个对象都包含它能进行操作所需要的所有信息”。三项好处：降低耦合、可自由修改内部实现、拥有清晰的公共接口。
- **继承 (Inheritance)** — 表达 **is-a** 关系。三条规则：子类拥有父类的非 private 成员；子类可以添加自己的成员；子类可以重写父类的行为。代价：“父类变，则子类不得不变”，并且暴露了父类的内部（强耦合）。只为 is-a 而继承，绝不为 has-a 而继承（手不继承人）。
- **多态 (Polymorphism)** — “不同的对象可以执行相同的动作，但要通过它们自己的实现代码来执行”。京剧的类比：儿子*以*父亲的身份表演（子类表现为父类类型），用自己的方式表演（重写），而且表演时不能展示自己的绝活（通过父类引用看不到子类独有的成员）。声明为父类，实例化为子类；绑定取决于运行时类型 [AMNFP]。
- **抽象类 (Abstract class)** — 不能被实例化；抽象方法必须被重写；任何含有抽象方法的类都是抽象类。经验法则：“抽象类拥有尽可能多的共同代码，拥有尽可能少的数据” [J&DP]；在继承树中“树叶节点应当是具体类，而树枝节点均应当是抽象类” [J&DP]。
- **接口 (Interface)** — “把隐式公共方法和属性组合起来，以封装特定功能的一个集合”；没有字段、没有构造方法、没有方法体；一个类可以实现多个接口。
- **集合与泛型 (Collections and generics)** — `ArrayList` 按需增长，但不是类型安全的，并且会对值类型装箱；`ArrayList<T>` 两个问题都解决了。优先使用泛型集合。

## 关键概念
- **字段 vs 属性 (field vs property)**：字段以私有方式存储数据；属性是对它的受控公共访问。
- **耦合 (Coupling)**：「藕断丝连」，两个类的变化相互牵连。继承是一种强耦合关系。
- **方法重写 (Override)**：子类用自己的实现替换父类的实现。
- **is-a vs has-a**：is-a 是继承的依据；has-a 要用合成（组合）。
- **装箱/拆箱 (Boxing/unboxing)**：把值类型包装成 `Object` 再取回；开销大，泛型可避免。
- **重构 (Refactoring)**：在出现重复时改进现有代码的设计，而不是提前改进。

## 心智模型
- **抽象类自下而上发现，接口自上而下设计。**先有 Cat 和 Dog，`Animal` 是通过重构从它们中*泛化*出来的。接口（电源插座、运动会的项目清单）在任何实现者出现之前就已定义。
- **相似的事物用抽象类，跨越不相关事物的行为用接口。**猫和狗共享 `Animal` 父类；飞机、麻雀和超人只共享 `IFly`。
- **把 `protected` 看作「仅限家人」。**子类需要的数据（name、shoutNum）用 protected；其余一律 private。
- **只有 `Cat` 时就设计 `Animal` 是过度设计。**等第二个类出现，再提取。

## 反模式
- **因为代码看起来相似就让 Dog extends Cat**：此后猫的每个新行为（爬树、抓老鼠）都会泄漏到 Dog 中。代码相似不等于 is-a 关系。
- **Ctrl+C / Ctrl+V 式复用**：五个动物类有 90% 相同的方法体；喊叫格式改一个字就要改五处。
- **为了让多态生效而把「变出东西」放到 `Animal` 上**：迫使每个动物都拥有只有三个特殊动物才有的行为。应改用接口。
- **用公共字段代替属性**：「没有纱窗的窗户」：任何人随时都可以写入任何内容。
- **用定长数组存放不断增长的名单**：`new Animal[5]` 任意限制了报名人数；应使用泛型列表。

## 代码示例
重构的最终状态：抽象父类承载所有共享行为，子类只提供不同之处。

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
- **说明了什么**：继承消除了重复；多态让 `Animal` 引用分派到 `Cat`/`Dog`；抽象的 `getShoutSound()` 是模板方法模式（Template Method）(ch10) 的雏形。

用接口表达跨越不相关类的行为，加上泛型集合的客户端：

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
- **说明了什么**：`ArrayList<Animal>` 在编译期就拒绝 `add(123)`，循环中也无需类型转换；`IChange` 让猫和猴子可以被统一对待，而不污染 `Animal`。

## 参考表
| | 抽象类 Abstract class | 接口 Interface |
|---|---|---|
| 能否包含实现 | 能（部分） | 不能 |
| 每个类可使用的数量 | 一个 | 多个 |
| 抽象的对象 | 整个类（字段、属性、方法） | 一种行为（类的一个切面） |
| 设计方向 | 自下而上：通过重构从已有子类泛化而来 | 自上而下：在实现者未知时就先定义 |
| 适用场景 | 对象是相似的种类（猫、狗 → 动物） | 不相关的对象共享一种行为（飞机、麻雀、超人 → IFly） |

| | 数组 Array | `ArrayList` | `ArrayList<T>` |
|---|---|---|---|
| 大小 | 创建时固定 | 按需增长 | 按需增长 |
| 类型安全 | 是 | 否（一切都是 `Object`） | 是 |
| 装箱开销 | 无 | 对值类型装箱 | 无 |
| 结论 | 适合固定集合 | 有了泛型之后「太老土」 | 默认选择 |

## 实战示例
作者带着一个程序走过八次重构：
1. **朴素版**：在 `main` 中直接写 `System.out.println("喵")`。需要第二声喵时就得复制粘贴。
2. **函数**：提取出 `shout()`。但它仍然在 `Test` 里，归属不对。
3. **类**：`Cat` 带有 `public String shout()`；客户端写 `Cat cat = new Cat(); cat.shout();`。
4. **构造方法 + 重载**：用 `Cat(String name)` 让猫一出生就有名字；再加上默认为「无名」的 `Cat()`，这样无名的猫依然可以存在。
5. **属性**：`shoutNum` 作为私有字段，配上 `setShoutNum`/`getShoutNum`，让 setter 限制取值（`if (value <= 10) ... else 10`）：窗户上的「纱窗」。
6. **第二个类让它崩溃**：`Dog` 是 `Cat` 的拷贝，只改了一个字符串。提取出 `Animal`（name、shoutNum、属性方法），让两者都 `extends Animal`，并调用 `super(name)`。
7. **为运动会使用多态**：`Animal[] arrayAnimal` 里装满猫和狗；`arrayAnimal[i].shout()` 按运行时类型分派。加入 `Cattle` 和 `Sheep`，循环依然无需改动。
8. **剩余的重复**：每个 `shout()` 里的循环都是一样的。把 `shout()` 上移到 `Animal`，只把 `getShoutSound()` 留作抽象方法，并把 `Animal` 声明为抽象类，因为「一个动物」无法被实例化。子类缩减为一个构造方法和一行代码。

随后是两个扩展：为叮当/孙悟空设计的 `IChange`（这种行为不能放在 `Animal` 上），以及用 `ArrayList<Animal>` 取代五个槽位的数组，使报名和退出（`remove(1)`）无需在下标运算上出意外（移除一次后，后面的元素会前移，所以连续两次移除下标 1 会移除两只相邻的狗）。

意义所在：每一步都由一个具体的重复或一个具体的新需求触发。没有任何东西是出于臆测而抽象的。

## 关键要点
1. 当函数没有天然归属时提取类；当两个类共享方法体时提取父类。
2. 只为 is-a 而继承；has-a 用合成。「Dog extends Cat」是典型的错误。
3. 变量声明为父类或接口类型，实例化为具体类型：这正是多态得以成立的原因。
4. 叶子类是具体类，树枝类是抽象类；抽象类承载最多的共享代码和最少的数据。
5. 抽象类产生于重构；接口在实现者出现之前设计。
6. 默认使用 `ArrayList<T>`；原始的 `ArrayList` 牺牲了类型安全和装箱开销，却一无所获。
7. 没有设计模式，对多态的理解“多半都是肤浅和片面的”：本章是入场券，而不是终点。

## 关联章节
- **[ch01](ch01-simple-factory.md)**：计算器把这三大特性（封装、继承、多态）用到了一个业务问题上。
- **[ch10](ch10-template-method.md)**：第 8 步中 `shout()`/`getShoutSound()` 的拆分*就是*模板方法模式；作者明确这样说过。
- **[ch05](ch05-dependency-inversion.md)**：「声明为父类，实例化为子类」成为面向抽象编程这一正式原则。
- **[ch22](ch22-bridge.md)**：这里 is-a 与 has-a 的警告后来成为合成/聚合复用原则（CARP）。
- **GoF / UML**：类、接口、泛化和实现的符号在 ch01 §1.11 中被形式化。
