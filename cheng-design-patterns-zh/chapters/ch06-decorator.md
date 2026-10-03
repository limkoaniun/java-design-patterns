# 第6章：穿什么有这么重要？——装饰模式（Decorator）

## 核心思想
当某个功能只在某些场景下需要，且组合方式多变时，不要往核心类里添加字段和方法；应把每个功能放进各自的包装类，包装类实现与被包装对象相同的接口，由客户端在运行时按需要的任意顺序层层叠加。故事：给小菜穿衣服（T 恤、大裤衩、运动鞋……或西装、领带、皮鞋……或草帽加一只运动鞋一只皮鞋），而 `Person` 类不必知道每一件衣服。

## 引入的框架
- **装饰模式（Decorator）** — “动态地给一个对象添加一些额外的职责，就增加功能来说，装饰模式比生成子类更为灵活。”[DP]
  - 结构：`Component { +operation() }`（可动态添加职责的对象的接口）；`ConcreteComponent`（被装饰的具体对象）；`Decorator extends Component { -component; +setComponent(); +operation() }`（抽象包装类：持有一个 `Component`，转发 `operation()`；`Component` 并不知道它的存在）；`ConcreteDecoratorA/B`（先调用 `super.operation()`，再添加自己的状态/行为）。
  - 适用场景：某个类只在特殊情况下才需要额外行为；附加功能的集合及其顺序是变化的；希望把装饰逻辑从核心类中移除（"把类中的装饰功能从类中搬移去除，这样可以简化原有的类"）。
  - 做法：（1）定义共同接口；（2）核心类实现该接口；（3）抽象装饰类实现该接口，持有另一个实例的引用并转发；（4）每个具体装饰类重写 `operation()`，写成“先转发，再做自己的额外工作”；（5）客户端构建链：`d1.setComponent(c); d2.setComponent(d1); d2.operation();`。
  - 为何有效：每个装饰类只了解自己的职责和接口，不关心自己在链中的位置——"每个装饰对象只关心自己的功能，不需要关心如何被添加到对象链当中"[DPE]。失效模式：**顺序很重要**（先加密再过滤 vs 先过滤再加密）；理想情况下让装饰类彼此独立，使任意顺序都有效。
- **简化规则**（作者明确给出的变体）：如果只有一个 `ConcreteComponent` 而没有抽象的 `Component`，`Decorator` 可以直接继承 `ConcreteComponent`；如果只有一个 `ConcreteDecorator`，就把 `Decorator` 与 `ConcreteDecorator` 合并为一个类。
- **简单工厂（Simple Factory）+ 策略模式（Strategy）+ 装饰模式（组合）**，用于商场收银程序：`ISale` = Component，`CashNormal` = ConcreteComponent，`CashSuper` = Decorator（持有一个 `ISale`，转发），`CashRebate` / `CashReturn` = ConcreteDecorator；`CashContext` 为每种促销组装链。

## 关键概念
- **Component / ConcreteComponent / Decorator / ConcreteDecorator**：上述四种角色。
- **setComponent / decorate**：包装调用；作者的版本命名为 `decorate(ICharacter component)`。
- **包装顺序**：最后应用的包装最先执行；"先打8折再满300返100" ≠ "先满300返100再打8折"。
- **核心职责 vs 装饰功能**：该模式强制做出的划分；核心类只保留其主要行为。
- **穿衣舞**：作者对第二版代码的称呼，该版本把每一步都暴露给客户端，而不是在内部组装。
- **建造者 vs 装饰的边界**：建造者要求构建过程稳定；装饰用于不稳定、可自由重新组合的步骤。

## 心智模型
- 把装饰想成穿衣服：每件衣服都包裹在已有的一切之外，可以按任意顺序穿（超人 = 内裤穿在外面）。
- 当问题是“这次要哪些额外功能、按什么顺序？”时用装饰；当步骤固定时用建造者。
- 把 `CashNormal`（原价）看作光着身子的人，把打折 / 返利看作衣服；新的促销是新的组合，而不是新的类。
- 当组合可能爆炸时，优先用包装而不是子类：N 个功能用继承是 2^N 个子类；用装饰是 N 个类。

