# Chapter 17: 在NBA我需要翻译——适配器模式 — Adapter

## Core Idea
When a class you need already exists and works but its interface does not match what your client expects, and neither side can reasonably change, wrap it in an adapter that translates. Adapter is a late-stage, "亡羊补牢" tool: prevent interface mismatch first, refactor second, adapt only when both sides are frozen.

## Frameworks Introduced
- **适配器模式 (Adapter)** — “将一个类的接口转换成客户希望的另外一个接口。Adapter模式使得原本由于接口不兼容而不能一起工作的那些类可以一起工作。”[DP]
  - Structure: `Target` (`request()`, what the client expects — concrete, abstract, or interface) ← `Adapter` (extends/implements Target, holds a private `Adaptee`, its `request()` calls `adaptee.specificRequest()`); `Adaptee` (`specificRequest()`, the class to be adapted).
  - When to use: "两个类所做的事情相同或相似，但是具有不同的接口时"; reusing legacy code or a third-party component whose interface you will not and cannot change.
  - How: (1) identify the `Target` interface clients already call; (2) create `Adapter` that inherits `Target`; (3) compose the `Adaptee` inside it; (4) implement each Target method by forwarding to the Adaptee's differently-named method.
- **类适配器 vs 对象适配器 (class vs object adapter)** — GoF describes both; the class form needs multiple inheritance, which Java/C#/VB.NET lack, so the book teaches only the *object adapter* (composition).
- **扁鹊三兄弟 (the three physician brothers)** — the author's timing heuristic: 事前控制 (design consistent interfaces) > 事中控制 (refactor small mismatches immediately) > 事后控制 (adapt when nothing else is possible).

## Key Concepts
- **Target**: "这是客户所期待的接口".
- **Adaptee**: "需要适配的类" — correct data and behaviour, wrong interface.
- **Adapter**: "通过在内部包装一个Adaptee对象，把源接口转换成目标接口".
- **接口不符 (interface mismatch)**: system data and behaviour are right, only the method names/signatures differ.
- **控制范围之外 (outside your control)**: the trigger condition — the adaptee is legacy code, another team's code, or a vendor component.
- **DataAdapter (.NET)**: the author's real-world example; `Fill` and `Update` map between any data source and a uniform `DataSet`.
- **翻译者 (Translator)**: the chapter's adapter, letting an English-speaking coach direct a Chinese-speaking centre.

## Mental Models
- Think of an adapter as a **travel plug**: it changes the shape of the socket, not the electricity.
- Use Adapter when you would otherwise say "I would use that class if only its method were called X".
- Prefer changing the interface at design time over adapting later: "如果是在设计阶段，你有必要把类似的功能类的接口设计得不同吗？"
- An adapter that exists because *your own team* named things inconsistently is a symptom of missing naming standards, not a pattern success.

## Anti-patterns
- **Adapting instead of refactoring**: when both classes are yours and changeable, unify the interface; "首先不应该考虑用适配器，而是应该考虑通过重构统一接口".
- **Pattern enthusiasm**: 小菜's "我要经常性地使用它" gets a flat "NO！模式乱用不如不用".
- **Forcing the client to learn the adaptee's vocabulary**: making the coach learn Chinese, i.e. changing the whole client population to suit one component.
- **Bending your own system's interface to match a vendor's**: "完全没有必要为了迎合它而改动自己的接口" — adapt the vendor instead.

## Code Examples
Generic structure:
```java
class Target  { public void request() { System.out.println("普通请求!"); } }
class Adaptee { public void specificRequest() { System.out.println("特殊请求!"); } }

class Adapter extends Target {
    private Adaptee adaptee = new Adaptee();          // object adapter: composition
    public void request() { adaptee.specificRequest(); }
}

Target target = new Adapter();
target.request();   // client calls Target.request(); Adaptee.specificRequest() runs
```
- **What it demonstrates**: the client is unchanged; only the adapter knows both vocabularies.

