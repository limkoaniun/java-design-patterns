# 第21章：有些类也需计划生育——单例模式（Singleton）

## 核心思想
是否允许存在第二个实例，是类自身的职责，而不是调用者的职责：把构造方法设为 `private`，把唯一实例保存在 `static` 字段中，并且只通过 `getInstance()` 对外提供。线程安全问题再决定该选懒汉（懒汉式）变体还是饿汉（饿汉式）的静态初始化。

## 引入的框架
- **单例模式（Singleton）** — “保证一个类仅有一个实例，并提供一个访问它的全局访问点。”[DP]
  - 理由（作者引用 GoF）：全局变量可以让对象被访问，却无法阻止客户端创建多个对象；“一个最好的办法就是，让类自身负责保存它的唯一实例。这个类可以保证没有其他实例可以被创建，并且它可以提供一个访问该实例的方法。”[DP]
  - 适用场景：必须恰好存在一个实例（工具箱窗口、配置、连接池），且调用者不能再 `new` 出另一个；同时你希望对该实例有受控的访问（“对唯一实例的受控访问”）。
  - 做法：(1) `private static Singleton instance;` (2) `private Singleton() {}`，使外部 `new` 在编译期失败；(3) `public static Singleton getInstance()` 在首次调用时创建实例，之后返回同一个对象；(4) 选择一种线程安全变体（见表）。
  - 结构：`Singleton` 含 `-instance : Singleton`、`-Singleton()`、`+getInstance() : Singleton`；客户端只调用 `Singleton.getInstance()`。

## 关键概念
- **私有构造方法**：显式的 `private` 构造方法取消了默认构造方法，因此类外的 `new Singleton()` 无法通过编译。
- **getInstance()**：唯一的全局访问点；承担「是否已创建？」的判断。
- **懒汉式单例**：实例在首次被引用时创建；多线程下需要加锁。
- **饿汉式单例**：实例在类加载时由静态初始化创建；由 JVM 保证线程安全，但会提前占用资源。
- **synchronized**：Java 的同步锁；同一时刻只有一个线程执行被锁定的代码块。
- **双重锁定（Double-Check Locking）**：检查 `null`、加锁、再次检查 `null`；只有在实例仍不存在时才加锁。
- **volatile**：与双重锁定配合使用，使对 `instance` 的写入在线程之间正确可见。
- **实用类 vs 单例**：实用类（如 `Math`）是无状态的静态方法，不能通过多态被继承；单例是有状态的对象，可以有子类。

## 心智模型
- 把 `getInstance()` 看作**知道报告是否已提交的下属**：老板（客户端）只负责询问；下属（类）负责判断。不要让客户端决定是否实例化。
- 在 Java 中默认使用饿汉式；它无需加锁就同时满足两个目标（全局访问和实例化控制）。只有当提前创建的代价确实过高时，才考虑懒汉 + 双重检查。
- 锁的是**类**（`synchronized(Singleton.class)`），而不是实例：创建之前并没有实例可锁。
- 如果你想写「把 `if (x == null)` 检查复制到第二个按钮的处理方法里」，请停下：这是重复的职责，它应当属于类。

## 反模式
- **在点击处理方法里实例化**（每次点击都 `new JFrame("工具箱")`）：每次点击都会产生另一个窗口。
- **在调用者里判空**：对一个调用者有效，但当第二个调用者（菜单 + 工具栏）持有自己的引用并打开第二个窗口时，会悄无声息地失效。
- **把判断复制粘贴到每个调用者里**："复制粘贴是最容易的编程，但也是最没有价值的编程" — 重复的逻辑会在下一次修复缺陷时出现分歧。
- **对整个 `getInstance()` 加 `synchronized`**：正确，但每次调用都要加锁；实例一旦创建，这就成了可测量的开销。
- **双重检查缺少内层的 null 判断**：两个线程通过外层检查，在锁上排队，随后都创建了实例。

## 代码示例
```java
// 基本单例（懒汉式）
class Singleton {
    private static Singleton instance;
    private Singleton() { }                       // 构造方法private化
    public static Singleton getInstance() {       // 得到实例的唯一途径
        if (instance == null) {
            instance = new Singleton();
        }
        return instance;
    }
}
// 客户端
Singleton s1 = Singleton.getInstance();
Singleton s2 = Singleton.getInstance();
if (s1 == s2) System.out.println("两个对象是相同的实例。");
// Singleton s3 = new Singleton();   // 编译错误
```
- **展示内容**：私有构造方法加静态访问方法即可得到一个共享实例；从外部 `new` 会产生编译错误。

