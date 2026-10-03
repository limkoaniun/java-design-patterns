---
name: cheng-design-patterns-zh
description: "程杰（Cheng Jie）所著 \"大话设计模式（Java溢彩加强版）\" 的知识库。在设计或重构Java/面向对象代码时运用23个GoF设计模式（Strategy/Factory/Decorator/Observer/State等，即策略/工厂/装饰/观察者/状态）或六大面向对象设计原则（单一职责、开放-封闭、依赖倒转、里氏代换、迪米特、合成/聚合复用），在相似模式之间做选择、学习本书或查阅其章节时使用。"
---

<!-- argument-hint: [模式名称（中/英）、原则、章节编号或设计问题] -->

# 大话设计模式（Java溢彩加强版）
**作者**: 程杰 (Cheng Jie) | **页数**: ~500 | **章节**: 30 (楔子 ch00 + ch01–ch29) | **生成日期**: 2026-09-30

## 使用方法

- **不带参数**——加载下方的设计原则与模式选择规则
- **指定主题**——询问 `策略模式`、`strategy`、`double-checked locking`、`商场收银`；我会找到并阅读相关章节
- **指定章节**——请求 `ch14`；我会加载该章节
- **浏览**——询问「有哪些章节？」即可查看完整索引

当你询问下方核心框架未覆盖的主题时，我会先阅读相关章节文件再作答。
模式名称同时以中文和英文建立索引。

---

## 核心框架与心智模型

### 作者的核心观点
设计模式是"面向对象编程思维的体操"。学全23个模式不是为了把23个都用上，而是为了养成三种本能：**封装变化**、**对象间松散耦合**、**针对接口编程**。书中每一次重构的目标都是可维护、可扩展、可复用、灵活性好的代码。

**设计模式四境界（Four stages of mastery）**：(1) 不懂模式，写出糟糕的代码 → (2) 懂几个模式，滥用它们 → (3) 全都懂，却被相似性困扰而犹豫不决 → (4) 运用自如，"无剑胜有剑"。过度设计是第二阶段的暂时症状；因害怕过度设计而不用模式则是因噎废食。

### 六大设计原则（评判每个模式的标尺）
| 原则 | 作者的表述 | 何时应用 |
|---|---|---|
| **单一职责原则（SRP）** | 就一个类而言，应该仅有一个引起它变化的原因 | 一个类有两个引起变化的原因 → 拆分（手机 vs 电子阅读器；俄罗斯方块的逻辑 vs 显示） |
| **开放-封闭原则（OCP）** | 软件实体（类、模块、函数等）应该可以扩展，但是不可修改 [ASD] | 通过新增类来扩展，而不是修改已能工作的类。只在变化真正出现的地方抽象；"拒绝不成熟的抽象和抽象本身一样重要" |
| **依赖倒转原则（DIP）** | 抽象不应该依赖细节，细节应该依赖于抽象 — 针对接口编程，不要对实现编程 | 高层模块应依赖接口（电脑的各模块插在主板上；收音机则是焊死的） |
| **里氏代换原则（LSP）** | 子类型必须能够替换掉它们的父类型 [ASD] | 任何使用基类型的地方，换成任意子类型都必须无需修改即可工作；正是它使依赖倒转原则和开放-封闭原则成为可能 |
| **迪米特法则（LoD / 最少知识原则）** | 如果两个类不必彼此直接通信，那么这两个类就不应当发生直接的相互作用；可以通过第三者转发这个调用 [J&DP] | 通过中介者/管理者转发调用；尽量降低成员的可见性（第一天上班应该找人事部，而不是自己去IT部门找人） |
| **合成/聚合复用原则（CARP）** | 尽量使用合成/聚合，尽量不要使用类继承 [J&DP] | 继承会泄露父类细节，并在两个变化维度下导致子类爆炸；改用对象合成（手机品牌 × 手机软件） |

