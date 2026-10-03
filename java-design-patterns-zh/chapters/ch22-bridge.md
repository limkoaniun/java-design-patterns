# 第22章：手机软件何时统一——桥接模式（Bridge）

## 核心思想
当系统沿多个维度变化时（手机*品牌* × 手机*软件*），单一的继承树会急剧膨胀；应把每个维度拆成各自的层次结构，再用聚合把它们连接起来，这样品牌和软件就可以各自独立变化。本章还给出了背后的原则：优先使用合成/聚合，而不是类继承。

## 引入的框架
- **桥接模式（Bridge）** — “将抽象部分与它的实现部分分离，使它们都可以独立地变化。”[DP]
  - 作者特别强调的澄清："实现"不是指「抽象类的派生类」；“实现指的是抽象类和它的派生类用来实现自己的对象”[DPE]。以手机为例：手机既可以按品牌分类，也可以按功能分类；桥接模式让这两种分类各自独立变化。
  - 适用时机：你发现需要从**多个角度**对对象分类，而仅靠继承会为每种组合都产生一个类，并违反开放-封闭原则（OCP）。
  - 做法：(1) 找出两个（或更多）相互独立的维度；(2) 为每个维度提供一个抽象类（`Abstraction`、`Implementor`）；(3) `Abstraction` 持有一个通过 `setImplementor()` 设置的 `Implementor` 引用；(4) `RefinedAbstraction.operation()` 委托给 `implementor.operation()`；(5) 增加品牌或功能时，只需在对应的层次结构中增加一个子类。
  - 结构：`Abstraction`（`-implementor`、`+setImplementor()`、`+operation()`）⟵ `RefinedAbstraction`；`Implementor`（`+operation()`）⟵ `ConcreteImplementorA`、`ConcreteImplementorB`。两个抽象类之间的聚合线就是「桥」。
- **合成／聚合复用原则（CARP, Composite/Aggregate Reuse Principle）** — “尽量使用合成／聚合，尽量不要使用类继承。”[J&DP]
  - 聚合（Aggregation）是弱的「has-a」：A 可以包含 B，但 B 不是 A 的一部分（大雁和雁群）。合成（Composition）是强的「has-a」：严格的整体-部分关系，生命周期一致（大雁和它的翅膀）。[DPE]
  - 好处：“优先使用对象的合成／聚合将有助于你保持每个类被封装，并被集中在单个任务上。这样类和类继承层次会保持较小规模，并且不太可能增长为不可控制的庞然大物。”[DP]
  - 经验法则：只有在真正的 **is-a** 关系下才使用继承；否则使用合成。

## 关键概念
- **抽象部分 / 实现部分**：两个相互独立变化的层次结构（这里是 `HandsetBrand` 和 `HandsetSoft`）。
- **多角度分类**：桥接模式的触发条件；品牌和功能是对手机分类的两个正交角度。
- **继承的强耦合**：继承在编译期就已固定；父类的改动会迫使子类改动；被复用的子类会连带继承不合适的父类实现。[DP]
- **"有了新锤子，所有的东西看上去都成了钉子"**[DPE]：新手对继承的滥用。
- **聚合 vs 合成**：弱所有权 vs 强所有权；品牌*聚合*软件（软件不是品牌的一部分）。
- **PC 模式 vs 2007 手机模式**：操作系统/软件厂商与硬件厂商解耦，对比每个手机厂商都把自己的软件固化在手机里；这是桥接的类比。

## 心智模型
- 把这两个抽象类想成**硬件厂商和软件厂商**：各自独立出货，只在使用时通过 `setHandsetSoft()` 结合在一起。
- 选择之前先数类的个数：用继承时，B 个品牌 × F 个功能 = B·F 个叶子类；用桥接模式时，只有 B + F 个类。如果乘积项在增长，就该用桥接模式。
- 用「这个改动会不会产生连锁反应？」来检验：增加品牌 S 只涉及一个类；增加音乐播放只涉及一个类；其他任何东西都不需要重新编译。
- 桥接模式是开放-封闭原则与合成/聚合复用原则的结合应用；“很多设计模式其实就是原则的应用而已”。

## 反模式
- **以品牌为根的继承**（`HandsetBrandM` → `HandsetBrandMGame`、`HandsetBrandMAddressList`……）：每增加一个新功能，就要在每个品牌下增加一个子类；每增加一个新品牌，所有功能又要重来一遍。
- **以功能为根的继承**（`HandsetGame` → `HandsetBrandMGame`、`HandsetBrandNGame`）：从另一侧出现同样的膨胀；"换一种方式"并不能解决问题。
- **为复用而非 is-a 而继承**：把子类锁死在父类的实现上，并阻碍运行时替换。
- **任由层次结构变成"不可控制的庞然大物"**：说明你把两个维度混进了同一棵树。

