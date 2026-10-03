# 第26章：项目多也别傻做——享元模式（Flyweight）

## 核心思想
当需要成千上万个几乎相同的细粒度对象时，把每个对象的状态拆成可共享的内部状态和每次使用时不同的外部状态，在工厂中为每种内部状态变体只保留一个共享实例，并在调用时传入外部状态。

## 引入的框架
- **享元模式（Flyweight）** — “运用共享技术有效地支持大量细粒度的对象。”[DP]
  - 结构：`Flyweight`（超类或接口，通过 `operation(extrinsicstate)` 接收并作用于外部状态）→ `ConcreteFlyweight`（增加内部状态的存储）和 `UnsharedConcreteFlyweight`（不需要共享的子类；接口使共享成为可能，但并不强制共享）；`FlyweightFactory` 负责创建和管理享元，返回已有实例或按需创建。
  - 适用场景：(1) 应用程序使用了大量对象，造成很大的存储开销；(2) 对象的大多数状态都可以变为外部状态，剥离外部状态之后，可以用相对较少的共享对象取代多组对象。
  - 做法：(1) 区分内部状态与外部状态；(2) `ConcreteFlyweight` 中只存储内部状态；(3) 由客户端保存或计算外部状态，并传给 `operation`；(4) 通过以内部状态为键的 `FlyweightFactory`（`Hashtable<String, Flyweight>`）获取实例，未命中时延迟创建。
  - 为何有效 / 失败模式：节省的开销随共享实例的数量和共享状态的多少而增长。但工厂的注册表本身要消耗资源，把状态外部化会使客户端逻辑变复杂，整个设计也更难阅读。只有在可共享的实例足够多时才值得使用。

## 关键概念
- **内部状态（intrinsic state）**：享元内部不随环境变化的部分，可以共享。例如围棋中棋子的颜色。
- **外部状态（extrinsic state）**：随环境变化、不能共享的部分，由客户端存储或计算并传入。例如棋子的位置。
- **FlyweightFactory**：确保正确共享的注册表；可以预先填充，也可以在得到 `null` 时延迟创建。
- **UnsharedConcreteFlyweight**：为偶尔出现、不得共享的对象留的逃生口。
- **字符串驻留（String interning）**：对于字面量，`"大话设计模式" == "大话设计模式"` 为 `true`，因为 JVM 共享同一个实例；两次 `new String(...)` 则得到两个引用。这是作者给出的证明，说明你每天都在使用享元模式。
- **共享代码（shared code）**：业务层面的说法，一套代码和数据库服务于许多租户网站，以用户 id 区分。

## 心智模型
- 把 100 个客户网站看作 2 个享元（产品展示、博客）加 100 个 `User` 对象，而不是 100 套部署。
- 用围棋来检验：361 个位置但只有 2 种颜色，意味着只要把位置传入，就只需 2 个棋子实例，而不是 300 个。
- 想想文字处理器：页面上每个「a」共用一个字符对象；字形是内部状态，位置是外部状态。
- 当对象只在少数几个参数上不同时，优先考虑共享；把这些参数移到外部再传入。

## 反模式
- **每个租户一个实例**：为六个客户 `new WebSite("产品展示")` 六次；相同的代码和数据结构被重复，维护成本和服务器成本随客户数增长。
- **只共享不外部化**：第二版共享了网站，却无法区分客户；只有把变化的部分（账号）移到外部，共享才行得通。
- **为少数几个对象使用享元模式**：两三个个人博客不值得为之建立注册表和外部化状态。
- **忘记注册表的成本**：所有现存享元的列表本身就是开销。

## 代码示例
网站练习的第三版，传入外部状态（`User`）：

