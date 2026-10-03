# Chapter 15: 就不能不换DB吗？——抽象工厂模式 — Abstract Factory (and the reflection + config refinement)

## Core Idea
When a system must switch an entire *family* of related products at once (every data-access class for SQL Server vs. Access), give the client one abstract factory interface and let a concrete factory produce the whole family. Then use reflection plus a config file to remove the last hard-coded `new` so switching families needs no recompilation.

## Frameworks Introduced
- **抽象工厂模式 (Abstract Factory)** — “提供一个创建一系列相关或相互依赖对象的接口，而无须指定它们具体的类。”[DP]
  - Structure: `AbstractFactory` (`createProductA()`, `createProductB()`) ← `ConcreteFactory1`, `ConcreteFactory2`; `AbstractProductA` ← `ProductA1`, `ProductA2`; `AbstractProductB` ← `ProductB1`, `ProductB2`; `Client` uses only the abstract types.
  - When to use: two or more *dimensions* of variation — several product types (User, Department, Project…) × several product families (SQL Server, Access, Oracle…) — and the family must be swapped as a unit.
  - How: (1) one interface per product type (`IUser`, `IDepartment`); (2) one implementation per product × family; (3) `IFactory` declares one `createXxx()` per product; (4) one concrete factory per family; (5) the client instantiates a factory once at startup and touches only interfaces.
- **反射 + 抽象工厂 (Reflection + Abstract Factory)** — replace the concrete-factory classes and every `switch(db)` with `Class.forName(packageName + db + "User")`, so the family choice is a *string variable* resolved at run time rather than a compile-time class name.
  - How: `assemblyName + db + "User"` → `getInstance(className)` → cast to `IUser`.
- **反射 + 配置文件 (Reflection + properties file)** — read `db=Sqlserver` from `db.properties` so switching databases needs no code change at all, which the author calls the true fulfilment of 开放-封闭原则.
- **依赖注入 (Dependency Injection)** — named as the general idea behind this; the author says an IoC container like Spring does it properly, but plain reflection is enough here.

## Key Concepts
- **产品系列 (product family)**: all the concrete classes that belong to one variant (everything SQL-Server-flavoured).
- **产品等级 / product type**: one abstract product (`IUser`) with an implementation per family.
- **具体工厂只出现一次**: the concrete factory is named exactly once, at initialisation — that is why swapping a family is cheap.
- **编译时 → 运行时**: reflection moves the instantiation decision from compile time to run time because the class name is a string.
- **`Class.forName(...).getDeclaredConstructor().newInstance()`**: the author's canonical reflection idiom; the parameterised form passes `new Class[]{double.class,...}` and `new Object[]{a,b,c}`.
- **db.properties / data.properties**: external config files that hold the family name or the strategy table.
- **Abstract Factory 的缺点**: adding a new *product type* (Project) forces edits to `IFactory` and every concrete factory plus three new classes.

## Mental Models
- Think of the factory as a **catalogue for one supplier**: you pick the supplier (concrete factory) once, then order any product from the catalogue and it is guaranteed to be that supplier's.
- Use Factory Method when there is **one product with several implementations**; graduate to Abstract Factory the moment a **second product type** appears alongside the same set of families.
- Treat every `switch`/`if` that picks a class to instantiate as a **reflection candidate**: "所有在用简单工厂的地方，都可以考虑用反射技术来去除switch或if".
- Prefer configuration over recompilation: the design goal is "改动变得最小", and the best change is one made to a text file.

## Anti-patterns
- **Global find-and-replace between databases**: SQL dialects differ (`GetDate()` vs `Now()`, `Substring` vs `Mid`, reserved words like `password` needing `[ ]`), so the two copies diverge and every future feature is built twice.
- **`SqlserverUser su = new SqlserverUser()` in business code**: the client is welded to one family; polymorphism is impossible.
- **`IFactory factory = new SqlServerFactory()` in every client class**: with 100 callers, a switch means 100 edits — the pattern alone does not fix this.
- **Simple-factory `DataAccess` with `switch(db)`** (the 95-point version): adding Oracle means editing every `case` block, violating 开放-封闭.
- **Solving change with overtime**: "菜鸟程序员碰到问题，只会用时间来摆平" — the author's warning that patching two codebases by hand is the problem, not the solution.

## Code Examples
Abstract Factory (step 2 of the ladder):
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
- **What it demonstrates**: the client knows only `IUser`/`IDepartment`; swapping the whole family is a one-line change.

