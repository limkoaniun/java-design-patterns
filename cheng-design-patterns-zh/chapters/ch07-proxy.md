# 第7章：为别人做嫁衣——代理模式（Proxy）

## 核心思想
当一个对象不应或无法被直接访问时，在它前面放一个与它共享接口的替身，由替身转发调用。本章的故事：卓贾易通过朋友戴励追求娇娇；女孩从未见过真正的追求者，却收到了每一份礼物。

## 引入的框架
- **代理模式（Proxy）**——“为其他对象提供一种代理以控制对这个对象的访问。”[DP]
  - 结构：`«interface» ISubject { request() }`；`RealSubject implements ISubject`（代理所代表的真实实体）；`Proxy implements ISubject`（持有对 `RealSubject` 的引用，暴露相同的方法并委托给它）；`Client` 只与 `Proxy` 交互。
  - 适用场景：客户端必须间接访问某个对象；希望在不改动真实对象或客户端的前提下，在访问周围增加「内务处理」（记账、延迟加载、访问控制、远程调用）。
  - 做法：(1) 提取共享接口（`IGiveGift`）；(2) 让真实主题实现它；(3) 编写实现同一接口的代理，持有或创建真实主题，并转发每个方法；(4) 客户端只实例化代理。
  - 作者列举的四种应用 [DP]：
    1. **远程代理（remote proxy）**：为位于另一个地址空间的对象提供本地代表，并隐藏这一事实——例如在 Java 项目中添加 Web Service 时生成的 WSDL 客户端存根。
    2. **虚拟代理（virtual proxy）**：在创建开销大的对象真正被需要之前充当它的替身——例如浏览器在图片下载期间显示保存了图片路径和尺寸的占位框。
    3. **安全代理（protection proxy）**：当客户端拥有不同权限时，控制对真实对象的访问权限。
    4. **智能指引（smart reference）**：每次访问时做额外工作——引用计数以便释放对象、首次使用时把持久对象加载到内存、访问前检查锁。
  - 为什么有效 / 失败模式：代理引入了「一定程度的间接性」，额外的行为正是放在这层间接性里。失败模式：如果代理没有实现与真实主题相同的接口，客户端就无法互换使用它们，这个「代理」不过是另一个知道得太多的类（小菜的第二次尝试）。

## 关键概念
- **ISubject / Subject 接口**：共享接口，使 `Proxy` 能用在任何期望 `RealSubject` 的地方。
- **RealSubject**：真正干活的真实实体；代理“代表”它。
- **Proxy**：唯一同时认识真实主题和（故事中的）接收者的类；把调用转发给同名方法。
- **间接性（indirection）**：该模式的本质；每种应用都为这层间接性赋予不同的目的。
- **远程代理 / 虚拟代理 / 安全代理 / 智能指引**：上面列出的四种标准用途。
- **替身（stand-in）**：作者对代理的日常说法：真实对象的代表。

## 心智模型
- 把代理看作真实对象的代表：它必须能做真实对象的接口所承诺的一切，因此必须实现该接口。
- 当问题是「谁能在何时、以何种代价访问这个对象？」而不是「这个对象做什么？」时，使用代理。
- 需要远程代理的心智原型时，想想「生成的 Web Service 存根」；需要虚拟代理的心智原型时，想想「加载中网页里的图片占位框」。
- 在生活中识别这个模式：《武林外传》里吕秀才让燕小六去向郭芙蓉求婚就是一种代理——也提醒我们，客户端可能永远只看得到代理。

## 反模式
- **变成真实主题的代理**（小菜的第二版）：用 `Proxy` 替换 `Pursuit` 并让它承担真正的工作，意味着真实主题消失了；礼物变成了“戴励送的”，这是错误的。
- **没有共享接口的代理与真实主题**：客户端无法用其中一个替换另一个，于是模式的全部意义就丢失了。
- **认识真实主题的客户端**（第一版）：`Pursuit` 直接持有 `SchoolGirl`，即双方“彼此认识”，违背了访问必须受控的要求。
- **认为代理很少见**：作者明确反驳这一点：它是远程调用、延迟加载、安全和智能引用的基础。

## 代码示例
教科书形式：

