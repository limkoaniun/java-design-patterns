# 第15章：就不能不换DB吗？——抽象工厂模式（Abstract Factory (and the reflection + config refinement)）

## 核心思想
当系统需要一次性切换整个相关产品*系列*时（例如 SQL Server 与 Access 的全部数据访问类），给客户端一个抽象工厂接口，由具体工厂生产整个产品系列。然后用反射加配置文件去掉最后一处硬编码的 `new`，这样切换产品系列就无需重新编译。

## 引入的框架
- **抽象工厂模式（Abstract Factory）** — “提供一个创建一系列相关或相互依赖对象的接口，而无须指定它们具体的类。”[DP]
  - 结构：`AbstractFactory`（`createProductA()`、`createProductB()`）← `ConcreteFactory1`、`ConcreteFactory2`；`AbstractProductA` ← `ProductA1`、`ProductA2`；`AbstractProductB` ← `ProductB1`、`ProductB2`；`Client` 只使用抽象类型。
  - 适用场景：存在两个或更多变化*维度*——多种产品类型（User、Department、Project……）× 多种产品系列（SQL Server、Access、Oracle……）——并且产品系列必须作为一个整体切换。
  - 做法：(1) 每种产品类型一个接口（`IUser`、`IDepartment`）；(2) 每个产品 × 系列组合一个实现；(3) `IFactory` 为每个产品声明一个 `createXxx()`；(4) 每个系列一个具体工厂；(5) 客户端在启动时实例化一次工厂，之后只接触接口。
- **反射 + 抽象工厂（Reflection + Abstract Factory）** — 用 `Class.forName(packageName + db + "User")` 取代具体工厂类和每一处 `switch(db)`，这样产品系列的选择就成了在运行时解析的*字符串变量*，而不是编译期的类名。
  - 做法：`assemblyName + db + "User"` → `getInstance(className)` → 强制转换为 `IUser`。
- **反射 + 配置文件（Reflection + properties file）** — 从 `db.properties` 读取 `db=Sqlserver`，这样切换数据库完全不需要改代码，作者称之为对开放-封闭原则的真正落实。
- **依赖注入（Dependency Injection）** — 被指为这背后的通用思想；作者说像 Spring 这样的 IoC 容器能把它做得更规范，但这里只用反射就够了。

## 关键概念
- **产品系列（product family）**：属于同一变体的所有具体类（所有 SQL Server 风格的类）。
- **产品等级 / product type**：一个抽象产品（`IUser`），每个系列各有一个实现。
- **具体工厂只出现一次**：具体工厂只在初始化时被命名一次——这正是切换产品系列代价很小的原因。
- **编译时 → 运行时**：因为类名是字符串，反射把实例化的决定从编译时移到了运行时。
- **`Class.forName(...).getDeclaredConstructor().newInstance()`**：作者的标准反射写法；带参数的形式传入 `new Class[]{double.class,...}` 和 `new Object[]{a,b,c}`。
- **db.properties / data.properties**：保存产品系列名称或策略表的外部配置文件。
- **抽象工厂模式的缺点**：新增一种*产品类型*（Project）会迫使修改 `IFactory` 和每一个具体工厂，外加三个新类。

## 心智模型
- 把工厂想成**某一家供应商的目录**：你只选一次供应商（具体工厂），之后从目录里订任何产品，都保证是这家供应商的。
- 当**一个产品有多种实现**时用工厂方法模式；一旦在同一组系列旁边出现**第二种产品类型**，就升级为抽象工厂模式。
- 把每一处挑选要实例化哪个类的 `switch`/`if` 都当作**反射的候选对象**："所有在用简单工厂的地方，都可以考虑用反射技术来去除switch或if"。
- 优先用配置而不是重新编译：设计目标是"改动变得最小"，而最好的改动就是改一个文本文件。