## 反模式
- **臃肿的核心类**（第一版）：`Person` 有 `wearTShirts()`、`wearSuit()` 等方法。添加“超人”就得修改 `Person`：违反开放-封闭原则。
- **只有继承没有组合**（第二版）：存在 `Finery` 子类，但客户端逐个调用 `dtx.show(); kk.show(); xc.show();`；组装过程被暴露，无法重新排序或嵌套。
- **组合类**（`CashReturnRebate`）：每种促销组合一个类，会重复 `CashReturn` 和 `CashRebate` 的代码，并随组合增多而爆炸（打折→返利、返利→打折、积分、抽奖……）。
- **把依赖顺序的装饰类当作与顺序无关**：在敏感词过滤之前加密会破坏过滤。

## 代码示例
教科书式的装饰（作者的命名，已整理）：

```java
abstract class Component { public abstract void operation(); }

class ConcreteComponent extends Component {
    public void operation() { System.out.println("具体对象的实际操作"); }
}

abstract class Decorator extends Component {
    protected Component component;
    public void setComponent(Component component) { this.component = component; }
    public void operation() { if (component != null) component.operation(); }   // forward
}

class ConcreteDecoratorA extends Decorator {
    private String addedState;
    public void operation() {
        super.operation();                       // run the wrapped object first
        addedState = "具体装饰对象A的独有操作";  // then this decorator's own work
        System.out.println(addedState);
    }
}
class ConcreteDecoratorB extends Decorator {
    public void operation() { super.operation(); addedBehavior(); }
    private void addedBehavior() { System.out.println("具体装饰对象B的独有操作"); }
}

ConcreteComponent c = new ConcreteComponent();
ConcreteDecoratorA d1 = new ConcreteDecoratorA();
ConcreteDecoratorB d2 = new ConcreteDecoratorB();
d1.setComponent(c);      // d1 wraps c
d2.setComponent(d1);     // d2 wraps d1
d2.operation();          // c → A → B
```
- **演示了什么**：链由客户端在运行时构建；每个装饰类先转发再添加。

收银程序，三种模式结合：

```java
public interface ISale { double acceptCash(double price, int num); }        // Component

public class CashNormal implements ISale {                                  // ConcreteComponent
    public double acceptCash(double price, int num) { return price * num; }
}

public class CashSuper implements ISale {                                   // Decorator (no longer abstract)
    protected ISale component;
    public void decorate(ISale component) { this.component = component; }
    public double acceptCash(double price, int num) {
        double result = 0d;
        if (component != null) result = component.acceptCash(price, num);   // run wrapped algorithm
        return result;
    }
}

public class CashRebate extends CashSuper {                                 // ConcreteDecorator
    private double moneyRebate = 1d;
    public CashRebate(double moneyRebate) { this.moneyRebate = moneyRebate; }
    public double acceptCash(double price, int num) {
        double result = price * num * moneyRebate;
        return super.acceptCash(result, 1);       // hand result to the next layer
    }
}

public class CashReturn extends CashSuper {                                 // ConcreteDecorator
    private double moneyCondition = 0d, moneyReturn = 0d;
    public CashReturn(double moneyCondition, double moneyReturn) { … }
    public double acceptCash(double price, int num) {
        double result = price * num;
        if (moneyCondition > 0 && result >= moneyCondition)
            result = result - Math.floor(result / moneyCondition) * moneyReturn;
        return super.acceptCash(result, 1);
    }
}

public class CashContext {                                                   // strategy context + simple factory
    private ISale cs;
    public CashContext(int cashType) {
        switch (cashType) {
            case 1: cs = new CashNormal(); break;
            case 5: // 先打8折, 再满300返100
                CashNormal cn = new CashNormal();
                CashReturn cr1 = new CashReturn(300d, 100d);
                CashRebate cr2 = new CashRebate(0.8d);
                cr1.decorate(cn);    // 满300返100 wraps 原价
                cr2.decorate(cr1);   // 打8折 wraps that   → executes 8折 first, then 返利
                cs = cr2; break;
            case 6: // 先满200返50, 再打7折
                CashNormal cn2 = new CashNormal();
                CashRebate cr3 = new CashRebate(0.7d);
                CashReturn cr4 = new CashReturn(200d, 50d);
                cr3.decorate(cn2); cr4.decorate(cr3);
                cs = cr4; break;
        }
    }
    public double getResult(double price, int num) { return cs.acceptCash(price, num); }
}
```
- **演示了什么**：不需要 `CashReturnRebate` 类；每个具体装饰类计算自己的那一步，并把累计金额（作为 `price`，`num = 1`）沿链向下传递。计算示例：1000×1 用 case 5 → 800 → 两个 300 → 600。500×4 用 case 6 → 2000 → 十个 200 → 1500 → ×0.7 → 1050。