### 模式选择：变化点决定模式
- **一族可互换的算法**（打折规则）→ **策略模式（Strategy）**；与简单工厂模式（Simple Factory）结合，使客户端永远看不到具体策略。策略模式 vs 状态模式：结构相同；策略模式由客户端选择，状态模式则随条件变化自行切换。
- **要创建哪个具体类** → 从 **工厂方法模式（Factory Method）** 开始（"通常设计应该是从工厂方法开始"）。简单工厂模式把 `switch` 集中在一处，违反了开放-封闭原则；工厂方法模式把创建推迟到子类；当你要创建成*系列*的相关产品时（SQL Server 与 Oracle 各自的全部 DAO），用 **抽象工厂模式（Abstract Factory）**。用简单工厂模式 + 反射 + 配置文件消除类爆炸。
- **在运行时以任意顺序为对象添加职责** → **装饰模式（Decorator）**（穿衣的顺序很重要）。当行为需要叠加结合时，优先用它而不是子类爆炸。
- **控制对某个对象的访问**（延迟加载、远程、权限、智能指引）→ **代理模式（Proxy）**；代理模式以相同接口包装一个对象，装饰模式添加行为，适配器模式改变接口。
- **让已有的不兼容接口能够配合使用** → **适配器模式（Adapter）**——只用于事后补救，针对遗留代码或第三方代码；绝不要把新代码设计成需要它。
- **子系统难以使用；分层** → **外观模式（Facade）**（基金屏蔽了股票/国债/房产）。外观模式是单向的简化；**中介者模式（Mediator）** 管理多对多的同级交互（安理会）。
- **算法骨架相同，步骤不同** → **模板方法模式（Template Method）**（试卷题目相同，答案各异）。基于继承；如果整个算法都在变，优先用策略模式。
- **一对多的变化通知，发送者不应知道接收者** → **观察者模式（Observer）**；把抽象观察者声明为*接口*，使无关的类也能订阅，并把通知者的类型声明为接口（而不是 `Boss`）。`java.util.Observable` 可用，但已被弃用，且会占用唯一的继承机会。
- **行为取决于状态，针对状态字段写了很长的 `if/else` 链** → **状态模式（State）**；由每个状态决定下一次转换（"方法过长是坏味道"）。
- **部分-整体的树形结构，叶子与组合被一致对待** → **组合模式（Composite）**（分公司 = 部门）。透明方式（叶子也实现 add/remove）vs 安全方式。
- **把请求作为对象**（撤销、排队、日志、解耦调用者与接收者）→ **命令模式（Command）**；当处理者要在运行时沿链传递才能确定时，用 **职责链模式（Chain of Responsibility）**（加薪逐级上报）；当你必须在不暴露内部的前提下保存并恢复状态时，用 **备忘录模式（Memento）**。
- **两个独立的变化维度** → **桥接模式（Bridge）**（抽象 × 实现，二者都通过合成连接）。桥接模式预先分离维度；装饰模式在单一维度上叠加行为。
- **大量细粒度对象共享内部状态** → **享元模式（Flyweight）**；把内部状态（共享）与外部状态（传入）分开。
- **一个对象，全局访问** → **单例模式（Singleton）**；在 Java 中优先用静态初始化（饿汉）或带 `volatile` 的双重锁定。
- **数据不同的对象副本** → 通过 `Cloneable` 实现 **原型模式（Prototype）**；要分清浅复制与深复制（`WorkExperience` 字段会被共享，除非你也克隆它）。
- **复杂对象分步构建，构建过程相同而表示不同** → **建造者模式（Builder）**（小人必须有头、身体、手臂、腿；由 Director 保证顺序）。
- **遍历集合而不暴露其结构** → **迭代器模式（Iterator）**（`java.util.Iterator` 已经提供；理解其结构，使用类库即可）。
- **稳定、简单且需反复解释的文法** → **解释器模式（Interpreter）**（音乐解释器）；当数据结构固定（男人/女人）而操作不断增加（成功/失败/恋爱）时，用 **访问者模式（Visitor）**。

