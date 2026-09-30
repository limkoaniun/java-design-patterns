# Cheatsheet — 大话设计模式 (the author's judgment on one page)

## Decision rules
- **Change is the trigger, not the plan.** Do not abstract on day one; when a *second* variation arrives, abstract exactly that axis (OCP: "拒绝不成熟的抽象"). Start with the simplest design; the 商场收银 program grew through five patterns one requirement at a time.
- **Ask "what varies?" before "which pattern?"** Algorithm → 策略. Concrete class → 工厂方法/抽象工厂. Extra behaviour → 装饰. Interface mismatch → 适配器. State-dependent behaviour → 状态. Two axes → 桥接. Operations on a fixed structure → 访问者.
- **Default creation path: 工厂方法.** Move to 抽象工厂 only for product *families*; collapse factory explosion with 简单工厂 + 反射 + 配置文件.
- **Inheritance leaks; composition contains.** If a subclass must know parent internals or the class count multiplies under two changes, switch to object composition (CARP).
- **Keep the user's business rules out of the UI and out of `main`.** Every book example first fails by mixing display, calculation, and control (SRP).
- **Never let the sender know the receiver** when the receiver set may change: 观察者 (many receivers), 命令 (queue/undo), 职责链 (who handles decided at runtime), 中介者 (peer web).
- **Use the library when the pattern is already there**: `java.util.Iterator`, `Cloneable`. Learn the structure, don't reimplement. (Exception: `java.util.Observable` is deprecated; write your own `Subject` interface.)

## Similar patterns — pick by intent
| Confusable pair | Same shape, different intent |
|---|---|
| 策略 vs 状态 | Client picks the strategy; state object switches itself and knows its successor |
| 装饰 vs 代理 vs 适配器 | Decorator adds behaviour (same interface); Proxy controls access (same interface, one real subject); Adapter converts interface |
| 桥接 vs 装饰 | Bridge separates two dimensions up-front; Decorator stacks behaviours on one |
| 外观 vs 中介者 | Facade is a one-way simplifier over a subsystem; Mediator coordinates two-way peer traffic |
| 简单工厂 vs 工厂方法 vs 抽象工厂 | One `switch`; one factory per product; one factory per product *family* |
| 模板方法 vs 策略 | Template varies steps via inheritance; Strategy swaps the whole algorithm via composition |
| 命令 vs 职责链 | Command packages one request for one receiver; Chain passes a request until someone accepts |
| 组合 vs 装饰 | Both recursive-wrapping; Composite models trees, Decorator models layered behaviour |
| 建造者 vs 抽象工厂 | Builder returns one product after ordered steps; Abstract Factory returns a family immediately |
| 访问者 vs 解释器 | Visitor: fixed elements, growing operations; Interpreter: a grammar of expressions |

## Smells → pattern
| Tell | Likely fix |
|---|---|
| `switch`/`if` on a type or state field repeated in several methods | 状态 (state field) or 策略/工厂 (type field) |
| Every new product edits an existing factory class | 简单工厂 → 工厂方法 |
| Subclass count = brands × features | 桥接 |
| Subclass per combination of add-ons | 装饰 |
| Class knows a stranger's stranger (`a.getB().getC().do()`) | 迪米特: introduce a mediator/facade |
| One method over a screen long ("方法过长是坏味道") | 提炼 into 模板方法 or 状态 |
| Copy-pasted code with small diffs ("重复=易错+难改") | 模板方法 |
| Object needs to be reset to an earlier state | 备忘录 |
| Many identical heavy objects | 享元 (split 内/外部状态) |
| Duplicate construction steps, sometimes one forgotten | 建造者 with Director |
| Two modules both change when a DB/vendor changes | 依赖倒转 + 抽象工厂 |

## Thresholds & defaults the author commits to
- Class diagrams first: draw UML before coding once more than ~3 classes interact (ch01).
- Singleton in Java: prefer 静态初始化; if lazy, use 双重锁定 with `volatile`, never a bare null check.
- 原型: whenever a field is a reference type, decide 深复制 vs 浅复制 explicitly.
- 组合: default to 透明方式 unless leaf misuse is a real risk.
- 抽象工厂 with reflection: keep the DB/vendor name in a config file, not in code.
- 观察者: make the observer an interface, not an abstract class, so unrelated classes can subscribe; type subjects as an interface, never as the concrete `Boss`.

## The book's growth ladder (use as a "how far to go" gauge)
1. Working procedural code → 2. 封装 into classes (业务逻辑 vs 界面) → 3. 简单工厂 → 4. 策略 → 5. 装饰 for combinable rules → 6. 工厂方法 → 7. 抽象工厂 + 反射 + 配置. Stop at the rung that absorbs the change you actually have.
