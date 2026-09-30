# Chapter 26: 项目多也别傻做——享元模式 — Flyweight

## Core Idea
When you need thousands of nearly identical fine-grained objects, split each object's state into a shared intrinsic part and a per-use extrinsic part, keep one shared instance per intrinsic variant in a factory, and pass the extrinsic state in at call time.

## Frameworks Introduced
- **享元模式 (Flyweight)** — “运用共享技术有效地支持大量细粒度的对象。”[DP]
  - Structure: `Flyweight` (superclass/interface that accepts and acts on external state via `operation(extrinsicstate)`) → `ConcreteFlyweight` (adds storage for internal state) and `UnsharedConcreteFlyweight` (a subclass that does not need sharing; the interface makes sharing possible but not mandatory); `FlyweightFactory` creates and manages flyweights, returning an existing instance or creating one on demand.
  - When to use: (1) the application uses a large number of objects and they cause heavy storage overhead; (2) most object state can be made external, so that removing it lets relatively few shared objects replace many groups of objects.
  - How: (1) separate 内部状态 from 外部状态; (2) store only internal state in `ConcreteFlyweight`; (3) let the client hold or compute external state and pass it to `operation`; (4) fetch instances through a `FlyweightFactory` keyed on internal state (`Hashtable<String, Flyweight>`), lazily creating on miss.
  - Why it works / failure mode: savings grow with the number of shared instances and the amount of shared state. But the factory's registry costs resources, externalising state complicates client logic, and the whole design gets harder to read. Only worth it when there are enough instances to share.

## Key Concepts
- **内部状态 (intrinsic state)**: the part inside the flyweight that does not change with environment; shareable. Stone colour in 围棋.
- **外部状态 (extrinsic state)**: the part that changes with environment and cannot be shared; stored or computed by the client and passed in. Stone position.
- **FlyweightFactory**: the registry ensuring proper sharing; can pre-populate or create lazily on `null`.
- **UnsharedConcreteFlyweight**: the escape hatch for the occasional object that must not be shared.
- **String interning**: `"大话设计模式" == "大话设计模式"` is `true` for literals because the JVM shares one instance; `new String(...)` twice gives two references. The author's proof that you use Flyweight daily.
- **共享代码 (shared code)**: the business framing, one codebase and database serving many tenant sites distinguished by user id.

## Mental Models
- Think of 100 client websites as 2 flyweights (产品展示, 博客) plus 100 `User` objects, not 100 deployments.
- Use the 围棋 test: 361 positions but only 2 colours means 2 stone instances, not 300, if position is passed in.
- Think of a word processor: every 'a' on the page shares one character object; the glyph is intrinsic, the position is extrinsic.
- Prefer sharing when objects differ only in a few parameters; move those parameters outside and pass them in.

## Anti-patterns
- **One instance per tenant**: `new WebSite("产品展示")` six times for six customers; identical code and data structures duplicated, maintenance and server cost scale with customers.
- **Sharing without externalising**: the second version shares sites but cannot tell customers apart; sharing only works once the varying part (account) is moved out.
- **Flyweight for a handful of objects**: two or three personal blogs do not justify a registry and externalised state.
- **Forgetting the registry cost**: the list of all existing flyweights is itself overhead.

## Code Examples
Third version of the website exercise, with external state (`User`) passed in:

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
- **What it demonstrates**: the factory returns the same `ConcreteWebSite` for the same key; per-customer identity travels in `User`, so many users share two objects.

The GoF skeleton the author gives first uses the same shape: `Flyweight.operation(int extrinsicstate)`, `ConcreteFlyweight`, `UnsharedConcreteFlyweight`, and a `FlyweightFactory` pre-loading keys `"X"`, `"Y"`, `"Z"` into a `Hashtable`.

## Worked Example
1. **Version 1 (naive)**: 小菜 builds a product-showcase site, then copies the code to a new server for each friend-of-a-friend who wants one. Six sites of two kinds means six `WebSite` instances and six deployments; a bug fix must be applied everywhere and hosting cost cannot drop.
2. **Insight**: large blog/e-commerce platforms host thousands of "sites" on one codebase and database, distinguishing tenants by user id. Share the core, vary the data.
3. **Version 2 (shared, incomplete)**: abstract `WebSite`, `ConcreteWebSite`, and a `WebSiteFactory` that caches by category. Now "产品展示" is one instance however many times it is requested. 大鸟's objection: the customers have different accounts and data; this version expresses only what is shared, not what differs.
4. **Version 3 (intrinsic vs extrinsic)**: introduce `User` as external state and pass it to `use(User)`. Six users, two instances, and each call still knows whose site it is.
5. **Payoff**: 1,000 site orders of similar shape reduce to a few category classes, tiny server footprint, one place to maintain. The author closes with the same idea in the JVM: string literals are interned flyweights.

## Key Takeaways
1. Use Flyweight when object count is causing real storage overhead and most state can be externalised; otherwise skip it.
2. Split state deliberately: intrinsic stays in the flyweight, extrinsic is passed in by the client on every call.
3. Route creation through a factory keyed on intrinsic state; lazy creation on miss is fine.
4. Keep an unshared subclass available for the rare object that must be unique.
5. Savings scale with the number of shared instances; complexity is the fixed price, so the count must be large enough to pay it.
6. Java `String` literals already do this; `==` versus `equals` shows the difference between shared reference and equal value.

## Connects To
- **[ch21](ch21-singleton.md)**: Singleton is the degenerate case, one shared instance; Flyweight shares one instance per intrinsic variant.
- **[ch01](ch01-simple-factory.md)** / **[ch08](ch08-factory-method.md)**: `FlyweightFactory` is a creation-and-caching factory.
- **[ch09](ch09-prototype.md)**: Prototype copies objects; Flyweight avoids creating them at all.
- **[ch29](ch29-pattern-summary.md)**: the document-character example given by 享元 in the contest.
