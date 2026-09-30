# Chapter 22: 手机软件何时统一——桥接模式 — Bridge

## Core Idea
When a system varies along more than one axis (phone *brand* × phone *software*), a single inheritance tree explodes; split each axis into its own hierarchy and connect them by aggregation, so brand and software can each change independently. The chapter also states the principle behind it: prefer composition/aggregation to class inheritance.

## Frameworks Introduced
- **桥接模式 (Bridge)** — “将抽象部分与它的实现部分分离，使它们都可以独立地变化。”[DP]
  - Clarification the author insists on: "实现" does not mean "the abstract class's subclasses"; “实现指的是抽象类和它的派生类用来实现自己的对象”[DPE]. For the phone: the phone can be classified by brand *or* by function; Bridge lets both classifications vary on their own.
  - When to use: you find yourself needing to classify objects from **multiple angles**, and inheritance alone would create a class for every combination and violate 开放-封闭原则.
  - How: (1) identify the two (or more) independent dimensions; (2) give each an abstract class (`Abstraction`, `Implementor`); (3) `Abstraction` holds an `Implementor` reference set via `setImplementor()`; (4) `RefinedAbstraction.operation()` delegates to `implementor.operation()`; (5) add a brand or a function by adding one subclass to the matching hierarchy.
  - Structure: `Abstraction` (`-implementor`, `+setImplementor()`, `+operation()`) ⟵ `RefinedAbstraction`; `Implementor` (`+operation()`) ⟵ `ConcreteImplementorA`, `ConcreteImplementorB`. The aggregation line between the two abstractions is "the bridge".
- **合成／聚合复用原则 (CARP, Composite/Aggregate Reuse Principle)** — “尽量使用合成／聚合，尽量不要使用类继承。”[J&DP]
  - 聚合 (Aggregation) is a weak "has-a": A may contain B, but B is not part of A (大雁 and 雁群). 合成 (Composition) is a strong "has-a": strict part-whole with shared lifetime (大雁 and its 翅膀).[DPE]
  - Benefit: “优先使用对象的合成／聚合将有助于你保持每个类被封装，并被集中在单个任务上。这样类和类继承层次会保持较小规模，并且不太可能增长为不可控制的庞然大物。”[DP]
  - Rule of thumb: use inheritance only for a true **is-a** relationship; otherwise compose.

## Key Concepts
- **抽象部分 / 实现部分**: the two independently varying hierarchies (here `HandsetBrand` and `HandsetSoft`).
- **多角度分类**: the trigger for Bridge; brand and function are orthogonal ways to classify a phone.
- **继承的强耦合**: inheritance is fixed at compile time; a parent change forces child changes; reused subclasses drag unsuitable parent implementations along.[DP]
- **"有了新锤子，所有的东西看上去都成了钉子"**[DPE]: the novice's overuse of inheritance.
- **聚合 vs 合成**: weak vs strong ownership; brand *aggregates* software (software is not part of the brand).
- **PC 模式 vs 2007 手机模式**: OS/software vendors decoupled from hardware vendors versus every phone maker baking its own software; the analogy for bridging.

## Mental Models
- Think of the two abstract classes as **hardware maker and software maker**: each ships independently, combined only at use time via `setHandsetSoft()`.
- Count classes before choosing: with inheritance, B brands × F functions = B·F leaf classes; with Bridge, B + F classes. If the multiplication term is growing, bridge.
- Use "does this change ripple?" as the test: adding brand S touches one class; adding music playback touches one class; nothing else recompiles.
- Bridge is 开放-封闭原则 + CARP applied together; “很多设计模式其实就是原则的应用而已”.

## Anti-patterns
- **Brand-rooted inheritance** (`HandsetBrandM` → `HandsetBrandMGame`, `HandsetBrandMAddressList`, …): every new function adds a subclass under every brand; every new brand adds all functions again.
- **Function-rooted inheritance** (`HandsetGame` → `HandsetBrandMGame`, `HandsetBrandNGame`): the same explosion from the other side; "换一种方式" does not fix it.
- **Inheritance for reuse rather than is-a**: locks the child to the parent's implementation and prevents runtime substitution.
- **Letting the hierarchy become "不可控制的庞然大物"**: a sign you have mixed two axes into one tree.

## Code Examples
```java
// 实现部分：手机软件
abstract class HandsetSoft {
    public abstract void run();
}
class HandsetGame extends HandsetSoft {
    public void run() { System.out.println("手机游戏"); }
}
class HandsetAddressList extends HandsetSoft {
    public void run() { System.out.println("通讯录"); }
}
class HandsetMusicPlay extends HandsetSoft {              // 新功能：只加一个类
    public void run() { System.out.println("音乐播放"); }
}
// 抽象部分：手机品牌，聚合一个软件
abstract class HandsetBrand {
    protected HandsetSoft soft;
    public void setHandsetSoft(HandsetSoft soft) { this.soft = soft; }  // 安装软件
    public abstract void run();
}
class HandsetBrandM extends HandsetBrand {
    public void run() { System.out.print("手机品牌M"); soft.run(); }
}
class HandsetBrandN extends HandsetBrand {
    public void run() { System.out.print("手机品牌N"); soft.run(); }
}
class HandsetBrandS extends HandsetBrand {                // 新品牌：只加一个类
    public void run() { System.out.print("手机品牌S"); soft.run(); }
}
// 客户端
HandsetBrand ab = new HandsetBrandM();
ab.setHandsetSoft(new HandsetGame());        ab.run();
ab.setHandsetSoft(new HandsetAddressList()); ab.run();
HandsetBrand ab2 = new HandsetBrandN();
ab2.setHandsetSoft(new HandsetGame());       ab2.run();
ab2.setHandsetSoft(new HandsetMusicPlay());  ab2.run();
```
- **What it demonstrates**: brand and software vary independently; adding either kind costs exactly one class and changes no existing code.