### 商场收银演进阶梯（全书主线）
计算器/收银程序 → 简单工厂模式（ch01）→ 策略模式 + 简单工厂模式（ch02）→ + 装饰模式实现可叠加的促销（ch06）→ + 工厂方法模式（ch08）→ + 抽象工厂模式结合反射 + 配置文件（ch15）。每一步都由一个新需求驱动；可用它作为「该走多远」的模板。

---

## 章节索引

| # | 标题 | 关键框架 |
|---|-------|----------------|
| [ch00](chapters/ch00-oo-basics.md) | 楔子 培训实习生——面向对象基础 | 类/实例、封装、继承、多态、抽象类、接口、泛型 |
| [ch01](chapters/ch01-simple-factory.md) | 代码无错就是优？ | 简单工厂（Simple Factory）、复制 vs 复用、紧耦合 vs 松耦合、UML类图 |
| [ch02](chapters/ch02-strategy.md) | 商场促销 | 策略（Strategy）、策略+简单工厂 |
| [ch03](chapters/ch03-single-responsibility.md) | 电子阅读器vs.手机 | 单一职责原则（SRP） |
| [ch04](chapters/ch04-open-closed.md) | 考研求职两不误 | 开放-封闭原则（OCP） |
| [ch05](chapters/ch05-dependency-inversion.md) | 会修电脑不会修收音机？ | 依赖倒转原则（DIP）、里氏代换原则（LSP） |
| [ch06](chapters/ch06-decorator.md) | 穿什么有这么重要？ | 装饰（Decorator）、简单工厂+策略+装饰 |
| [ch07](chapters/ch07-proxy.md) | 为别人做嫁衣 | 代理（Proxy）：远程/虚拟/安全/智能指引 |
| [ch08](chapters/ch08-factory-method.md) | 工厂制造细节无须知 | 工厂方法（Factory Method）、简单工厂 vs 工厂方法 |
| [ch09](chapters/ch09-prototype.md) | 简历复印 | 原型（Prototype）、浅复制 vs 深复制 |
| [ch10](chapters/ch10-template-method.md) | 考题抄错会做也白搭 | 模板方法（Template Method） |
| [ch11](chapters/ch11-law-of-demeter.md) | 无熟人难办事？ | 迪米特法则（LoD） |
| [ch12](chapters/ch12-facade.md) | 牛市股票还会亏钱？ | 外观（Facade）、何时使用外观（三层架构） |
| [ch13](chapters/ch13-builder.md) | 好菜每回味不同 | 建造者（Builder）、Director |
| [ch14](chapters/ch14-observer.md) | 老板回来，我不知道 | 观察者（Observer）、接口 vs 抽象类、java.util.Observable |
| [ch15](chapters/ch15-abstract-factory.md) | 就不能不换DB吗？ | 抽象工厂（Abstract Factory）、反射、配置文件 |
| [ch16](chapters/ch16-state.md) | 无尽加班何时休 | 状态（State）、方法过长坏味道 |
| [ch17](chapters/ch17-adapter.md) | 在NBA我需要翻译 | 适配器（Adapter）：类/对象适配器 |
| [ch18](chapters/ch18-memento.md) | 如果再回到从前 | 备忘录（Memento）、Originator/Caretaker |
| [ch19](chapters/ch19-composite.md) | 分公司=一部门 | 组合（Composite）、透明方式 vs 安全方式 |
| [ch20](chapters/ch20-iterator.md) | 想走？可以！先买票 | 迭代器（Iterator）、java.util.Iterator |
| [ch21](chapters/ch21-singleton.md) | 有些类也需计划生育 | 单例（Singleton）、双重锁定、静态初始化 |
| [ch22](chapters/ch22-bridge.md) | 手机软件何时统一 | 桥接（Bridge）、合成/聚合复用原则（CARP） |
| [ch23](chapters/ch23-command.md) | 烤羊肉串引来的思考 | 命令（Command）、Invoker/Receiver、撤销/队列/日志 |
| [ch24](chapters/ch24-chain-of-responsibility.md) | 加薪非要老总批？ | 职责链（Chain of Responsibility） |
| [ch25](chapters/ch25-mediator.md) | 世界需要和平 | 中介者（Mediator）、Colleague |
| [ch26](chapters/ch26-flyweight.md) | 项目多也别傻做 | 享元（Flyweight）、内部状态 vs 外部状态 |
| [ch27](chapters/ch27-interpreter.md) | 其实你不懂老板的心 | 解释器（Interpreter）、音乐解释器 |
| [ch28](chapters/ch28-visitor.md) | 男人和女人 | 访问者（Visitor）、双分派 |
| [ch29](chapters/ch29-pattern-summary.md) | OOTV杯超级模式大赛——模式总结 | 创建型/结构型/行为型分类、相似模式对比、决赛应用题 |