## 实战示例
1. **第一版**：`Person` 每件衣服一个方法，外加 `show()`。添加超人需要修改 `Person`（违反开放-封闭原则）。
2. **第二版**：抽象的 `Finery`，带 `TShirts`、`BigTrouser` 等子类；`Person` 只有 `show()`。通过子类扩展，但客户端依次调用每件衣服的 `show()`，然后调用 `xc.show()`：即“穿衣舞”——组装过程暴露，无法嵌套，也无法控制顺序。
3. **不是建造者**：小菜提议用建造者；大鸟否决，因为这里的组装过程不稳定（任意衣服、任意顺序，甚至一件都不穿）。
4. **第三版（装饰）**：`ICharacter { show() }`；`Person implements ICharacter`；`Finery implements ICharacter`，持有一个 `ICharacter component`、`decorate(component)`，并转发 `show()`；每件衣服重写 `show()`，先打印自己再调用 `super.show()`。客户端：`pqx.decorate(xc); kk.decorate(pqx); dtx.decorate(kk); dtx.show();`。添加草帽 = 一个新子类加一条新链。
5. **迁移到商场收银**：第一次尝试添加 `CashReturnRebate`（重复代码，每种组合一个类）。第二次尝试引入 `ISale`，但忘了 `ConcreteComponent`；大鸟指出 `CashNormal` 就是基础算法。最终：`CashSuper` 成为具体装饰基类，`CashRebate` / `CashReturn` 以 `super.acceptCash(result, 1)` 结尾，`CashContext` 负责组装链。任何新的促销顺序只需改动 `CashContext`。

## 关键要点
1. 把每个可选功能放进各自的类，实现核心接口，持有并转发给被包装对象。
2. 具体装饰类遵循“先转发，再添加”；由客户端组装链，因此顺序和成员是运行时决定的。
3. 装饰模式把装饰逻辑从核心类中剥离，并消除重复的组合代码。
4. 包装顺序会改变结果；让装饰类保持独立以使任意顺序都有效，或者记录必需的顺序。
5. 当模式中只有一个具体组件或一个具体装饰类时，合并角色。
6. 当组装过程不稳定时，用装饰而不是建造者。

## 关联章节
- **[ch02](ch02-strategy.md)**：收银程序的 `CashContext` / `CashSuper` 家族起源于策略模式 + 简单工厂；本章加入了装饰。
- **[ch08](ch08-factory-method.md)**：`CashContext` 内部纠缠的 `new` 与 `decorate` 调用用工厂方法模式来整理。
- **[ch13](ch13-builder.md)**：作者划出的边界情形：稳定的构建序列用建造者，自由组合用装饰。
- **[ch07](ch07-proxy.md)**：代理模式有同样的“包装类实现相同接口”的形态，但它控制访问，而不是添加职责。
- **[ch04](ch04-open-closed.md)**：贯穿全章的动机：通过扩展来添加衣服和促销，而不是修改 `Person` 或算法类。