## 反模式
- **在数据库之间全局查找替换**：SQL 方言各不相同（`GetDate()` 与 `Now()`、`Substring` 与 `Mid`、像 `password` 这样需要加 `[ ]` 的保留字），于是两份代码渐行渐远，今后每个功能都要做两遍。
- **业务代码中的 `SqlserverUser su = new SqlserverUser()`**：客户端被焊死在一个产品系列上，无法使用多态。
- **每个客户端类里都写 `IFactory factory = new SqlServerFactory()`**：有 100 个调用方，切换一次就要改 100 处——光靠这个模式解决不了这一点。
- **带有 `switch(db)` 的简单工厂模式 `DataAccess`**（95 分版本）：新增 Oracle 意味着要修改每一个 `case` 块，违反开放-封闭。
- **用加班解决变化**："菜鸟程序员碰到问题，只会用时间来摆平"——作者警告说，手工修补两套代码库本身就是问题，而不是解决办法。

## 代码示例
抽象工厂（演进阶梯第 2 步）：
```java
public interface IUser { void insert(User user); User getUser(int id); }
public interface IDepartment { void insert(Department d); Department getDepartment(int id); }

public class SqlserverUser implements IUser {
    public void insert(User user) { System.out.println("在SQL Server中给User表增加一条记录"); }
    public User getUser(int id)  { System.out.println("在SQL Server中根据用户ID得到User表一条记录"); return null; }
}
// AccessUser, SqlserverDepartment, AccessDepartment: same shape

public interface IFactory { IUser createUser(); IDepartment createDepartment(); }

public class SqlserverFactory implements IFactory {
    public IUser createUser()             { return new SqlserverUser(); }
    public IDepartment createDepartment() { return new SqlserverDepartment(); }
}
public class AccessFactory implements IFactory { /* returns Access* products */ }

// client — the concrete factory appears exactly once
IFactory factory = new SqlserverFactory();   // or new AccessFactory()
IUser iu = factory.createUser();
iu.insert(user); iu.getUser(1);
IDepartment idept = factory.createDepartment();
idept.insert(department); idept.getDepartment(2);
```
- **演示了什么**：客户端只认识 `IUser`/`IDepartment`；切换整个产品系列只需改一行。

反射 + 配置（最后一级）：
```java
import java.util.Properties; import java.io.*;
public class DataAccess {
    private static String assemblyName = "code.chapter15.abstractfactory6.";
    private static String db = getDb();   // read from db.properties: db=Sqlserver

    public static String getDb() {
        String result = "";
        try (BufferedReader r = new BufferedReader(new FileReader(
                System.getProperty("user.dir") + "/code/chapter15/abstractfactory6/db.properties"))) {
            Properties p = new Properties(); p.load(r); result = p.getProperty("db");
        } catch (IOException e) { e.printStackTrace(); }
        return result;
    }
    public static IUser createUser()             { return (IUser) getInstance(assemblyName + db + "User"); }
    public static IDepartment createDepartment() { return (IDepartment) getInstance(assemblyName + db + "Department"); }

    private static Object getInstance(String className) {
        try { return Class.forName(className).getDeclaredConstructor().newInstance(); }
        catch (ReflectiveOperationException e) { e.printStackTrace(); return null; }
    }
}
```
- **演示了什么**：没有 `switch`，没有具体工厂类，更换数据库也无需重新编译——新增 Oracle 只需添加 `OracleUser`/`OracleDepartment` 并修改文本中的一行。

## 参考表
本章针对数据访问问题的演进阶梯：

| 阶梯 | 设计 | 切换数据库的代价 | 新增产品类型（Project）的代价 | 结论 |
|---|---|---|---|---|
| 15.2 | 客户端中的 `new SqlserverUser()` | 全部重写 | 修改客户端 | 紧耦合 |
| 15.3 | 工厂方法: `IFactory` + `IUser` | 每个客户端都要修改 `new XxxFactory()` | 不适用（只有一个产品） | 只解决一个产品 |
| 15.4 | 抽象工厂: 工厂创建 User + Department | 每个客户端都要修改 `new XxxFactory()` | 3 个新类 + 修改 `IFactory` 和每个工厂 | 系列切换可行，但仍有 N 处调用点 |
| 15.7 | 带 `switch(db)` 的简单工厂 `DataAccess` | 修改一个 `db` 字符串 | 新增一个 `createProject()` | "95分"：新增 Oracle 要修改每个 `switch` |
| 15.8 | 反射 + 抽象工厂 | 修改一个 `db` 字符串，重新编译 | 新增类 + 一个 `createProject()` | 没有 switch；仍需重新编译 |
| 15.9 | 反射 + `db.properties` | 编辑一个文本文件 | 同上 | "满分"：开放-封闭得到充分遵守 |