Basketball translator:
```java
abstract class Player {
    protected String name;
    public Player(String name) { this.name = name; }
    public abstract void attack();
    public abstract void defense();
}
class Forwards extends Player { /* prints "前锋 name 进攻/防守" */ }
class Center   extends Player { /* prints "中锋 name 进攻/防守" */ }
class Guards   extends Player { /* prints "后卫 name 进攻/防守" */ }

// the Adaptee: right skills, different interface (Chinese method names, property-style name)
class ForeignCenter {
    private String name;
    public String getName() { return name; }
    public void setName(String value) { this.name = value; }
    public void 进攻() { System.out.println("外籍中锋 " + name + " 进攻"); }
    public void 防守() { System.out.println("外籍中锋 " + name + " 防守"); }
}

// the Adapter
class Translator extends Player {
    private ForeignCenter foreignCenter = new ForeignCenter();
    public Translator(String name) { super(name); foreignCenter.setName(name); }
    public void attack()  { foreignCenter.进攻(); }
    public void defense() { foreignCenter.防守(); }
}

Player forwards = new Forwards("巴蒂尔");   forwards.attack();
Player guards   = new Guards("麦克格雷迪"); guards.attack();
Player center   = new Translator("姚明");   center.attack(); center.defense();
```
- **What it demonstrates**: the coach's code (`Player.attack()/defense()`) never changes; `Translator` maps `attack`→`进攻`, `defense`→`防守`.

## Worked Example
Setting: 姚明 arrives in the NBA speaking no English. The coach and teammates will not learn Chinese; 姚明 cannot learn English overnight. Solution: a translator.

1. **Naive model**: `Player` abstract class with `attack()`/`defense()`; `Forwards`, `Center`, `Guards` subclasses; `new Center("姚明")`. Wrong — this pretends 姚明 already understands `attack`.
2. **Reality**: `ForeignCenter` is a separate class with methods `进攻()`/`防守()` and a property-style `name` (deliberately different from the constructor style of the other players, to emphasise it was written elsewhere).
3. **Three options**: teach 姚明 English (change the adaptee — unrealistic short-term), teach everyone Chinese (change every client — absurd), hire a translator (adapter).
4. **Adapter**: `Translator extends Player`, composes a `ForeignCenter`, forwards `attack()`→`进攻()`, `defense()`→`防守()`. The client line becomes `Player center = new Translator("姚明")` and the rest of the client is untouched.
5. **Real-world confirmation**: .NET's `DataAdapter` adapts SQL Server / Oracle / Access / DB2 sources into one `DataSet` via `Fill`/`Update`; Hibernate does something similar in Java.
6. **The brake**: 大鸟 tells the 扁鹊 story — the famous brother cures the gravely ill; the unknown eldest brother prevents illness. Adapter is the surgeon; good interface design is the eldest brother.

Why it works: composition lets the adapter present one interface while delegating to another, so mismatch is absorbed in exactly one class.

## Key Takeaways
1. Use Adapter when data and behaviour are correct but the interface is wrong *and* the mismatched class is outside your control.
2. Implement it as an object adapter in Java: inherit `Target`, compose `Adaptee`, forward each method.
3. It is legitimately a design-time choice when integrating a third-party component whose interface you should not mirror.
4. Inside your own codebase, fix naming with standards and refactoring first; adapting your own inconsistency is 事后控制.
5. Order of preference: prevent mismatch (事前) > refactor early (事中) > adapt (事后).
6. Do not adapt "because you can"; misused patterns are worse than no patterns.

## Connects To
- **[ch07](ch07-proxy.md)**: same wrapper shape; a proxy keeps the *same* interface and controls access, an adapter *changes* the interface.
- **[ch06](ch06-decorator.md)**: also wraps, but to add responsibilities while keeping the interface.
- **[ch12](ch12-facade.md)**: simplifies a subsystem's interface rather than converting one class's interface.
- **[ch22](ch22-bridge.md)**: 合成/聚合复用原则 — the object adapter is composition over inheritance in action.
- **[ch29](ch29-pattern-summary.md)**: Adapter is the audience-vote finalist; her "杀手锏" answer restates this chapter's when-to-use rule.