## 主题索引

- **抽象工厂（Abstract Factory）** → ch15, ch29
- **适配器（Adapter）** → ch17, ch29
- **桥接（Bridge）** → ch22
- **建造者（Builder）** → ch13
- **职责链（Chain of Responsibility）** → ch24
- **内聚与耦合（Cohesion & coupling）、紧耦合 vs 松耦合** → ch01, ch22, ch29
- **命令（Command）** → ch23
- **组合（Composite）** → ch19
- **合成/聚合复用原则（Composition over inheritance，CARP）** → ch22, ch29
- **反射+配置文件（Configuration file + reflection）** → ch15
- **装饰（Decorator）** → ch06
- **依赖倒转原则（Dependency Inversion，DIP）** → ch05
- **双重锁定（Double-checked locking）、volatile** → ch21
- **外观（Facade）、三层架构（three-tier architecture）** → ch12
- **工厂方法（Factory Method）** → ch08, ch15, ch29
- **享元（Flyweight）** → ch26
- **接口 vs 抽象类（Interface vs abstract class）** → ch00
- **解释器（Interpreter）** → ch27
- **迭代器（Iterator）** → ch20
- **迪米特法则（Law of Demeter）、最少知识原则** → ch11, ch25
- **里氏代换原则（Liskov Substitution，LSP）** → ch05
- **中介者（Mediator）** → ch25
- **备忘录（Memento）** → ch18
- **观察者（Observer）、java.util.Observable** → ch14, ch29
- **开放-封闭原则（Open-Closed，OCP）** → ch04, ch08, ch29
- **多态、继承、封装（Polymorphism, inheritance, encapsulation）** → ch00, ch01
- **原型（Prototype）、深复制 浅复制（deep vs shallow copy）** → ch09
- **代理（Proxy）** → ch07
- **重构（Refactoring）、坏味道（code smells）** → ch00, ch01, ch10, ch16
- **商场收银（Shopping-mall checkout）** → ch02, ch06, ch08, ch15
- **简单工厂（Simple Factory）** → ch01, ch02, ch08, ch15
- **单一职责原则（Single Responsibility，SRP）** → ch03
- **单例（Singleton）** → ch21
- **状态（State）** → ch16
- **策略（Strategy）** → ch02, ch29
- **模板方法（Template Method）** → ch10
- **UML类图（UML class diagrams）** → ch01
- **访问者（Visitor）、双分派（double dispatch）** → ch28

## 辅助文件

- [glossary.md](glossary.md) — 全部关键术语及其定义（中/英）
- [patterns.md](patterns.md) — 23个模式与6条原则，整理为何时用/如何用/权衡卡片
- [cheatsheet.md](cheatsheet.md) — 决策规则、相似模式辨析、坏味道 → 模式

---

## 范围与限制

本技能仅涵盖书中内容。若要在你的代码库中动手实现，
请结合项目专用工具。超出本书范围的主题，请查阅相关技能
或直接询问智能体。

来源说明：所用 PDF 中的全部代码清单和 UML 图均以图片形式嵌入。
它们经 OCR 识别并人工整理；章节文件中的代码是忠实的
精简重构，并非逐字照抄，在细节上（变量名、注释）可能与印刷版清单
略有差异。
