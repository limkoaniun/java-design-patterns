# Patterns & Principles — 大话设计模式

Compact cards. Story = the book's motivating example. Structure = the author's UML roles.

## Creational 创建型

### 简单工厂 Simple Factory (ch01)
**When to use**: few product types, creation logic in one place, change is rare.
**How**: `OperationFactory.createOperate("+")` switches on input and returns an `Operation` subclass; client calls `getResult()`.
**Trade-offs**: simplest; but every new product edits the factory `switch` (violates OCP). Fine as a first step and as the helper inside 策略/抽象工厂.

### 工厂方法 Factory Method (ch08)
**When to use**: you want to add products without editing existing code. "通常设计应该是从工厂方法开始".
**How**: `IFactory { createOperation() }`; one `ConcreteFactory` per product; client picks a factory, then calls the product's interface. Structure: Creator / ConcreteCreator / Product / ConcreteProduct.
**Trade-offs**: OCP-clean; moves the choice to the client and doubles the class count.

### 抽象工厂 Abstract Factory (ch15)
**When to use**: families of related products that must be swapped together (all DAOs for SQL Server vs MySQL).
**How**: `IFactory { createUser(); createDepartment() }` with one concrete factory per family. Reduce the factory explosion with 简单工厂 + `Class.forName(assemblyName + "." + db + "User")` + a properties file.
**Trade-offs**: swapping the family is one line; adding a *new product type* touches every factory.

### 建造者 Builder (ch13)
**When to use**: an object needs many ordered construction steps and the same steps yield different representations.
**How**: `PersonBuilder { buildHead(); buildBody(); ... }`; `PersonDirector.createPerson(builder)` enforces the order; concrete builders (瘦人/胖人) fill in details. Structure: Builder / ConcreteBuilder / Director / Product.
**Trade-offs**: guarantees no step is forgotten (炒面没放盐); overkill when construction is trivial.

### 原型 Prototype (ch09)
**When to use**: creating an object is expensive or you need many near-identical copies (简历).
**How**: implement `Cloneable`, override `clone()`; for reference fields (`WorkExperience`) clone them too for 深复制.
**Trade-offs**: hides construction cost; shallow copies silently share state.

### 单例 Singleton (ch21)
**When to use**: exactly one instance must exist and be globally reachable.
**How**: private constructor + `getInstance()`. Thread-safe variants: `synchronized`, 双重锁定 (`volatile` field, null-check outside and inside the lock), or 静态初始化 (`private static final Singleton instance = new Singleton()`).
**Trade-offs**: global state hides dependencies; 饿汉 creates early, 懒汉 needs locking.

## Structural 结构型

### 适配器 Adapter (ch17)
**When to use**: a needed class exists but its interface does not match (姚明 needs a 翻译); legacy or third-party code.
**How**: object adapter holds the Adaptee and implements Target (`Translator extends Player { ForeignCenter fc; attack() { fc.进攻(); } }`).
**Trade-offs**: no changes to either side; a sign of design debt if needed inside new code.

### 桥接 Bridge (ch22)
**When to use**: two independent axes of change (手机品牌 × 手机软件) would otherwise multiply subclasses.
**How**: `HandsetBrand` holds a `HandsetSoft`; each axis is its own hierarchy; `run()` delegates. Structure: Abstraction / RefinedAbstraction / Implementor / ConcreteImplementor.
**Trade-offs**: linear class growth; slightly more indirection.

### 组合 Composite (ch19)
**When to use**: tree of part–whole objects treated uniformly (总公司/分公司/部门).
**How**: `Component { add; remove; display }`; `Leaf` and `Composite` (holds `List<Component>`). 透明方式 keeps `add/remove` on Component; 安全方式 moves them to Composite.
**Trade-offs**: clients ignore leaf/composite difference; transparency costs leaf no-op methods.

### 装饰 Decorator (ch06)
**When to use**: add behaviours to an object dynamically, in a chosen order, without a subclass per combination (T恤 → 垮裤 → 破球鞋).
**How**: `Decorator extends Component` holding a `Component`; `decorate(c)` wraps; `show()` calls inner then adds its own. Structure: Component / ConcreteComponent / Decorator / ConcreteDecorator.
**Trade-offs**: removes conditional logic from the core class; order-dependent wrapping can confuse.

### 外观 Facade (ch12)
**When to use**: a subsystem is complex (股票/国债/房产) or you need a clean seam between layers (三层架构); also to wrap legacy code.
**How**: `Fund { buyFund(); sellFund(); }` calls the subsystem classes; client sees only Fund.
**Trade-offs**: simplifies clients; can become a god object if it grows logic.

### 享元 Flyweight (ch26)
**When to use**: huge numbers of similar objects (网站 templates per customer) with shared 内部状态.
**How**: `WebSiteFactory.getWebSiteCategory(key)` caches instances in a `Hashtable`; 外部状态 (`User`) is passed to `use(user)`.
**Trade-offs**: memory saved; state must be cleanly split; runtime a bit slower.

