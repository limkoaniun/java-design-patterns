# Chapter 19: 分公司=一部门——组合模式 — Composite

## Core Idea
When your domain is a tree of parts and wholes (head office → branches → offices → departments) and you want clients to treat a single object and a group of objects the same way, give leaves and branches one common `Component` interface and let branches hold children recursively.

## Frameworks Introduced
- **组合模式 (Composite)** — “将对象组合成树形结构以表示‘部分-整体’的层次结构。组合模式使得用户对单个对象和组合对象的使用具有一致性。”[DP]
  - Structure: `Component` (`add(Component)`, `remove(Component)`, `display(int depth)`) ← `Leaf` (no children) and `Composite` (holds `ArrayList<Component> children`, implements child management and recurses in `display`). Client works only through `Component`.
  - When to use: "当你发现需求中是体现部分与整体层次的结构时，以及你希望用户可以忽略组合对象与单个对象的不同，统一地使用组合结构中的所有对象时".
  - How: (1) find the part–whole hierarchy; (2) declare the common operations on `Component`; (3) `Leaf` implements the operations directly; (4) `Composite` implements them by iterating children (`depth + 2` for display); (5) build the tree with `add`, then call one method on the root.
- **透明方式 (transparent) vs 安全方式 (safe)** — where to declare `add`/`remove`: on `Component` (transparent: uniform interface, but leaf implementations are meaningless) or only on `Composite` (safe: no useless methods, but clients must distinguish leaf from branch). The author refuses to pick a default: "两者各有好处，视情况而定".

## Key Concepts
- **Component**: "为组合中的对象声明接口，在适当情况下，实现所有类共有接口的默认行为。声明一个接口用于访问和管理Component的子部件".
- **Leaf**: "在组合中表示叶节点对象，叶节点没有子节点".
- **Composite**: "定义有枝节点行为，用来存储子部件，在Component接口中实现与子部件有关的操作，比如增加add和删除remove".
- **部分-整体 (part–whole)**: selling a component vs. a whole PC, copying a file vs. a folder, formatting a character vs. a paragraph — "其本质都是同样的问题".
- **递归组合 (recursive composition)**: a Composite may contain Composites, so any depth of tree needs only the same two classes.
- **一致对待 (uniform treatment)**: the client calls `display`/`lineOfDuty` on the root and never checks node type.
- **java.awt.Container extends Component**: the author's built-in example — a container is itself a component with `add`/`remove`.

## Mental Models
- Think of the tree as **the same shape at every level**: a branch is "a component that has components".
- Use Composite when you catch yourself writing `if (isHeadOffice) … else if (isBranch) …` before calling the same operation.
- Choose transparent when clients should be oblivious; choose safe when leaf `add()` would be a lie you must document.
- A department under a village household is still just a leaf — the pattern imposes no depth limit, only a shape.

## Anti-patterns
- **Copy the head-office code per branch**: "简单复制是最糟糕的设计" — the branches diverge and the tree structure is lost.
- **Flat sharing keyed by ID**: one code base distinguishing 总部/分公司/办事处 by ID forces type checks before every operation and cannot express the hierarchy.
- **Leaf methods that silently do nothing without explanation**: acceptable in transparent mode only if you know why (`Leaf.add` printing "Cannot add to a leaf." makes the contract visible).
- **Having a stated preference** ("我喜欢透明式") without weighing the safe form — 大鸟: "开发怎么能随便有倾向性？"

## Code Examples
Generic structure (transparent mode):
```java
abstract class Component {
    protected String name;
    public Component(String name) { this.name = name; }
    public abstract void add(Component component);
    public abstract void remove(Component component);
    public abstract void display(int depth);
}
class Leaf extends Component {
    public Leaf(String name) { super(name); }
    public void add(Component c)    { System.out.println("Cannot add to a leaf."); }
    public void remove(Component c) { System.out.println("Cannot remove from a leaf."); }
    public void display(int depth)  { for (int i = 0; i < depth; i++) System.out.print("-"); System.out.println(name); }
}
class Composite extends Component {
    private ArrayList<Component> children = new ArrayList<>();
    public Composite(String name) { super(name); }
    public void add(Component c)    { children.add(c); }
    public void remove(Component c) { children.remove(c); }
    public void display(int depth) {
        for (int i = 0; i < depth; i++) System.out.print("-");
        System.out.println(name);
        for (Component item : children) item.display(depth + 2);   // recurse
    }
}

Composite root = new Composite("root");
root.add(new Leaf("Leaf A")); root.add(new Leaf("Leaf B"));
Composite comp = new Composite("Composite X");
comp.add(new Leaf("Leaf XA")); comp.add(new Leaf("Leaf XB"));
root.add(comp);
Composite comp2 = new Composite("Composite XY");
comp2.add(new Leaf("Leaf XYA")); comp2.add(new Leaf("Leaf XYB"));
comp.add(comp2);
Leaf leaf2 = new Leaf("Leaf D"); root.add(leaf2); root.remove(leaf2);   // "被风吹走了"
root.display(1);
```
- **What it demonstrates**: one `display(1)` on the root walks the whole tree; depth is threaded through recursion.