Reflection + config (final rung):
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
- **What it demonstrates**: no `switch`, no concrete factory classes, no recompilation to change database — add Oracle by adding `OracleUser`/`OracleDepartment` and editing one text line.

## Reference Tables
The chapter's evolution ladder for the data-access problem:

| Rung | Design | Switch DB costs | Add product type (Project) costs | Verdict |
|---|---|---|---|---|
| 15.2 | `new SqlserverUser()` in client | rewrite everything | edit client | coupled |
| 15.3 | 工厂方法: `IFactory` + `IUser` | change `new XxxFactory()` per client | n/a (one product) | solves one product |
| 15.4 | 抽象工厂: factory creates User + Department | change `new XxxFactory()` per client | 3 new classes + edit `IFactory` and every factory | family swap works, still N call sites |
| 15.7 | 简单工厂 `DataAccess` with `switch(db)` | change one `db` string | add a `createProject()` | "95分": adding Oracle edits every `switch` |
| 15.8 | 反射 + 抽象工厂 | change one `db` string, recompile | add classes + one `createProject()` | no switch; still recompiles |
| 15.9 | 反射 + `db.properties` | edit a text file | same as above | "满分": 开放-封闭 fully honoured |

## Worked Example
小菜 ships an e-commerce site on SQL Server; the next customer can only afford Access. He tries global replacement of the ADO.NET classes and drowns in SQL-dialect errors and reserved-word bugs, then faces double maintenance forever.

1. **Naive**: `SqlserverUser su = new SqlserverUser(); su.insert(user);` — the type name and the SQL inside it both bind the client to one database.
2. **Factory Method**: introduce `IUser` + `IFactory`; `SqlServerFactory`/`AccessFactory` each create one product. Switching is now `new AccessFactory()`. Fine for a single table.
3. **Abstract Factory**: a `Department` table arrives. `IFactory` grows `createDepartment()`; each concrete factory now builds the whole family. The client uses two interfaces and one factory. 大鸟: you have refactored your way into a named GoF pattern.
4. **Limits exposed**: adding `Project` touches `IFactory` and both factories; and 100 client classes each hold `new SqlServerFactory()`.
5. **Simple-factory rewrite**: drop the three factory classes for static `DataAccess.createUser()` with a `switch(db)`. Clients no longer name any database. 95/100 — Oracle still means editing every `switch`.
6. **Reflection**: `Class.forName(assemblyName + db + "User")` — the moment 小菜 sees the class name is a *string*, the switch disappears. Still needs a rebuild to change `db`.
7. **Config file**: `db=Sqlserver` in `db.properties`; `getDb()` reads it. No recompilation. Same trick then removes the six-case `switch` in the 商场收银 `CashContext`: `data.properties` holds `strategy1=CashRebateReturnFactory,1d,0d,0d` … and a parameterised `getInstance(className, a, b, c)` builds the `IFactory` via `getDeclaredConstructor(double.class, double.class, double.class)`.

Why it works: each rung moves one more decision out of compiled client code — first out of the client (interfaces), then out of the factory hierarchy (reflection), then out of the binary entirely (config).

## Key Takeaways
1. Reach for Abstract Factory when you have **families × product types**; a single product type only needs Factory Method.
2. The pattern's payoff is that the concrete factory is named **once**; its cost is that every new product type edits the factory interface and all factories.
3. Any `switch`/`if` that chooses which class to `new` can be replaced by `Class.forName(prefix + variable + suffix)`.
4. Push the variable into a properties file so a database swap is a config edit, not a build — that is the author's standard for 开放-封闭.
5. Reflection does not remove the need to *add* classes for Oracle; that is extension, which the principle permits. It removes *modification*.
6. Keep `getInstance` in one place and cast to the interface; clients must never see a concrete class name or a database name.

## Connects To
- **[ch08](ch08-factory-method.md)**: the single-product rung; Abstract Factory is Factory Method scaled to a family.
- **[ch01](ch01-simple-factory.md)**: the `DataAccess` simplification is Simple Factory; reflection then fixes Simple Factory's `switch` weakness.
- **[ch02](ch02-strategy.md)**, **[ch06](ch06-decorator.md)**: the 商场收银 program gets its final upgrade here — strategy selection moves into `data.properties`.
- **[ch04](ch04-open-closed.md)**, **[ch05](ch05-dependency-inversion.md)**: 小菜 calls this pattern those two principles "发挥到极致"; 大鸟 corrects: it is simply their good application.
- **Spring / IoC**: the author names Dependency Injection as the industrial form of the reflection trick.
