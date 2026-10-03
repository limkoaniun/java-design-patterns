# Chapter 21: 有些类也需计划生育——单例模式 — Singleton

## Core Idea
Whether a second instance may exist is the class's own responsibility, not the caller's: make the constructor `private`, keep the sole instance in a `static` field, and expose it only through `getInstance()`. Thread safety then decides between lazy (懒汉) variants and eager static initialisation (饿汉).

## Frameworks Introduced
- **单例模式 (Singleton)** — “保证一个类仅有一个实例，并提供一个访问它的全局访问点。”[DP]
  - Rationale (author quoting GoF): a global variable lets an object be reached but cannot stop clients creating several; “一个最好的办法就是，让类自身负责保存它的唯一实例。这个类可以保证没有其他实例可以被创建，并且它可以提供一个访问该实例的方法。”[DP]
  - When to use: exactly one instance must exist (a toolbox window, a configuration, a connection pool) and callers must not be able to `new` another; you also want controlled access to that instance (“对唯一实例的受控访问”).
  - How: (1) `private static Singleton instance;` (2) `private Singleton() {}` so external `new` fails at compile time; (3) `public static Singleton getInstance()` creates on first call and returns the same object afterwards; (4) choose a thread-safety variant (see table).
  - Structure: `Singleton` with `-instance : Singleton`, `-Singleton()`, `+getInstance() : Singleton`; the client only calls `Singleton.getInstance()`.

## Key Concepts
- **私有构造方法**: an explicit `private` constructor cancels the default one, so `new Singleton()` outside the class does not compile.
- **getInstance()**: the single global access point; holds the "has it been created?" judgement.
- **懒汉式单例**: instance created on first reference; needs locking under multithreading.
- **饿汉式单例**: instance created by static initialisation when the class loads; thread-safe by the JVM, but occupies resources early.
- **synchronized**: Java's synchronisation lock; only one thread executes the locked block at a time.
- **Double-Check Locking (双重锁定)**: check `null`, lock, check `null` again; locks only when the instance is still absent.
- **volatile**: paired with double-checked locking so the write to `instance` is visible correctly across threads.
- **实用类 vs 单例**: a utility class (e.g. `Math`) is stateless static methods and cannot be inherited polymorphically; a singleton is a stateful object that can have subclasses.

## Mental Models
- Think of `getInstance()` as the **subordinate who knows whether the report was submitted**: the boss (client) only asks; the subordinate (class) judges. Do not let the client decide whether to instantiate.
- Use 饿汉式 by default in Java; it satisfies both goals (global access and instantiation control) with no locking. Reach for 懒汉 + double-check only when eager creation is genuinely too costly.
- Lock the **class** (`synchronized(Singleton.class)`), not the instance: before creation there is no instance to lock.
- If you are tempted to write "copy the `if (x == null)` check into the second button handler", stop: that is duplicated responsibility that belongs in the class.

## Anti-patterns
- **Instantiating inside the click handler** (`new JFrame("工具箱")` per click): every click spawns another window.
- **Null-checking in the caller**: works for one caller, silently fails when a second caller (menu + toolbar) holds its own reference and opens a second window.
- **Copy-pasting the guard into each caller**: "复制粘贴是最容易的编程，但也是最没有价值的编程" — duplicated logic diverges on the next bug fix.
- **`synchronized` on the whole `getInstance()`**: correct but locks on every call; a measurable cost once the instance exists.
- **Double-check without the inner null test**: two threads pass the outer check, queue on the lock, and both create instances.

## Code Examples
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
- **What it demonstrates**: private constructor plus static accessor yields one shared instance; `new` from outside is a compile error.

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
- **What it demonstrates**: the two production-grade variants; double-check locks only until the instance exists, static initialisation delegates thread safety to class loading.

## Reference Tables
| Variant | Creation time | Thread-safe? | Cost | Author's verdict |
|---|---|---|---|---|
| 懒汉式 (plain `if null`) | first `getInstance()` | No | none | fine single-threaded only |
| 懒汉式 + `synchronized` method | first call | Yes | lock on **every** call | works, hurts performance |
| 懒汉式 + Double-Check Locking (`volatile`) | first call | Yes | lock only until created | use when performance matters |
| 饿汉式 (static initialisation) | class load | Yes (JVM) | early resource use | "从Java语言角度来讲，饿汉式的单例类已经足够满足我们的需求" |

| Utility class (`Math`) | Singleton |
|---|---|
| No state; static methods/fields | Stateful, one real object |
| Private constructor to prevent instances | Private constructor + one stored instance |
| Cannot be subclassed polymorphically | Can have subclasses |

## Worked Example
1. **Naive**: a Swing main window has an "打开工具箱" button whose `actionPerformed` does `JFrame toolkit = new JFrame("工具箱")` and shows it. Each click opens another toolbox.
2. **Fix 1 (caller-side guard)**: hoist `JFrame toolkit;` to a field and wrap creation in `if (toolkit == null || !toolkit.isVisible())`. Works for one button.
3. **What broke**: add a second button ("打开工具箱2") reusing a shared `ToolkitListener`; each listener instance holds its own `toolkit` field, so the two buttons open two toolboxes. Copy-pasting the guard did not help; the *judgement* lives in the wrong place.
4. **Refactor (Singleton)**: create `class Toolkit extends JFrame` with `private static Toolkit toolkit;`, a `private Toolkit(String title)` constructor, and `public static Toolkit getInstance()` that instantiates (and configures size, location, always-on-top, `DISPOSE_ON_CLOSE`, visible) only when `toolkit == null || !toolkit.isVisible()`, then returns it. Both listeners now do only `Toolkit.getInstance();`. Reverting to `new Toolkit("工具箱")` is a compile error.
5. **Why**: whether a second instance may exist is the class's own responsibility, like a couple deciding on a second child under 计划生育. The client just uses it.
6. **Harden**: under multithreading, two simultaneous `getInstance()` calls can both pass `instance == null`; add `synchronized`, then reduce the cost with double-checked locking, or sidestep it entirely with static initialisation.

## Key Takeaways
1. Make the constructor `private` and expose one `static getInstance()`; that alone stops external `new` at compile time.
2. Put the "already created?" decision inside the class, never in callers; callers multiply and their guards drift.
3. In multithreaded code, plain lazy creation is unsafe; use double-checked locking with `volatile`, or static initialisation.
4. Double-check needs *both* null tests: the outer avoids locking, the inner prevents duplicate creation after queuing.
5. Prefer 饿汉式 (static initialisation) in Java unless early instantiation is genuinely expensive.
6. Do not confuse a stateless utility class with a singleton; the singleton is a real object with state and possible subclasses.

## Connects To
- **[ch08](ch08-factory-method.md)** and **[ch15](ch15-abstract-factory.md)**: factories are frequently made singletons; creational patterns share the "control who calls `new`" theme.
- **[ch03](ch03-single-responsibility.md)**: moving the instantiation judgement into the class is a single-responsibility decision.
- **[ch29](ch29-pattern-summary.md)**: the contest summary contrasts Singleton ("一人创建，全家获益") with the other creational patterns.
- **Java memory model**: `volatile` and class-loading guarantees are what make the double-check and 饿汉式 variants correct.