```java
interface ISubject { void request(); }

class RealSubject implements ISubject {
    public void request() { System.out.println("真实的请求。"); }
}

class Proxy implements ISubject {
    private RealSubject rs;
    public Proxy() { this.rs = new RealSubject(); }
    public void request() { this.rs.request(); }   // forward; add bookkeeping here if needed
}

// client
Proxy proxy = new Proxy();
proxy.request();
```
- **演示了什么**：代理与真实主题共享 `ISubject`，因此客户端可以使用任意一个；代理持有引用并委托。

故事形式（「符合实际」的版本）：

```java
interface IGiveGift { void giveDolls(); void giveFlowers(); void giveChocolate(); }

class Pursuit implements IGiveGift {            // 追求者 = RealSubject
    private SchoolGirl mm;
    public Pursuit(SchoolGirl mm) { this.mm = mm; }
    public void giveDolls()     { System.out.println(mm.getName() + " 你好! 送你洋娃娃。"); }
    public void giveFlowers()   { System.out.println(mm.getName() + " 你好! 送你鲜花。"); }
    public void giveChocolate() { System.out.println(mm.getName() + " 你好! 送你巧克力。"); }
}

class Proxy implements IGiveGift {              // 代理 = the only class knowing both sides
    private Pursuit gg;
    public Proxy(SchoolGirl mm) { this.gg = new Pursuit(mm); }   // proxy init == real subject init
    public void giveDolls()     { gg.giveDolls(); }              // proxy "gives", real subject actually gives
    public void giveFlowers()   { gg.giveFlowers(); }
    public void giveChocolate() { gg.giveChocolate(); }
}

SchoolGirl girlLjj = new SchoolGirl(); girlLjj.setName("李娇娇");
Proxy boyDl = new Proxy(girlLjj);       // client only ever sees the proxy
boyDl.giveDolls(); boyDl.giveFlowers(); boyDl.giveChocolate();
```
- **演示了什么**：`Pursuit` 只是多了 `implements IGiveGift`；代理的构造函数创建真实主题，每个代理方法都调用同名的真实方法；客户端代码与“只有代理”的尝试相比没有变化，但语义现在正确了。

## 实战示例
1. **版本 1——没有代理**：`Pursuit` 持有 `SchoolGirl` 并直接送礼物。问题：故事要求两人彼此不认识；直接耦合违背了这一要求。
2. **版本 2——只有代理**：把 `Pursuit` 改名为 `Proxy`。问题：真正的追求者消失了；代码现在说的是戴励买了礼物并送出，这是假的。干活的代理不是代理。
3. **版本 3——带共享接口的代理**：注意到 `Pursuit` 和 `Proxy` 有相同的三个方法 → 二者都实现 `IGiveGift`。`Proxy` 在构造函数中创建 `Pursuit(mm)` 并转发。客户端代码与版本 2 保持一致。
4. **原因**：客户端（娇娇）只与代理打交道，却达成了效果（卓贾易送来礼物）；真实主题被隐藏，对它的访问由代理控制。同样的形态随后可推广到远程存根、延迟占位、权限检查和智能引用。

## 关键要点
1. 代理必须实现与真实主题相同的接口；这正是它可以被替换的原因。
2. 代理持有对真实主题的引用并转发同名调用；额外的行为（远程调用、延迟加载、安全、记账）都放在这层转发里。
3. 按意图选择代理的变体：远程、虚拟、保护或智能引用。
4. 不要让代理吞掉真正的工作；如果真实主题消失了，你只是给一个类改了名，并没有应用模式。
5. 代理是常见的基础设施（Web Service 存根、浏览器图片加载），不是什么奇特的模式。

## 关联章节
- **[ch06](ch06-decorator.md)**：装饰模式和代理模式都在同一接口后包装一个对象；装饰添加职责，代理控制访问。
- **[ch17](ch17-adapter.md)**：适配器模式同样包装，但会改变接口而不是保持接口。
- **[ch29](ch29-pattern-summary.md)**：比赛一章调侃代理小姐可能派了个替身来参赛：一句话说明这个模式。
- **[ch05](ch05-dependency-inversion.md)**：客户端依赖 `ISubject`，这是「针对接口编程」的一次应用。
