# Chapter 7: 为别人做嫁衣——代理模式 — Proxy

## Core Idea
When one object should not, or cannot, be reached directly, put a stand-in that shares its interface in front of it and let the stand-in forward the calls. The chapter's story: 卓贾易 courts 娇娇 through his friend 戴励; the girl never meets the real suitor, yet receives every gift.

## Frameworks Introduced
- **代理模式 (Proxy)** — “为其他对象提供一种代理以控制对这个对象的访问。”[DP]
  - Structure: `«interface» ISubject { request() }`; `RealSubject implements ISubject` (the real entity the proxy represents); `Proxy implements ISubject` (holds a reference to `RealSubject`, exposes the same method and delegates to it); `Client` talks only to `Proxy`.
  - When to use: the client must access an object indirectly; you want to add "内务处理" (bookkeeping, laziness, access control, remoting) around access without changing the real object or the client.
  - How: (1) extract the shared interface (`IGiveGift`); (2) have the real subject implement it; (3) write a proxy that implements the same interface, owns/creates the real subject, and forwards each method; (4) client instantiates only the proxy.
  - Four applications the author enumerates [DP]:
    1. **远程代理 (remote proxy)**: a local representative for an object in another address space, hiding that fact — e.g. the generated WSDL client stubs when you add a Web Service to a Java project.
    2. **虚拟代理 (virtual proxy)**: stands in for an expensive-to-create object until it is really needed — e.g. a browser shows placeholder frames holding image path and size while images download.
    3. **安全代理 (protection proxy)**: controls access rights to the real object when clients have different permissions.
    4. **智能指引 (smart reference)**: does extra work on each access — reference counting to free the object, loading a persistent object into memory on first use, checking locks before access.
  - Why it works / failure mode: proxy introduces "一定程度的间接性" and that indirection is where the extra behaviour lives. Failure mode: if the proxy does not implement the same interface as the real subject, the client can't treat them interchangeably and the "proxy" is just another class that knows too much (小菜's second attempt).

## Key Concepts
- **ISubject / Subject 接口**: the shared interface that lets `Proxy` be used anywhere `RealSubject` is expected.
- **RealSubject**: the real entity that does the work; the proxy "represents" it.
- **Proxy**: the only class that knows both the real subject and (in the story) the recipient; forwards calls to same-named methods.
- **间接性 (indirection)**: the essence of the pattern; each application adds a different purpose to the indirection.
- **远程代理 / 虚拟代理 / 安全代理 / 智能指引**: the four standard purposes listed above.
- **替身 (stand-in)**: the author's everyday word for a proxy: the real object's representative.

## Mental Models
- Think of a proxy as the real object's representative: it must be able to do everything the real object's interface promises, so it must implement that interface.
- Use a proxy when the question is "who is allowed to reach this object, when, and at what cost?" rather than "what does this object do?"
- Think "generated Web Service stub" when you need a mental prototype of a remote proxy, and "image placeholder in a loading web page" for a virtual proxy.
- Recognise the pattern in life: 吕秀才 sending 燕小六 to propose to 郭芙蓉 in 《武林外传》 is a proxy — and a reminder that the client may only ever see the proxy.

## Anti-patterns
- **Proxy that becomes the real subject** (小菜's second version): replacing `Pursuit` with `Proxy` and giving it the real work means the real subject vanishes; the gifts are now "sent by 戴励", which is wrong.
- **Proxy and real subject without a shared interface**: the client can't substitute one for the other, so you lose the whole point of the pattern.
- **Client that knows the real subject** (first version): `Pursuit` holds `SchoolGirl` directly, i.e. the two parties "know each other", contradicting the requirement that access be controlled.
- **Assuming proxy is rare**: the author explicitly counters this: it underlies remoting, lazy loading, security and smart references.

## Code Examples
Textbook form:

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
- **What it demonstrates**: the proxy and the real subject share `ISubject`, so the client can use either; the proxy owns the reference and delegates.

Story form (the version that "符合实际"):

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
- **What it demonstrates**: `Pursuit` only gained `implements IGiveGift`; the proxy constructor builds the real subject and every proxy method calls the same-named real method; the client code is unchanged from the "proxy only" attempt but now the semantics are right.

## Worked Example
1. **Version 1 — no proxy**: `Pursuit` holds a `SchoolGirl` and sends gifts directly. Problem: the story requires that the two never know each other; direct coupling contradicts the requirement.
2. **Version 2 — proxy only**: rename `Pursuit` to `Proxy`. Problem: the real suitor disappears; the code now says 戴励 bought and sent the gifts, which is false. A proxy that does the work is not a proxy.
3. **Version 3 — proxy with shared interface**: notice `Pursuit` and `Proxy` have the same three methods → both implement `IGiveGift`. `Proxy` creates `Pursuit(mm)` in its constructor and forwards. Client code stays identical to version 2.
4. **Why**: the client (娇娇) deals only with the proxy, yet the effect (gifts from 卓贾易) is achieved; the real subject is hidden and access to it is controlled by the proxy. The same shape then generalises to remote stubs, lazy placeholders, permission checks and smart references.

## Key Takeaways
1. A proxy must implement the same interface as the real subject; that is what makes it substitutable.
2. The proxy holds the reference to the real subject and forwards same-named calls; extra behaviour (remoting, laziness, security, bookkeeping) lives in that forwarding layer.
3. Choose the proxy variant by intent: remote, virtual, protection, or smart reference.
4. Do not let the proxy absorb the real work; if the real subject vanishes you have renamed a class, not applied a pattern.
5. Proxy is common infrastructure (Web Service stubs, browser image loading), not an exotic pattern.

## Connects To
- **[ch06](ch06-decorator.md)**: decorator and proxy both wrap an object behind the same interface; decorator adds responsibilities, proxy controls access.
- **[ch17](ch17-adapter.md)**: adapter also wraps, but changes the interface rather than preserving it.
- **[ch29](ch29-pattern-summary.md)**: the contest chapter jokes that 代理小姐 may have sent a stand-in to compete: the pattern in one line.
- **[ch05](ch05-dependency-inversion.md)**: the client depends on `ISubject`, an application of "针对接口编程".
