# Chapter 25: 世界需要和平——中介者模式 — Mediator

## Core Idea
When many objects must all know each other, the web of references makes the system an indivisible lump. Route every interaction through one mediator so colleagues only know the mediator, turning a mesh (网状) into a star (星状) centred on it.

## Frameworks Introduced
- **中介者模式 (Mediator)** — “用一个中介对象来封装一系列的对象交互。中介者使各对象不需要显式地相互引用，从而使其耦合松散，而且可以独立地改变它们之间的交互。”[DP]
  - Structure: `Mediator` (abstract, declares `send(message, colleague)`) → `ConcreteMediator` (knows every `ConcreteColleague`, receives messages and issues commands); `Colleague` (abstract, holds a `Mediator` reference) → `ConcreteColleague1/2` (know only their own behaviour plus the mediator).
  - When to use: a group of objects communicates in a well-defined but complex way (the author's example: every control on a Form/aspx page talks through the form), or you want to customise behaviour spread across many classes without spawning subclasses.
  - How: (1) give every colleague a constructor that receives the mediator; (2) colleagues call `mediator.send(msg, this)` instead of calling each other; (3) the concrete mediator decides which colleague's `notify` to invoke; (4) if you cannot foresee more than one mediator, merge `Mediator` and `ConcreteMediator` into one class.
  - Why it works / failure mode: coupling moves from N×N colleague links to N links into the mediator. The cost is that all interaction complexity lands in `ConcreteMediator`; with many colleagues it becomes the most complex, most fragile class in the system.

## Key Concepts
- **网状 → 星状**: the structural effect of a mediator, every node connects to the hub rather than to each other.
- **Colleague (同事类)**: a participant that knows its own behaviour and the mediator, nothing about other colleagues.
- **ConcreteMediator**: must know all concrete colleagues; the place where interaction rules live.
- **集中控制 (centralised control)**: both the pattern's advantage and its weakness.
- **Form / aspx as mediator**: the author's everyday example, controls never reference each other, the form's event handlers mediate.
- **迪米特法则 (Law of Demeter)**: the principle Mediator implements; two classes that need not talk directly should go through a third party ([ch11](ch11-law-of-demeter.md)).

## Mental Models
- Think of the mediator as the United Nations: countries (colleagues) do not negotiate bilaterally, they declare through the Security Council, and a new member does not force every other member to change.
- Use a mediator when you catch yourself writing code in `Button` that sets `TextBox.text`; that cross-control knowledge belongs in the form.
- Think of the mediator as a lens that raises your viewpoint from "what each object does" to "how the objects interact", the design shifts from individual behaviour to collaboration.
- Do not reach for Mediator the moment you see many-to-many chatter; first ask whether the design itself is wrong. The author warns it is as easy to misuse as to use.

## Anti-patterns
- **Colleagues referencing each other directly**: each new object forces edits in every peer; the system cannot be changed piecemeal.
- **God mediator**: piling every rule into `ConcreteMediator` until it is more complex than any colleague and a single point of failure ("if the Security Council fails, the whole world has a problem").
- **Premature mediator**: applying the pattern to a tangled object group instead of questioning why the group is tangled.

## Code Examples
The author's exercise: the USA and Iraq talk only through the UN Security Council.

```java
// Colleague
abstract class Country {
    protected UnitedNations unitedNations;
    public Country(UnitedNations unitedNations) { this.unitedNations = unitedNations; }
}
class USA extends Country {
    public USA(UnitedNations un) { super(un); }
    public void declare(String message) { this.unitedNations.declare(message, this); }
    public void getMessage(String message) { System.out.println("美国获得对方信息:" + message); }
}
class Iraq extends Country {
    public Iraq(UnitedNations un) { super(un); }
    public void declare(String message) { this.unitedNations.declare(message, this); }
    public void getMessage(String message) { System.out.println("伊拉克获得对方信息:" + message); }
}
// Mediator
abstract class UnitedNations {
    public abstract void declare(String message, Country country);
}
// ConcreteMediator: must know every concrete colleague
class UnitedNationsSecurityCouncil extends UnitedNations {
    private USA countryUSA;
    private Iraq countryIraq;
    public void setUSA(USA value) { this.countryUSA = value; }
    public void setIraq(Iraq value) { this.countryIraq = value; }
    public void declare(String message, Country country) {
        if (country == this.countryUSA) this.countryIraq.getMessage(message);
        else if (country == this.countryIraq) this.countryUSA.getMessage(message);
    }
}
// Client
UnitedNationsSecurityCouncil UNSC = new UnitedNationsSecurityCouncil();
USA c1 = new USA(UNSC);
Iraq c2 = new Iraq(UNSC);
UNSC.setUSA(c1);
UNSC.setIraq(c2);
c1.declare("不准研制核武器，否则要发动战争!");
c2.declare("我们没有核武器，也不怕侵略。");
```
- **What it demonstrates**: colleagues hold only a mediator reference; the routing decision (`if country == USA → notify Iraq`) lives in one place, and the generic template (`Colleague`/`ConcreteColleague1,2`/`Mediator`/`ConcreteMediator` with `send`/`notify`) is identical apart from names.

## Worked Example
1. **Naive picture**: the author draws nations as a mesh, each with bilateral ties. In code, every object needs a reference to every other; adding one object means touching all of them, and no object works without the rest.
2. **Apply Demeter**: 小菜 recalls the Law of Demeter from ch11. If two classes need not communicate directly, forward through a third party. The UN is that third party.
3. **Design question**: is 联合国 the `Mediator` or the `ConcreteMediator`? Answer depends on whether mediators will multiply. The UN has many organs (安理会, WHO, WTO...), so `UnitedNations` is abstract and `UnitedNationsSecurityCouncil` is concrete. If no extension is foreseeable, collapse them into one class.
4. **Result**: `USA` and `Iraq` never reference each other; adding a country changes only the mediator.
5. **The catch 小菜 spots**: `ConcreteMediator` has to know every colleague, so it accumulates responsibility. 大鸟 confirms: the pattern trades interaction complexity for mediator complexity. Good when the interaction is genuinely complex and well-defined (a Form with menus, text boxes, buttons), bad when used reflexively.

## Key Takeaways
1. Use Mediator when a group of objects interacts in complex but well-defined ways and you want to change that interaction independently of the objects.
2. Colleagues know the mediator and themselves, never each other; adding a colleague should only touch the mediator.
3. The mediator is where you look at the system from a macro angle: it models the collaboration, not the participants.
4. Expect `ConcreteMediator` to be the most complex class; if it is drowning in colleagues, the pattern's cost has exceeded its benefit.
5. Before applying Mediator to a many-to-many mess, reconsider the design; the pattern is easy to misuse.
6. You already use it: GUI forms and web pages mediating between their controls via events.

## Connects To
- **[ch11](ch11-law-of-demeter.md)**: Mediator is the structural realisation of 迪米特法则.
- **[ch12](ch12-facade.md)**: Facade also reduces coupling, but toward a subsystem from outside; Mediator coordinates peers from within (contrast drawn in [ch29](ch29-pattern-summary.md)).
- **[ch14](ch14-observer.md)**: the Form-as-mediator example runs on event notifications, an Observer mechanism.
- **[ch23](ch23-command.md)**: both decouple senders from receivers; Command reifies the request, Mediator centralises the routing.
