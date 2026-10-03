# 第19章：分公司=一部门——组合模式（Composite）

## 核心思想
当你的领域是由部分与整体构成的树（总公司 → 分公司 → 办事处 → 部门），并且希望客户端以同样的方式对待单个对象和一组对象时，让叶子和树枝共用一个 `Component` 接口，并让树枝递归地持有子节点。

## 引入的框架
- **组合模式（Composite）** — “将对象组合成树形结构以表示‘部分-整体’的层次结构。组合模式使得用户对单个对象和组合对象的使用具有一致性。”[DP]
  - 结构：`Component`（`add(Component)`、`remove(Component)`、`display(int depth)`）← `Leaf`（没有子节点）和 `Composite`（持有 `ArrayList<Component> children`，实现子节点管理，并在 `display` 中递归）。客户端只通过 `Component` 工作。
  - 适用时机："当你发现需求中是体现部分与整体层次的结构时，以及你希望用户可以忽略组合对象与单个对象的不同，统一地使用组合结构中的所有对象时".
  - 做法：(1) 找出部分-整体层次；(2) 在 `Component` 上声明公共操作；(3) `Leaf` 直接实现这些操作；(4) `Composite` 通过遍历子节点来实现这些操作（display 时用 `depth + 2`）；(5) 用 `add` 构建树，然后在根节点上调用一个方法。
- **透明方式（transparent）vs 安全方式（safe）** — `add`/`remove` 声明在哪里：声明在 `Component` 上（透明方式：接口统一，但叶子中的实现毫无意义），或只声明在 `Composite` 上（安全方式：没有无用方法，但客户端必须区分叶子和树枝）。作者拒绝给出默认选择："两者各有好处，视情况而定"。

## 关键概念
- **Component**："为组合中的对象声明接口，在适当情况下，实现所有类共有接口的默认行为。声明一个接口用于访问和管理Component的子部件".
- **Leaf**："在组合中表示叶节点对象，叶节点没有子节点".
- **Composite**："定义有枝节点行为，用来存储子部件，在Component接口中实现与子部件有关的操作，比如增加add和删除remove".
- **部分-整体（part–whole）**：销售一个零件与销售整台 PC、复制一个文件与复制一个文件夹、格式化一个字符与格式化一个段落——"其本质都是同样的问题"。
- **递归组合（recursive composition）**：`Composite` 可以包含 `Composite`，因此任意深度的树都只需要同样的两个类。
- **一致对待（uniform treatment）**：客户端在根节点上调用 `display`/`lineOfDuty`，从不检查节点类型。
- **java.awt.Container extends Component**：作者给出的内置示例——容器本身就是带有 `add`/`remove` 的组件。

## 心智模型
- 把树看作**每一层都是同一种形状**：树枝就是「拥有组件的组件」。
- 当你发现自己在调用同一个操作之前先写 `if (isHeadOffice) … else if (isBranch) …` 时，就该使用组合模式。
- 希望客户端无需关心时，选择透明方式；当叶子的 `add()` 会成为一个必须写文档说明的谎言时，选择安全方式。
- 村级农户之下的部门仍然只是叶子——该模式不限制深度，只规定形状。

## 反模式
- **为每个分公司复制总公司的代码**："简单复制是最糟糕的设计"——各分公司的代码会逐渐分叉，树形结构也随之丢失。
- **按 ID 区分的扁平共享**：用一份代码按 ID 区分总部/分公司/办事处，会迫使每次操作前都做类型检查，也无法表达层次结构。
- **叶子方法默默什么都不做且没有说明**：只有在你清楚原因时，透明方式下才可接受（`Leaf.add` 输出「Cannot add to a leaf.」可以让约定一目了然）。
- **带有既定偏好**（"我喜欢透明式"）而不权衡安全方式——大鸟："开发怎么能随便有倾向性？"

## 代码示例
通用结构（透明方式）：
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
- **演示内容**：在根节点上调用一次 `display(1)` 就能遍历整棵树；深度通过递归逐层传递。

公司管理系统：
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
- **演示内容**：加入组件接口的领域操作（`lineOfDuty`）会在整棵树中传播，客户端无需任何类型检查。

## 参考表
| | 透明方式 | 安全方式 |
|---|---|---|
| `add`/`remove` 放在哪里 | 声明在 `Component` 上，因此 `Leaf` 必须实现它们 | 只声明在 `Composite` 上 |
| 客户端视角 | 叶子和树枝的接口完全相同；无需类型检查 | 客户端必须知道自己持有的是叶子还是树枝 |
| 代价 | `Leaf.add()`/`remove()` 是无意义的空实现 | 客户端代码中多出一层判断 |
| 何时选用 | 统一性比少数几个无用方法更重要 | 你拒绝实现空操作方法 |

## 实战示例
小菜的 OA 系统是为总公司（人力资源、财务、运营）开发的。现在客户想把它用于全国范围的树：北京总公司 → 上海华东分公司 → 南京办事处 / 杭州办事处，每一层都需要同样的人力资源和财务功能。

1. **最初的想法**：共用一份代码，按 ID 区分节点。行不通，因为组织是一棵树；每个操作都得做「这是总部还是分公司？」的检查。
2. **重新定位**：总部是根，分公司是大树枝，办事处是小树枝，部门是叶子。部分-整体，与文件/文件夹、字符/段落是同一回事。
3. **应用组合模式**：抽象类 `Company` 带有 `add`、`remove`、`display(depth)`、`lineOfDuty()`。`ConcreteCompany` 是树枝（持有 `children`，并递归）。`HRDepartment` 和 `FinanceDepartment` 是叶子（`add`/`remove` 为空，`lineOfDuty` 输出各自的职责）。
4. **构建并运行**：用 `add` 组装这棵树，然后 `root.display(1)` 以短横线缩进输出组织结构图，`root.lineOfDuty()` 让每一层的每个部门都履行职责——无需任何按层级编写的代码。
5. **结果**："那家公司开多少个以及多少级办事处都没问题了"——任意的广度和深度，无需额外付出。

为什么有效：`ConcreteCompany.lineOfDuty()` 只是转发给它的子节点，而子节点都是 `Company`——无论叶子还是树枝——所以递归可以处理任何形状。

## 关键要点
1. 当需求是部分-整体层次，且客户端希望忽略单个与多个之间的差别时，就用组合模式。
2. 把客户端会在树上调用的每个操作——`display`、`lineOfDuty`——都放到 `Component` 上；树枝通过递归来实现它。
3. 每个项目都要明确决定采用透明方式还是安全方式；作者没有给出默认选择。
4. 把 `depth`（或任何累加器）通过递归调用传递下去，而不是存放在节点上。
5. 在类库中识别这个模式：`java.awt.Container` 继承 `Component` 并增加了 `add`/`remove`。
6. 组合模式消除了每个调用点上区分树枝与叶子的 `if`——这就是值得度量的可维护性收益。

## 关联章节
- **[ch06](ch06-decorator.md)**：两者都使用带有公共接口的递归对象结构；装饰模式（Decorator）增加职责，组合模式增加子节点。
- **[ch20](ch20-iterator.md)**：遍历组合结构是迭代器模式（Iterator）的工作；`for (Component item : children)` 是其内置形式。
- **[ch28](ch28-visitor.md)**：访问者模式（Visitor）在不修改节点类的前提下，对组合结构执行操作。
- **[ch11](ch11-law-of-demeter.md)**：客户端只与根节点对话；它从不深入到孙子节点。
- **[ch29](ch29-pattern-summary.md)**：组合模式在结构型分组中参与比较。