## 代码示例
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
- **演示内容**：品牌与软件相互独立地变化；增加任意一种只需增加一个类，且不修改任何现有代码。

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
- **演示内容**：GoF 的基本骨架；`Abstraction` 委托给可替换的 `Implementor`。

## 参考表
| 做法 | 增加一个品牌 | 增加一个功能 | B 个品牌 × F 个功能所需的类数 |
|---|---|---|---|
| 以品牌为根的继承 | 1 个品牌类 + F 个叶子类 | B 个新叶子类 | B + B·F |
| 以功能为根的继承 | B 个新叶子类 | 1 个功能类 + B 个叶子类 | F + B·F |
| 桥接模式（聚合） | 1 个类 | 1 个类 | B + F（+2 个抽象类） |

| 关系 | 强度 | 生命周期 | 示例 |
|---|---|---|---|
| 聚合 Aggregation | 弱「has-a」 | 相互独立 | 大雁属于某个雁群 |
| 合成 Composition | 强整体-部分 | 一致 | 大雁和它的翅膀 |

## 实战示例
1. **版本 1**：一个带 `run()` 的类 `HandsetBrandNGame`；客户端调用它。只有一个品牌时没问题。
2. **版本 2**：出现了第二个品牌 M；小菜抽象出 `HandsetGame`，其下有 `HandsetBrandMGame` / `HandsetBrandNGame` 子类。仍然没问题。
3. **版本 3**：两个品牌都需要通讯录。此时根变成 `HandsetBrand` → `HandsetBrandM` / `HandsetBrandN`，每个品牌下各有 `…Game` 和 `…AddressList` 叶子类。客户端使用 `HandsetBrand ab = new HandsetBrandMAddressList(); ab.run();`。
4. **问题所在**：增加音乐播放 → 要在*每个*品牌下增加一个子类；增加品牌 S → 增加一个品牌类，外加*所有*功能再来一遍；再增加输入法、拍照、品牌 L 和 X → "我要疯了"。把树翻转成以功能为根也无济于事。
5. **诊断**：大鸟指出了症结：继承是强的、编译期的耦合；“有了新锤子，所有的东西看上去都成了钉子”。应用合成／聚合复用原则。
6. **重构**：两个抽象类，`HandsetBrand` 和 `HandsetSoft`；品牌*聚合*软件（软件不是品牌的一部分，所以用聚合而不是合成）；`HandsetBrand.setHandsetSoft()` 负责安装软件；`run()` 进行委托。增加 `HandsetMusicPlay` 或 `HandsetBrandS` 各只需一个类，不触及其他任何东西——满足开放-封闭原则。
7. **命名**：两个抽象类之间的聚合线"像一座桥"→ 桥接模式。

## 关键要点
1. 当对象必须从多个相互独立的角度分类时，为每个角度提供各自的层次结构，并用聚合把它们桥接起来。
2. 遵循合成/聚合复用原则：“尽量使用合成／聚合，尽量不要使用类继承”；只有真正的 is-a 才继承。
3. 区分聚合（弱，生命周期相互独立）与合成（强整体-部分，生命周期一致）；手机品牌与软件之间的关系是聚合。
4. 用下一次改动的成本来衡量设计：桥接的设计每增加一个品牌或功能只需增加一个类，且不修改任何现有类。
5. 桥接模式中的「抽象与实现」指的是「对象自身会变化的各种实现」，而不是「基类 vs 子类」。
6. 许多模式不过是原则的应用；如果你真正理解了开放-封闭原则和合成/聚合复用原则，桥接模式自然就会浮现。

## 关联章节
- **[ch04](ch04-open-closed.md)**：桥接模式是针对排列组合式的继承违反开放-封闭原则这一问题的结构性解决方案。
- **[ch06](ch06-decorator.md)**：装饰模式（Decorator）同样主张用合成代替子类化，但目的是动态地*增加*职责，而不是分离多个维度。
- **[ch15](ch15-abstract-factory.md)**：抽象工厂模式（Abstract Factory）可以创建桥接模式所结合的相匹配的品牌/软件配对。
- **[ch17](ch17-adapter.md)**：二者都是结构型模式；适配器模式（Adapter）用于修复已有的接口不匹配，而桥接模式是在一开始就设计进去的。
- **[ch29](ch29-pattern-summary.md)**：比赛中称赞桥接模式的"用聚合来代替继承"是它的招牌手法。