## 实战示例
小菜把一个电商网站部署在 SQL Server 上；下一个客户只买得起 Access。他尝试全局替换 ADO.NET 的类，结果淹没在 SQL 方言错误和保留字 bug 里，之后还要永远面对双份维护。

1. **朴素做法**：`SqlserverUser su = new SqlserverUser(); su.insert(user);`——类型名和其中的 SQL 都把客户端绑定在一个数据库上。
2. **工厂方法**：引入 `IUser` + `IFactory`；`SqlServerFactory`/`AccessFactory` 各创建一个产品。现在切换只需 `new AccessFactory()`。对单张表来说够用了。
3. **抽象工厂**：出现了 `Department` 表。`IFactory` 增加 `createDepartment()`；每个具体工厂现在构建整个产品系列。客户端使用两个接口和一个工厂。大鸟：你一路重构，走进了一个有名字的 GoF 模式。
4. **暴露的局限**：新增 `Project` 要修改 `IFactory` 和两个工厂；而且 100 个客户端类各自都持有 `new SqlServerFactory()`。
5. **简单工厂式重写**：去掉三个工厂类，改用带 `switch(db)` 的静态 `DataAccess.createUser()`。客户端不再指名任何数据库。95/100——新增 Oracle 仍然意味着要修改每个 `switch`。
6. **反射**：`Class.forName(assemblyName + db + "User")`——小菜一看到类名是*字符串*，switch 就消失了。更改 `db` 仍然需要重新构建。
7. **配置文件**：`db.properties` 中写 `db=Sqlserver`；`getDb()` 读取它。无需重新编译。同样的招数随后去掉了商场收银 `CashContext` 里六个 case 的 `switch`：`data.properties` 保存 `strategy1=CashRebateReturnFactory,1d,0d,0d` ……，带参数的 `getInstance(className, a, b, c)` 通过 `getDeclaredConstructor(double.class, double.class, double.class)` 构建 `IFactory`。

为什么有效：每一级都把又一个决定移出已编译的客户端代码——先移出客户端（接口），再移出工厂层次结构（反射），最后彻底移出二进制文件（配置）。

## 关键要点
1. 当存在**系列 × 产品类型**时才用抽象工厂模式；只有单一产品类型时，工厂方法模式就够了。
2. 这个模式的收益是具体工厂只被命名**一次**；代价是每新增一种产品类型，都要修改工厂接口和所有工厂。
3. 任何选择要 `new` 哪个类的 `switch`/`if`，都可以替换成 `Class.forName(prefix + variable + suffix)`。
4. 把变量推到 properties 文件里，换数据库就只是改配置而不是重新构建——这就是作者对开放-封闭的标准。
5. 反射并不能免去为 Oracle *新增*类的需要；那属于扩展，是该原则所允许的。它消除的是*修改*。
6. 把 `getInstance` 放在一处并强制转换为接口；客户端绝不能看到具体类名或数据库名。

## 关联章节
- **[ch08](ch08-factory-method.md)**：单一产品这一级；抽象工厂模式就是扩展到一个系列的工厂方法模式。
- **[ch01](ch01-simple-factory.md)**：`DataAccess` 的简化就是简单工厂模式；随后反射修补了简单工厂模式的 `switch` 弱点。
- **[ch02](ch02-strategy.md)**、**[ch06](ch06-decorator.md)**：商场收银程序在这里得到最终升级——策略的选择移入了 `data.properties`。
- **[ch04](ch04-open-closed.md)**、**[ch05](ch05-dependency-inversion.md)**：小菜称这个模式把这两条原则"发挥到极致"；大鸟纠正：它只是对这两条原则的良好应用。
- **Spring / IoC**：作者把依赖注入称为反射这一招的工业化形式。