```java
// External state
class User {
    private String name;
    public User(String value) { this.name = value; }
    public String getName() { return this.name; }
}
// Flyweight
abstract class WebSite {
    public abstract void use(User user);
}
// ConcreteFlyweight: internal state = site category
class ConcreteWebSite extends WebSite {
    private String name = "";
    public ConcreteWebSite(String name) { this.name = name; }
    public void use(User user) {
        System.out.println("网站分类: " + name + " 用户: " + user.getName());
    }
}
// FlyweightFactory: create on miss, share on hit
class WebSiteFactory {
    private Hashtable<String, WebSite> flyweights = new Hashtable<String, WebSite>();
    public WebSite getWebSiteCategory(String key) {
        if (!flyweights.containsKey(key))
            flyweights.put(key, new ConcreteWebSite(key));
        return (WebSite) flyweights.get(key);
    }
    public int getWebSiteCount() { return flyweights.size(); }
}
// Client: six users, two instances
WebSiteFactory f = new WebSiteFactory();
WebSite fx = f.getWebSiteCategory("产品展示");
fx.use(new User("小菜"));
WebSite fy = f.getWebSiteCategory("产品展示");
fy.use(new User("大鸟"));
WebSite fl = f.getWebSiteCategory("博客");
fl.use(new User("老顽童"));
WebSite fm = f.getWebSiteCategory("博客");
fm.use(new User("桃谷六仙"));
System.out.println("网站分类总数为:" + f.getWebSiteCount()); // 2
```
- **演示了什么**：对同一个键，工厂返回同一个 `ConcreteWebSite`；每个客户的身份通过 `User` 传递，因此许多用户共享两个对象。

作者最先给出的 GoF 骨架采用同样的形态：`Flyweight.operation(int extrinsicstate)`、`ConcreteFlyweight`、`UnsharedConcreteFlyweight`，以及一个把键 `"X"`、`"Y"`、`"Z"` 预先装入 `Hashtable` 的 `FlyweightFactory`。

## 实战示例
1. **第一版（朴素）**：小菜做了一个产品展示网站，之后每当朋友的朋友想要一个，就把代码复制到新服务器上。两类共六个网站，意味着六个 `WebSite` 实例和六套部署；修复一个 bug 要在所有地方都改一遍，托管成本也降不下来。
2. **洞察**：大型博客/电商平台在同一套代码和数据库上托管成千上万个「网站」，以用户 id 区分租户。共享核心，改变数据。
3. **第二版（已共享，但不完整）**：抽象的 `WebSite`、`ConcreteWebSite`，以及按分类缓存的 `WebSiteFactory`。现在无论请求多少次，「产品展示」都只有一个实例。大鸟的反对意见：客户的账号和数据各不相同；这一版只表达了共享的部分，没有表达不同的部分。
4. **第三版（内部状态与外部状态）**：引入 `User` 作为外部状态，并传给 `use(User)`。六个用户，两个实例，每次调用仍然知道这是谁的网站。
5. **收益**：1,000 个形态相似的网站订单缩减为少数几个分类类，服务器占用极小，维护只在一处。作者以 JVM 中的同一思想收尾：字符串字面量就是被驻留的享元。

## 关键要点
1. 当对象数量确实造成存储开销、且大部分状态可以外部化时，才使用享元模式；否则跳过。
2. 有意识地拆分状态：内部状态留在享元中，外部状态由客户端在每次调用时传入。
3. 创建统一经过以内部状态为键的工厂；未命中时延迟创建即可。
4. 为偶尔必须唯一的对象保留一个不共享的子类。
5. 节省的开销随共享实例的数量而增长；复杂度是固定的代价，所以实例数量必须大到足以抵偿。
6. Java 的 `String` 字面量已经在这么做了；`==` 与 `equals` 的区别体现了共享引用与相等值之间的差异。

## 关联章节
- **[ch21](ch21-singleton.md)**：单例模式（Singleton）是退化的特例，只有一个共享实例；享元模式为每种内部状态变体共享一个实例。
- **[ch01](ch01-simple-factory.md)** / **[ch08](ch08-factory-method.md)**：`FlyweightFactory` 是一个负责创建并缓存的工厂。
- **[ch09](ch09-prototype.md)**：原型模式（Prototype）复制对象；享元模式则根本避免创建对象。
- **[ch29](ch29-pattern-summary.md)**：比赛中享元模式给出的文档字符示例。