Company management system:
```java
abstract class Company {
    protected String name;
    public Company(String name) { this.name = name; }
    public abstract void add(Company company);
    public abstract void remove(Company company);
    public abstract void display(int depth);
    public abstract void lineOfDuty();          // 履行职责
}
class ConcreteCompany extends Company {          // 树枝节点
    protected ArrayList<Company> children = new ArrayList<>();
    public ConcreteCompany(String name) { super(name); }
    public void add(Company c)    { children.add(c); }
    public void remove(Company c) { children.remove(c); }
    public void display(int depth) { /* print dashes + name, then children.display(depth+2) */ }
    public void lineOfDuty() { for (Company item : children) item.lineOfDuty(); }
}
class HRDepartment extends Company {             // 树叶节点
    public HRDepartment(String name) { super(name); }
    public void add(Company c) {}  public void remove(Company c) {}
    public void display(int depth) { /* dashes + name */ }
    public void lineOfDuty() { System.out.println(name + " 员工招聘培训管理"); }
}
class FinanceDepartment extends Company { /* same; lineOfDuty prints "公司财务收支管理" */ }

ConcreteCompany root = new ConcreteCompany("北京总公司");
root.add(new HRDepartment("总公司人力资源部")); root.add(new FinanceDepartment("总公司财务部"));
ConcreteCompany comp = new ConcreteCompany("上海华东分公司");
comp.add(new HRDepartment("华东分公司人力资源部")); comp.add(new FinanceDepartment("华东分公司财务部"));
root.add(comp);
ConcreteCompany comp2 = new ConcreteCompany("南京办事处"); /* + HR, Finance */ comp.add(comp2);
ConcreteCompany comp3 = new ConcreteCompany("杭州办事处"); /* + HR, Finance */ comp.add(comp3);
root.display(1);
root.lineOfDuty();     // every department at every level performs its duty
```
- **What it demonstrates**: a domain operation (`lineOfDuty`) added to the component interface propagates through the tree with no client-side type checks.

## Reference Tables
| | 透明方式 (transparent) | 安全方式 (safe) |
|---|---|---|
| Where `add`/`remove` live | declared on `Component`, so `Leaf` must implement them | declared only on `Composite` |
| Client view | leaf and branch have identical interfaces; no type checks | client must know whether it holds a leaf or a branch |
| Cost | `Leaf.add()`/`remove()` are meaningless stubs | extra judgement in client code |
| Pick when | uniformity matters more than a few dead methods | you refuse to implement no-op methods |

## Worked Example
小菜's OA system was built for a head office (HR, finance, operations). The customer now wants it for a national tree: 北京总公司 → 上海华东分公司 → 南京办事处 / 杭州办事处, each level needing the same HR and finance functions.

1. **First idea**: share one code base and distinguish nodes by ID. Fails because the organisation is a tree; every operation would need "is this HQ or a branch?" checks.
2. **Reframe**: HQ is the root, branches are boughs, offices are smaller boughs, departments are leaves. Part–whole, same as files/folders or characters/paragraphs.
3. **Apply Composite**: `Company` abstract with `add`, `remove`, `display(depth)`, `lineOfDuty()`. `ConcreteCompany` is the branch (holds `children`, recurses). `HRDepartment` and `FinanceDepartment` are leaves (`add`/`remove` empty, `lineOfDuty` prints their duty).
4. **Build and run**: assemble the tree with `add`, then `root.display(1)` prints the org chart with dash-indentation, and `root.lineOfDuty()` makes every department at every level report — with no per-level code.
5. **Result**: "那家公司开多少个以及多少级办事处都没问题了" — arbitrary breadth and depth for free.

Why it works: `ConcreteCompany.lineOfDuty()` just forwards to its children, and children are `Company` — leaf or branch — so recursion handles any shape.

## Key Takeaways
1. Reach for Composite when the requirement is a part–whole hierarchy and the client wants to ignore the difference between one and many.
2. Put every operation the client will call on the tree — `display`, `lineOfDuty` — onto `Component`; branches implement it by recursion.
3. Decide transparent vs. safe explicitly per project; the author gives no default.
4. Thread `depth` (or any accumulator) through the recursive call rather than storing it on nodes.
5. Recognise the pattern in libraries: `java.awt.Container` extends `Component` and adds `add`/`remove`.
6. Composite eliminates the branch-vs-leaf `if` at every call site — that is the maintenance win to measure.

## Connects To
- **[ch06](ch06-decorator.md)**: both use recursive object structures with a common interface; Decorator adds responsibilities, Composite adds children.
- **[ch20](ch20-iterator.md)**: traversing a composite is Iterator's job; `for (Component item : children)` is the built-in form.
- **[ch28](ch28-visitor.md)**: Visitor performs operations over a Composite structure without editing the node classes.
- **[ch11](ch11-law-of-demeter.md)**: the client talks only to the root; it never reaches into grandchildren.
- **[ch29](ch29-pattern-summary.md)**: Composite competes in the structural group.
