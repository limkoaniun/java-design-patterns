# 模式与原则 — 大话设计模式

精简卡片。故事 = 书中引出模式的示例。结构 = 作者给出的 UML 角色。

## 创建型 Creational

### 简单工厂（Simple Factory）(ch01)
**何时使用**：产品类型少，创建逻辑集中在一处，很少变化。
**做法**：`OperationFactory.createOperate("+")` 根据输入做 switch，返回一个 `Operation` 子类；客户端调用 `getResult()`。
**取舍**：最简单；但每新增一个产品都要修改工厂的 `switch`（违反开放-封闭原则（OCP））。作为第一步，以及作为策略模式/抽象工厂模式内部的辅助手段都很合适。

### 工厂方法（Factory Method）(ch08)
**何时使用**：希望在不修改现有代码的前提下增加产品。"通常设计应该是从工厂方法开始"。
**做法**：`IFactory { createOperation() }`；每个产品对应一个 `ConcreteFactory`；客户端先选择工厂，再调用产品的接口。结构：Creator / ConcreteCreator / Product / ConcreteProduct。
**取舍**：符合开放-封闭原则；把选择权移交给客户端，且类的数量翻倍。

### 抽象工厂（Abstract Factory）(ch15)
**何时使用**：需要整体替换的一族相关产品（SQL Server 与 MySQL 的全部 DAO）。
**做法**：`IFactory { createUser(); createDepartment() }`，每个产品族一个具体工厂。用简单工厂模式 + `Class.forName(assemblyName + "." + db + "User")` + 属性文件来缓解工厂类的膨胀。
**取舍**：替换产品族只需改一行；但增加*新的产品类型*会波及每一个工厂。

### 建造者（Builder）(ch13)
**何时使用**：对象需要许多有序的构建步骤，且同样的步骤能产生不同的表示。
**做法**：`PersonBuilder { buildHead(); buildBody(); ... }`；`PersonDirector.createPerson(builder)` 保证顺序；具体建造者（瘦人/胖人）填充细节。结构：Builder / ConcreteBuilder / Director / Product。
**取舍**：保证不会漏掉任何步骤（炒面没放盐）；构建过程很简单时则是过度设计。

### 原型（Prototype）(ch09)
**何时使用**：创建对象代价高昂，或需要大量近乎相同的副本（简历）。
**做法**：实现 `Cloneable`，重写 `clone()`；对于引用字段（`WorkExperience`），也要克隆它们以实现深复制。
**取舍**：隐藏了构造成本；浅复制会悄悄共享状态。

### 单例（Singleton）(ch21)
**何时使用**：必须恰好存在一个实例，并且可被全局访问。
**做法**：私有构造函数 + `getInstance()`。线程安全的变体：`synchronized`、双重锁定（`volatile` 字段，在锁外和锁内各做一次 null 检查），或静态初始化（`private static final Singleton instance = new Singleton()`）。
**取舍**：全局状态会隐藏依赖；饿汉式提前创建，懒汉式需要加锁。

## 结构型 Structural

### 适配器（Adapter）(ch17)
**何时使用**：需要的类已存在，但接口不匹配（姚明需要翻译）；遗留代码或第三方代码。
**做法**：对象适配器持有 Adaptee 并实现 Target（`Translator extends Player { ForeignCenter fc; attack() { fc.进攻(); } }`）。
**取舍**：双方都无需改动；但若在新代码内部也需要它，则是设计债务的信号。

### 桥接（Bridge）(ch22)
**何时使用**：两个独立的变化维度（手机品牌 × 手机软件）否则会使子类成倍增加。
**做法**：`HandsetBrand` 持有一个 `HandsetSoft`；每个维度各自成一套继承层次；`run()` 进行委托。结构：Abstraction / RefinedAbstraction / Implementor / ConcreteImplementor。
**取舍**：类的数量线性增长；间接层稍多。

### 组合（Composite）(ch19)
**何时使用**：部分-整体的对象树需要被一致地对待（总公司/分公司/部门）。
**做法**：`Component { add; remove; display }`；`Leaf` 和 `Composite`（持有 `List<Component>`）。透明方式把 `add/remove` 保留在 Component 上；安全方式把它们移到 Composite 上。
**取舍**：客户端无需区分叶子与组合；透明性的代价是叶子要带上空操作方法。

### 装饰（Decorator）(ch06)
**何时使用**：动态地、按选定顺序给对象添加行为，而无需为每种组合都建一个子类（T恤 → 垮裤 → 破球鞋）。
**做法**：`Decorator extends Component` 并持有一个 `Component`；`decorate(c)` 进行包装；`show()` 先调用内部对象，再添加自己的行为。结构：Component / ConcreteComponent / Decorator / ConcreteDecorator。
**取舍**：从核心类中移除条件逻辑；依赖顺序的包装可能令人困惑。

### 外观（Facade）(ch12)
**何时使用**：子系统很复杂（股票/国债/房产），或需要在各层之间划出清晰的接缝（三层架构）；也可用来包装遗留代码。
**做法**：`Fund { buyFund(); sellFund(); }` 调用各个子系统类；客户端只看得到 Fund。
**取舍**：简化客户端；若在其中堆积逻辑，会变成上帝对象。