```java
// 双重锁定（Double-Check Locking）
class Singleton {
    private volatile static Singleton instance;
    private Singleton() { }
    public static Singleton getInstance() {
        if (instance == null) {                         // 第一重：已存在则直接返回，不加锁
            synchronized (Singleton.class) {            // 防止多个线程同时进入创建实例
                if (instance == null) {                 // 第二重：排队进入的线程不再重复创建
                    instance = new Singleton();
                }
            }
        }
        return instance;
    }
}
// 静态初始化（饿汉式）
class Singleton {
    private static Singleton instance = new Singleton();
    private Singleton() { }
    public static Singleton getInstance() { return instance; }
}
```
- **展示内容**：两种可用于生产的变体；双重检查只在实例创建之前加锁，静态初始化则把线程安全交给类加载。

## 参考表
| 变体 | 创建时机 | 线程安全？ | 开销 | 作者的评价 |
|---|---|---|---|---|
| 懒汉式（普通 `if null`） | 首次 `getInstance()` | 否 | 无 | 仅适合单线程 |
| 懒汉式 + `synchronized` 方法 | 首次调用 | 是 | **每次**调用都加锁 | 可用，但损害性能 |
| 懒汉式 + 双重锁定（`volatile`） | 首次调用 | 是 | 仅在创建完成前加锁 | 性能重要时使用 |
| 饿汉式（静态初始化） | 类加载时 | 是（JVM） | 提前占用资源 | "从Java语言角度来讲，饿汉式的单例类已经足够满足我们的需求" |

| 实用类（`Math`） | 单例 |
|---|---|
| 无状态；静态方法/字段 | 有状态，一个真实的对象 |
| 私有构造方法，防止产生实例 | 私有构造方法 + 保存一个实例 |
| 不能通过多态被继承 | 可以有子类 |

## 实战示例
1. **朴素做法**：一个 Swing 主窗口有一个「打开工具箱」按钮，其 `actionPerformed` 执行 `JFrame toolkit = new JFrame("工具箱")` 并显示它。每次点击都会打开另一个工具箱。
2. **修复 1（调用者一侧的判断）**：把 `JFrame toolkit;` 提升为字段，并把创建代码包进 `if (toolkit == null || !toolkit.isVisible())`。对一个按钮有效。
3. **哪里出了问题**：再加第二个按钮（「打开工具箱2」），复用同一个 `ToolkitListener`；每个监听器实例都持有自己的 `toolkit` 字段，于是两个按钮打开了两个工具箱。复制粘贴判断没有帮助；*判断*放错了地方。
4. **重构（单例模式）**：创建 `class Toolkit extends JFrame`，包含 `private static Toolkit toolkit;`、一个 `private Toolkit(String title)` 构造方法，以及 `public static Toolkit getInstance()`，仅当 `toolkit == null || !toolkit.isVisible()` 时才实例化（并配置大小、位置、总在最前、`DISPOSE_ON_CLOSE`、可见），然后返回它。两个监听器现在都只执行 `Toolkit.getInstance();`。改回 `new Toolkit("工具箱")` 会产生编译错误。
5. **原因**：是否允许存在第二个实例是类自身的职责，就像一对夫妻在计划生育下决定要不要第二个孩子。客户端只管使用。
6. **加固**：在多线程下，两个同时进行的 `getInstance()` 调用可能都通过 `instance == null`；加上 `synchronized`，再用双重锁定降低开销，或者干脆用静态初始化绕开这个问题。

## 关键要点
1. 把构造方法设为 `private`，并暴露一个 `static getInstance()`；仅此一点就能在编译期阻止外部 `new`。
2. 把「是否已创建？」的决定放在类内部，绝不放在调用者里；调用者会不断增多，它们的判断也会逐渐走样。
3. 在多线程代码中，普通的懒创建是不安全的；使用带 `volatile` 的双重锁定，或者静态初始化。
4. 双重检查需要*两处* null 判断：外层避免加锁，内层防止排队之后重复创建。
5. 在 Java 中优先选择饿汉式（静态初始化），除非提前实例化的代价确实很高。
6. 不要把无状态的实用类与单例混为一谈；单例是有状态、可能有子类的真实对象。

## 关联章节
- **[ch08](ch08-factory-method.md)** 和 **[ch15](ch15-abstract-factory.md)**：工厂经常被做成单例；创建型模式共享「控制谁来调用 `new`」这一主题。
- **[ch03](ch03-single-responsibility.md)**：把实例化的判断移入类内部，是一个单一职责原则（SRP）层面的决定。
- **[ch29](ch29-pattern-summary.md)**：比赛总结把单例模式（"一人创建，全家获益"）与其他创建型模式作了对比。
- **Java 内存模型**：`volatile` 和类加载的保证，正是双重检查与饿汉式变体得以正确的原因。