```java
// 桥接模式基本代码
abstract class Implementor { public abstract void operation(); }
class ConcreteImplementorA extends Implementor {
    public void operation() { System.out.println("具体实现A的方法执行"); }
}
class ConcreteImplementorB extends Implementor {
    public void operation() { System.out.println("具体实现B的方法执行"); }
}
abstract class Abstraction {
    protected Implementor implementor;
    public void setImplementor(Implementor implementor) { this.implementor = implementor; }
    public abstract void operation();
}
class RefinedAbstraction extends Abstraction {
    public void operation() {
        System.out.print("具体的Abstraction ");
        implementor.operation();
    }
}
Abstraction ab = new RefinedAbstraction();
ab.setImplementor(new ConcreteImplementorA()); ab.operation();
ab.setImplementor(new ConcreteImplementorB()); ab.operation();
```
- **What it demonstrates**: the GoF skeleton; `Abstraction` delegates to a swappable `Implementor`.

## Reference Tables
| Approach | Add a brand | Add a function | Classes for B brands × F functions |
|---|---|---|---|
| Inheritance rooted at brand | 1 brand class + F leaf classes | B new leaf classes | B + B·F |
| Inheritance rooted at function | B new leaf classes | 1 function class + B leaves | F + B·F |
| Bridge (aggregation) | 1 class | 1 class | B + F (+2 abstractions) |

| Relationship | Strength | Lifetime | Example |
|---|---|---|---|
| 聚合 Aggregation | weak "has-a" | independent | 大雁 belongs to a 雁群 |
| 合成 Composition | strong part-whole | shared | 大雁 and its 翅膀 |

## Worked Example
1. **Version 1**: one class `HandsetBrandNGame` with `run()`; client calls it. Fine for one brand.
2. **Version 2**: a second brand M appears; 小菜 abstracts `HandsetGame` with `HandsetBrandMGame` / `HandsetBrandNGame` subclasses. Still fine.
3. **Version 3**: both brands need 通讯录. Now the root becomes `HandsetBrand` → `HandsetBrandM` / `HandsetBrandN`, each with `…Game` and `…AddressList` leaves. Client uses `HandsetBrand ab = new HandsetBrandMAddressList(); ab.run();`.
4. **What broke**: add music playback → a subclass under *every* brand; add brand S → a brand class plus *every* function again; add input method, camera, brands L and X → "我要疯了". Flipping the tree to root at function does not help.
5. **Diagnosis**: 大鸟 names the fault: inheritance is a strong, compile-time coupling; “有了新锤子，所有的东西看上去都成了钉子”. Apply 合成／聚合复用原则.
6. **Refactor**: two abstract classes, `HandsetBrand` and `HandsetSoft`; brand *aggregates* software (software is not part of the brand, so aggregation, not composition); `HandsetBrand.setHandsetSoft()` installs software; `run()` delegates. Adding `HandsetMusicPlay` or `HandsetBrandS` is one class each and touches nothing else — 开放-封闭原则 satisfied.
7. **Name**: the aggregation line between the two abstractions "像一座桥" → 桥接模式.

## Key Takeaways
1. When objects must be classified from several independent angles, give each angle its own hierarchy and bridge them with aggregation.
2. Follow CARP: “尽量使用合成／聚合，尽量不要使用类继承”; inherit only for genuine is-a.
3. Distinguish aggregation (weak, independent lifetimes) from composition (strong part-whole, shared lifetime); the phone-brand/software link is aggregation.
4. Measure the design by the cost of the next change: a bridged design adds one class per new brand or function and modifies none.
5. Bridge's "abstraction vs implementation" means "the object's own varying implementations", not "base class vs subclasses".
6. Many patterns are just principles applied; if you internalise 开放-封闭 and CARP, Bridge falls out naturally.

## Connects To
- **[ch04](ch04-open-closed.md)**: Bridge is the structural answer to the open-closed violation of combinatorial inheritance.
- **[ch06](ch06-decorator.md)**: Decorator also favours composition over subclassing but to *add* responsibilities dynamically rather than to separate axes.
- **[ch15](ch15-abstract-factory.md)**: an abstract factory can create the matching brand/software pairs that Bridge combines.
- **[ch17](ch17-adapter.md)**: both are structural patterns; Adapter fixes an existing interface mismatch, Bridge is designed in up front.
- **[ch29](ch29-pattern-summary.md)**: the contest praises Bridge's "用聚合来代替继承" as its defining trick.