### 代理 Proxy (ch07)
**When to use**: control access to an object — 远程代理, 虚拟代理 (lazy load), 安全代理, 智能指引.
**How**: `Proxy implements GiveGift` holding a `Pursuit` real subject; client talks to the proxy (卓贾易 → 戴励 → 娇娇).
**Trade-offs**: adds a hop; keeps the real subject's interface intact.

## Behavioral 行为型

### 职责链 Chain of Responsibility (ch24)
**When to use**: several handlers might handle a request; handler chosen at runtime (加薪 by 经理 → 总监 → 总经理).
**How**: `Manager { setSuperior(m); requestApplications(req) }`; each handler handles or forwards. Structure: Handler / ConcreteHandler.
**Trade-offs**: sender decoupled from handler; a request may fall off the end unhandled.

### 命令 Command (ch23)
**When to use**: decouple the invoker (服务员) from the receiver (烤肉串者); support queues, logging, undo.
**How**: `Command { execute() }` holds a `Barbecuer`; `Waiter` keeps a `List<Command>` and calls `notify()` to run them. Structure: Invoker / Command / ConcreteCommand / Receiver.
**Trade-offs**: requests become first-class; many small classes.

### 解释器 Interpreter (ch27)
**When to use**: a simple, frequently recurring grammar (音乐符号 "O 2 E 0.5 G 0.5").
**How**: `Expression { interpret(PlayContext) }`; `Note`/`Scale` terminal expressions consume the context text.
**Trade-offs**: grammar changes are easy; complex grammars grow unmanageable.

### 迭代器 Iterator (ch20)
**When to use**: traverse a collection without exposing internals; multiple traversal orders.
**How**: `Iterator { first(); next(); isDone(); currentItem() }` over `Aggregate`; in Java just use `java.util.Iterator`/foreach.
**Trade-offs**: learn the structure, use the library.

### 中介者 Mediator (ch25)
**When to use**: many colleagues interact in a web (国家 via 联合国安理会); interaction logic should live in one place.
**How**: `UnitedNations { declare(msg, colleague) }`; colleagues hold a mediator, never each other. Structure: Mediator / ConcreteMediator / Colleague.
**Trade-offs**: colleagues stay simple; the mediator can become a controller-sized hotspot.

### 备忘录 Memento (ch18)
**When to use**: snapshot/rollback state without breaking encapsulation (游戏存进度).
**How**: `GameRole.saveState()` returns a `RoleStateMemento`; `RoleStateCaretaker` stores it; `recoveryState(memento)`. Structure: Originator / Memento / Caretaker.
**Trade-offs**: simple undo; large states cost memory.

### 观察者 Observer (ch14)
**When to use**: one subject changes and many dependents must update; subject should not know them.
**How**: `Subject { attach; detach; notify }`; observers implement `update()` via an *interface* (unrelated classes can subscribe). `java.util.Observable` saves code but is deprecated and blocks other inheritance; keep observers typed to a `Subject` interface, not `Boss`.
**Trade-offs**: loose coupling; can cause cascades and hidden ordering.

### 状态 State (ch16)
**When to use**: behaviour depends on state and `if/else` on a state field grows (工作状态 by hour).
**How**: `State { writeProgram(Work w) }`; each `ConcreteState` acts or sets `w.setState(next)` and re-dispatches. Structure: Context / State / ConcreteState.
**Trade-offs**: transitions explicit and local; many small classes.

### 策略 Strategy (ch02)
**When to use**: a family of interchangeable algorithms (正常收费/打折/返利).
**How**: `CashSuper { acceptCash(price, num) }`; `CashContext` holds one strategy; pair with 简单工厂 in the context constructor so the client only passes a string.
**Trade-offs**: removes algorithm `switch`es; client must know the strategies unless a factory hides them.

### 模板方法 Template Method (ch10)
**When to use**: several classes share an algorithm skeleton and differ only in steps (试卷 with different answers).
**How**: abstract `TestPaper.testQuestion1()` prints the question then calls abstract `answer1()`; subclasses override only the answers.
**Trade-offs**: reuse via inheritance; rigid if the skeleton itself varies.

### 访问者 Visitor (ch28)
**When to use**: stable element structure (男人/女人), operations that keep growing (成功/失败/恋爱).
**How**: `Person.accept(Action)` calls `action.getManConclusion(this)`; `ObjectStructure` holds elements and applies a visitor. Double dispatch.
**Trade-offs**: new operations are cheap; new element types touch every visitor.

## Principles 原则
See the principles table in SKILL.md (SRP ch03, OCP ch04, DIP/LSP ch05, LoD ch11, CARP ch22).