### 享元（Flyweight）(ch26)
**何时使用**：存在海量相似对象（每个客户的网站模板），且它们共享内部状态。
**做法**：`WebSiteFactory.getWebSiteCategory(key)` 把实例缓存在 `Hashtable` 中；外部状态（`User`）通过 `use(user)` 传入。
**取舍**：节省内存；状态必须清晰地拆分；运行时略慢。

### 代理（Proxy）(ch07)
**何时使用**：控制对某个对象的访问：远程代理、虚拟代理（延迟加载）、安全代理、智能指引代理。
**做法**：`Proxy implements GiveGift` 并持有一个 `Pursuit` 作为真实主题；客户端与代理交互（卓贾易 → 戴励 → 娇娇）。
**取舍**：多了一跳；真实主题的接口保持不变。

## 行为型 Behavioral

### 职责链（Chain of Responsibility）(ch24)
**何时使用**：多个处理者都可能处理某个请求；处理者在运行时选定（加薪依次经过经理 → 总监 → 总经理）。
**做法**：`Manager { setSuperior(m); requestApplications(req) }`；每个处理者要么处理，要么转发。结构：Handler / ConcreteHandler。
**取舍**：发送者与处理者解耦；请求可能走到链尾仍无人处理。

### 命令（Command）(ch23)
**何时使用**：把调用者（服务员）与接收者（烤肉串者）解耦；支持队列、日志、撤销。
**做法**：`Command { execute() }` 持有一个 `Barbecuer`；`Waiter` 保存一个 `List<Command>`，并调用 `notify()` 来执行它们。结构：Invoker / Command / ConcreteCommand / Receiver。
**取舍**：请求成为一等对象；产生许多小类。

### 解释器（Interpreter）(ch27)
**何时使用**：简单且频繁重复出现的文法（音乐符号「O 2 E 0.5 G 0.5」）。
**做法**：`Expression { interpret(PlayContext) }`；`Note`/`Scale` 终结符表达式消费上下文文本。
**取舍**：文法变更容易；复杂文法会变得难以管理。

### 迭代器（Iterator）(ch20)
**何时使用**：遍历集合而不暴露其内部结构；支持多种遍历顺序。
**做法**：`Iterator { first(); next(); isDone(); currentItem() }` 作用于 `Aggregate`；在 Java 中直接使用 `java.util.Iterator`/foreach 即可。
**取舍**：理解其结构，使用现成的库。

### 中介者（Mediator）(ch25)
**何时使用**：许多同事对象之间交互成网（各国通过联合国安理会）；交互逻辑应集中在一处。
**做法**：`UnitedNations { declare(msg, colleague) }`；同事持有中介者，而不持有彼此。结构：Mediator / ConcreteMediator / Colleague。
**取舍**：同事类保持简单；中介者可能变成控制器规模的热点。

### 备忘录（Memento）(ch18)
**何时使用**：在不破坏封装的前提下对状态做快照/回滚（游戏存进度）。
**做法**：`GameRole.saveState()` 返回一个 `RoleStateMemento`；`RoleStateCaretaker` 保存它；`recoveryState(memento)`。结构：Originator / Memento / Caretaker。
**取舍**：撤销简单；状态很大时会占用内存。

### 观察者（Observer）(ch14)
**何时使用**：一个主题发生变化，许多依赖方必须更新；主题不应认识它们。
**做法**：`Subject { attach; detach; notify }`；观察者通过一个*接口*实现 `update()`（互不相关的类也可以订阅）。`java.util.Observable` 能省代码，但已被弃用，并且会阻碍其他继承；让观察者依赖 `Subject` 接口类型，而不是 `Boss`。
**取舍**：松耦合；可能引发级联更新和隐蔽的顺序问题。

### 状态（State）(ch16)
**何时使用**：行为取决于状态，且针对状态字段的 `if/else` 越来越长（按钟点划分的工作状态）。
**做法**：`State { writeProgram(Work w) }`；每个 `ConcreteState` 要么执行动作，要么设置 `w.setState(next)` 并重新分派。结构：Context / State / ConcreteState。
**取舍**：状态转换明确且局部化；产生许多小类。

### 策略（Strategy）(ch02)
**何时使用**：一族可互换的算法（正常收费/打折/返利）。
**做法**：`CashSuper { acceptCash(price, num) }`；`CashContext` 持有一个策略；在上下文的构造函数中配合简单工厂模式，使客户端只需传入一个字符串。
**取舍**：消除算法的 `switch`；除非用工厂把策略隐藏起来，否则客户端必须了解这些策略。

### 模板方法（Template Method）(ch10)
**何时使用**：若干个类共享同一个算法骨架，只在某些步骤上不同（答案各不相同的试卷）。
**做法**：抽象的 `TestPaper.testQuestion1()` 先打印题目，再调用抽象的 `answer1()`；子类只重写答案。
**取舍**：通过继承实现复用；若骨架本身会变化则显得僵化。

### 访问者（Visitor）(ch28)
**何时使用**：元素结构稳定（男人/女人），而操作不断增加（成功/失败/恋爱）。
**做法**：`Person.accept(Action)` 调用 `action.getManConclusion(this)`；`ObjectStructure` 持有元素并应用访问者。双分派。
**取舍**：新增操作代价低；新增元素类型会波及每一个访问者。

## 原则 Principles
见 SKILL.md 中的原则表（单一职责原则（SRP）ch03，开放-封闭原则 ch04，依赖倒转原则（DIP）/里氏代换原则（LSP）ch05，迪米特法则（LoD）ch11，合成/聚合复用原则（CARP）ch22）。
