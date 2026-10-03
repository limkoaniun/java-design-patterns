# Chapter 12: 牛市股票还会亏钱？——外观模式 — Facade

## Core Idea
Put a single, simple high-level interface in front of a tangle of subsystem classes so callers deal with one object instead of many. Buy the fund; let the fund manager deal with a thousand stocks.

## Frameworks Introduced
- **外观模式 (Facade)，又叫门面模式** — “为子系统中的一组接口提供一个一致的界面，此模式定义了一个高层接口，这个接口使得这一子系统更加容易使用。”[DP]
  - Structure: `Client` → `Facade` (knows which subsystem classes handle a request and delegates to them; `methodA()`, `methodB()`) → `SubSystemOne..Four` (implement the work; hold **no** reference to the Facade).
  - When to use — the author's three stages [R2P]:
    1. **设计初期**: consciously separate layers (classic three-tier: put a Facade between data access and business logic, and between business logic and presentation) so coupling between layers stays low.
    2. **开发阶段**: as refactoring multiplies small classes, add a Facade so external callers do not have to learn them all.
    3. **维护遗留系统**: wrap a hard-to-change but essential legacy system in a Facade; new code talks to the Facade, the Facade talks to the legacy mess. Split the team: one group builds Facade↔legacy, the other builds against the Facade's interface.
  - How: (1) Identify the subsystem classes and the operations clients actually need. (2) Create one class holding references to those subsystem objects. (3) Expose coarse-grained methods that orchestrate calls. (4) Point clients at the Facade only; keep subsystem classes ignorant of it.
  - Why it works: it is “依赖倒转原则和迪米特法则” in pattern form — clients depend on one abstraction and know nothing about the subsystem's internals. Failure mode: a Facade that grows into a god object or that leaks subsystem types through its signatures.

## Key Concepts
- **子系统 (subsystem)**: a group of classes that together implement some functionality; complex to use directly.
- **高层接口 (high-level interface)**: the coarse operations the Facade exposes (`buyFund()` rather than four `buy()` calls).
- **耦合性过高 (excessive coupling)**: every investor touching every stock; in code, a client instantiating and calling many subsystem classes.
- **一致的界面 (uniform interface)**: the Facade presents one consistent surface even if subsystems are heterogeneous (stocks, bonds, property).
- **三层架构中的 Facade**: layer boundaries are natural Facade sites.
- **遗留系统封装**: wrapping legacy code so it can be used but not touched.

## Mental Models
- Think of the Facade as the 基金 (fund): investors interact with one product; the manager handles the portfolio.
- Use a Facade when a caller would otherwise need to know several classes *and* their call order.
- Prefer Facade over "let clients learn the subsystem" because it lets the subsystem evolve behind a stable surface.
- A Facade does not forbid direct subsystem access; it offers the easy path. Power users can still go around it.

## Anti-patterns
- **客户端直接操作所有子系统** (`stock1.buy(); stock2.buy(); nd1.buy(); rt1.buy(); ...`): the client is coupled to every concrete class and to the correct sequencing; adding a product means editing every client.
- **Subsystem knowing the Facade**: the structure diagram is explicit — subsystem classes hold no reference to the Facade; a back-reference reintroduces coupling.
- **Speculative gambling without a system** (大鸟's investing aside): random wins are luck; only a validated framework produces repeatable results. Same for design — copy a pattern without understanding the coupling it removes and you gain nothing.

## Code Examples
```java
// Subsystem classes (each has buy()/sell())
class Stock1        { public void buy(){ System.out.println("股票1买入"); }  public void sell(){ System.out.println("股票1卖出"); } }
class Stock2        { public void buy(){ System.out.println("股票2买入"); }  public void sell(){ System.out.println("股票2卖出"); } }
class NationalDebt1 { public void buy(){ System.out.println("国债1买入"); }  public void sell(){ System.out.println("国债1卖出"); } }
class Realty1       { public void buy(){ System.out.println("房地产1买入"); } public void sell(){ System.out.println("房地产1卖出"); } }

// Facade
class Fund {
    private Stock1 stock1 = new Stock1();
    private Stock2 stock2 = new Stock2();
    private NationalDebt1 nd1 = new NationalDebt1();
    private Realty1 rt1 = new Realty1();

    public void buyFund()  { stock1.buy();  stock2.buy();  nd1.buy();  rt1.buy();  }
    public void sellFund() { stock1.sell(); stock2.sell(); nd1.sell(); rt1.sell(); }
    // holdings ratios, rebalancing, etc. happen here — the client is never told
}

// Client
Fund fund1 = new Fund();
fund1.buyFund();
fund1.sellFund();
```
- **What it demonstrates**: the client's four-class, eight-call dependency collapses to one object with two methods.

```java
// Generic structure
class Facade {
    private SubSystemOne one = new SubSystemOne();
    private SubSystemTwo two = new SubSystemTwo();
    private SubSystemThree three = new SubSystemThree();
    private SubSystemFour four = new SubSystemFour();

    public void methodA() { one.methodOne(); two.methodTwo(); three.methodThree(); four.methodFour(); }
    public void methodB() { two.methodTwo(); three.methodThree(); }
}
Facade facade = new Facade();
facade.methodA();   // client need not know the subsystems exist
facade.methodB();
```
- **What it demonstrates**: Facade methods can compose different subsets of subsystem calls.

## Worked Example
**Naive version (股民炒股):** each investor instantiates `Stock1`, `Stock2`, `NationalDebt1`, `Realty1` and calls `buy()`/`sell()` on each. A colleague, 顾韵梅, keeps buying the stock that just rose and selling the one about to rise; in code terms, the client is doing the fund manager's job with none of the expertise, and every client duplicates the orchestration.

**What broke:** coupling. Investors are tied to many specific instruments; adding a product or changing allocation rules means editing every investor.

**Refactored (投资基金):** introduce `Fund` holding the instruments; expose `buyFund()` / `sellFund()`. Clients now hold one reference. Allocation, timing, and rebalancing become `Fund`'s concern and can change without touching clients. 小菜 immediately recognizes this as the basic shape of Facade before the pattern is even named.

**Generalized:** replace instruments with `SubSystemOne..Four`, `Fund` with `Facade`, and note the rule from the structure diagram: subsystems never reference the Facade.

## Key Takeaways
1. When a client must call several classes in a particular order, wrap that choreography in one Facade method.
2. Insert Facades at layer boundaries early; it is the cheapest way to keep three-tier architectures decoupled.
3. After heavy refactoring produces many small classes, a Facade restores usability without undoing the refactoring.
4. Wrap legacy systems in a Facade and build new features against the Facade, not the legacy code.
5. Keep subsystem classes ignorant of the Facade; the dependency points one way only.

## Connects To
- **[ch11](ch11-law-of-demeter.md)**: Facade is the structural realization of 最少知识原则 — the client knows one class.
- **[ch05](ch05-dependency-inversion.md)**: clients depend on a high-level interface rather than concrete subsystem details.
- **[ch25](ch25-mediator.md)**: Mediator also centralizes interaction, but between peers who talk back; Facade is one-directional.
- **[ch17](ch17-adapter.md)**: Adapter changes one interface to match another; Facade simplifies many into one.
- **[ch29](ch29-pattern-summary.md)**: Facade is a finalist in the pattern contest for its clarity and ubiquity.
