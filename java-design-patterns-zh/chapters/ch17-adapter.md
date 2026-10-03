# 第17章：在NBA我需要翻译——适配器模式（Adapter）

## 核心思想
当你需要的类已经存在且能正常工作，但它的接口与客户端期望的不一致，而且双方都无法合理修改时，就用适配器把它包装起来做转换。适配器模式（Adapter）是一种后期工具，属于「亡羊补牢」：先防止接口不匹配，其次重构，只有在双方都已冻结时才使用适配。

## 引入的框架
- **适配器模式（Adapter）** — “将一个类的接口转换成客户希望的另外一个接口。Adapter模式使得原本由于接口不兼容而不能一起工作的那些类可以一起工作。”[DP]
  - 结构：`Target`（`request()`，客户端所期望的接口，可以是具体类、抽象类或接口）← `Adapter`（继承/实现 Target，持有私有的 `Adaptee`，其 `request()` 调用 `adaptee.specificRequest()`）；`Adaptee`（`specificRequest()`，被适配的类）。
  - 适用场景："两个类所做的事情相同或相似，但是具有不同的接口时"；复用遗留代码或第三方组件，而其接口你不会也不能修改。
  - 做法：(1) 确定客户端已在调用的 `Target` 接口；(2) 创建继承 `Target` 的 `Adapter`；(3) 在其内部合成 `Adaptee`；(4) 通过转发到 Adaptee 中名称不同的方法来实现每个 Target 方法。
- **类适配器 vs 对象适配器（class vs object adapter）** — GoF 两种形式都有描述；类适配器需要多重继承，而 Java/C#/VB.NET 不支持，所以本书只讲*对象适配器*（合成）。
- **扁鹊三兄弟（the three physician brothers）** — 作者的时机启发法：事前控制（设计一致的接口）> 事中控制（立即重构小的不匹配）> 事后控制（别无他法时才适配）。

## 关键概念
- **Target**："这是客户所期待的接口"。
- **Adaptee**："需要适配的类" — 数据和行为正确，接口错误。
- **Adapter**："通过在内部包装一个Adaptee对象，把源接口转换成目标接口"。
- **接口不符（interface mismatch）**：系统的数据和行为都是对的，只是方法名/签名不同。
- **控制范围之外（outside your control）**：触发条件 — 被适配者是遗留代码、其他团队的代码或供应商组件。
- **DataAdapter (.NET)**：作者的真实案例；`Fill` 和 `Update` 在任意数据源与统一的 `DataSet` 之间做映射。
- **翻译者（Translator）**：本章的适配器，让说英语的教练能够指挥说中文的中锋。

## 心智模型
- 把适配器想成**旅行转换插头**：它改变的是插座的形状，而不是电。
- 当你本来会说「如果那个类的方法叫 X 我就会用它」时，就用适配器模式。
- 相比事后适配，更应在设计时就调整接口："如果是在设计阶段，你有必要把类似的功能类的接口设计得不同吗？"
- 适配器的存在若是因为*你自己的团队*命名不一致，那是缺少命名规范的症状，而不是模式的成功。

## 反模式
- **用适配代替重构**：当两个类都是你的且可以修改时，应统一接口；"首先不应该考虑用适配器，而是应该考虑通过重构统一接口"。
- **模式狂热**：小菜说"我要经常性地使用它"，得到的是干脆的"NO！模式乱用不如不用"。
- **强迫客户端学习被适配者的词汇**：让教练去学中文，即为了迎合一个组件而改变整个客户端群体。
- **为迎合供应商而扭曲自己系统的接口**："完全没有必要为了迎合它而改动自己的接口" — 应该适配供应商。

## 代码示例
通用结构：
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
- **演示内容**：客户端不变；只有适配器同时懂得两套词汇。

篮球翻译：
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
- **演示内容**：教练的代码（`Player.attack()/defense()`）从不改变；`Translator` 把 `attack` 映射到 `进攻`，把 `defense` 映射到 `防守`。

## 实战示例
背景：姚明来到 NBA，不会说英语。教练和队友不会学中文；姚明也不可能一夜之间学会英语。解决办法：请一位翻译。

1. **朴素模型**：`Player` 抽象类带有 `attack()`/`defense()`；子类 `Forwards`、`Center`、`Guards`；`new Center("姚明")`。这是错的 — 它假装姚明已经听得懂 `attack`。
2. **现实情况**：`ForeignCenter` 是一个独立的类，方法为 `进攻()`/`防守()`，`name` 是属性风格（刻意与其他球员的构造器风格不同，以强调它写自别处）。
3. **三种选择**：教姚明英语（修改被适配者 — 短期内不现实）、教所有人中文（修改每个客户端 — 荒谬）、雇一个翻译（适配器）。
4. **适配器模式**：`Translator extends Player`，合成一个 `ForeignCenter`，把 `attack()` 转发到 `进攻()`，把 `defense()` 转发到 `防守()`。客户端那一行变成 `Player center = new Translator("姚明")`，客户端其余部分不动。
5. **现实世界的印证**：.NET 的 `DataAdapter` 通过 `Fill`/`Update` 把 SQL Server / Oracle / Access / DB2 数据源适配成一个 `DataSet`；Java 中 Hibernate 也做了类似的事。
6. **刹车**：大鸟讲了扁鹊的故事 — 有名的哥哥治疗重病，无名的大哥预防疾病。适配器模式是外科医生；良好的接口设计是大哥。

为什么有效：合成让适配器对外呈现一个接口，同时委托给另一个接口，因此不匹配只被一个类吸收。

## 关键要点
1. 当数据和行为正确但接口错误，*并且*不匹配的类在你的控制范围之外时，使用适配器模式。
2. 在 Java 中实现为对象适配器：继承 `Target`，合成 `Adaptee`，转发每个方法。
3. 集成第三方组件而你不应照搬其接口时，这确实是一种设计期的选择。
4. 在你自己的代码库内，先用规范和重构修正命名；适配自己的不一致属于事后控制。
5. 优先顺序：防止不匹配（事前）> 尽早重构（事中）> 适配（事后）。
6. 不要「因为能做」就去适配；乱用的模式比没有模式更糟。

## 关联章节
- **[ch07](ch07-proxy.md)**：包装的形状相同；代理模式（Proxy）保持*相同*的接口并控制访问，适配器*改变*接口。
- **[ch06](ch06-decorator.md)**：同样是包装，但目的是在保持接口不变的情况下增加职责。
- **[ch12](ch12-facade.md)**：简化一个子系统的接口，而不是转换单个类的接口。
- **[ch22](ch22-bridge.md)**：合成/聚合复用原则（CARP） — 对象适配器就是合成优于继承的实际体现。
- **[ch29](ch29-pattern-summary.md)**：适配器模式是观众投票的决赛选手；她的「杀手锏」回答重申了本章的适用规则。
