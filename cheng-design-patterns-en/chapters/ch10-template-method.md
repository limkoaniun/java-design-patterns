# Chapter 10: 考题抄错会做也白搭——模板方法模式 — Template Method

## Core Idea
When several subclasses share the same sequence of steps and differ only in a few details, lift the whole sequence into the parent as a template method and leave the differing steps abstract. The exam paper is printed once by the teacher; students only fill in answers.

## Frameworks Introduced
- **模板方法模式 (Template Method)** — “定义一个操作中的算法的骨架，而将一些步骤延迟到子类中。模板方法使得子类可以不改变一个算法的结构即可重定义该算法的某些特定步骤。”[DP]
  - Structure: `AbstractClass` (holds the concrete `templateMethod()` that gives the top-level skeleton and calls abstract `primitiveOperation1()`, `primitiveOperation2()`) → `ConcreteClass` (implements the primitive operations; any number of concrete classes per abstract class).
  - When to use: “当我们要完成在某一细节层次一致的一个过程或一系列步骤，但其个别步骤在更详细的层次上的实现可能不同时”. The process is the same at a high level but some steps differ per subclass.
  - How: (1) Write the shared process once in the superclass as a concrete method. (2) Extract every point where subclasses differ into an abstract (or overridable) method the template calls. (3) Subclasses override only those hooks. (4) Clients declare the variable as the superclass type so polymorphism dispatches to the right hook.
  - Why it works / failure mode: it moves the invariant behavior into one place, so a change to the process is made once. Failure mode: pushing too much into the template (hooks for everything) recreates the rigidity it was meant to remove; only hook the steps that actually vary.

## Key Concepts
- **算法骨架 (algorithm skeleton)**: the fixed ordering of steps, owned by the superclass.
- **templateMethod**: a concrete superclass method that calls the primitive operations in order; subclasses do not override it.
- **primitiveOperation (钩子步骤)**: an abstract method representing one variable step; each subclass supplies its own implementation.
- **不变行为搬移到超类**: the author's one-line summary of the pattern's value: move invariant behavior up, remove duplicate code from subclasses.
- **顶级逻辑**: the top-level logic; it may also call ordinary concrete methods, not only abstract ones.

## Mental Models
- Think of the template as the printed exam: identical question sheets for everyone, answers are the only blanks.
- Use Template Method when "the process is the same but a step's content varies" and you already have a meaningful inheritance relationship.
- Once you commit to inheritance, the parent should be the *template* for its children: any code repeated across children belongs in the parent.
- Java class libraries pull common behavior into abstract classes this way; you have probably used the pattern without naming it.

## Anti-patterns
- **Copy-paste sibling classes** (`TestPaperA`, `TestPaperB` each printing the full question text): 重复 = 易错 + 难改. If the teacher changes a question, both copies change, and one student will copy it wrong.
- **Half-lifted inheritance**: subclasses call `super.testQuestion1()` then print their answer. The shared line `System.out.println("答案：...")` still repeats; only the letter differs. Stop when the *only* thing left in the subclass is what genuinely varies.
- **Declaring the client variable as the subclass** (`TestPaperA studentA = new TestPaperA()`): you lose the polymorphic reuse; declare it as `TestPaper`.

## Code Examples
```java
// 金庸小说考题试卷 — the template
abstract class TestPaper {
    public void testQuestion1() {
        System.out.println("杨过得到，后来给了郭靖，炼成倚天剑、屠龙刀的玄铁可能是[ ] "
            + "a.球磨铸铁 b.马口铁 c.高速合金钢 d.碳素纤维");
        System.out.println("答案: " + this.answer1());
    }
    protected abstract String answer1();   // only this varies per student

    public void testQuestion2() { /* question text */ System.out.println("答案: " + this.answer2()); }
    protected abstract String answer2();

    public void testQuestion3() { /* question text */ System.out.println("答案: " + this.answer3()); }
    protected abstract String answer3();
}

class TestPaperA extends TestPaper {
    protected String answer1() { return "b"; }
    protected String answer2() { return "a"; }
    protected String answer3() { return "c"; }
}

class TestPaperB extends TestPaper {
    protected String answer1() { return "d"; }
    protected String answer2() { return "b"; }
    protected String answer3() { return "a"; }
}

// client: declare as the parent type
TestPaper studentA = new TestPaperA();
studentA.testQuestion1(); studentA.testQuestion2(); studentA.testQuestion3();
TestPaper studentB = new TestPaperB();
studentB.testQuestion1(); studentB.testQuestion2(); studentB.testQuestion3();
```
- **What it demonstrates**: each `testQuestionN()` is a template method; `answerN()` is the deferred primitive operation.

```java
// Generic structure
abstract class AbstractClass {
    public void templateMethod() {       // skeleton, shared by all subclasses
        this.primitiveOperation1();
        this.primitiveOperation2();
    }
    public abstract void primitiveOperation1();   // subclass-specific behavior
    public abstract void primitiveOperation2();
}
class ConcreteClassA extends AbstractClass {
    public void primitiveOperation1() { System.out.println("具体类A方法1实现"); }
    public void primitiveOperation2() { System.out.println("具体类A方法2实现"); }
}
```
- **What it demonstrates**: the canonical `AbstractClass` / `ConcreteClass` roles from the structure diagram.

## Worked Example
**Version 1 (抄试卷):** two unrelated classes `TestPaperA` and `TestPaperB`, each with `testQuestion1..3()` that print the full question text and then their answer. Everything except three letters is duplicated. A wrong copy of a question (大鸟's childhood "3 looks like 8") makes the whole answer worthless, and any question change must be made in every class.

**Version 2 (初步泛化):** extract a parent `TestPaper` holding the question text; `TestPaperA`/`B` extend it, and each override calls `super.testQuestion1()` then prints `"答案: b"`. Better, but the `super` call and the `"答案:"` print line still repeat in every subclass, and the client still declares subclass types.

**Version 3 (模板方法):** make `TestPaper` abstract; each `testQuestionN()` prints the question *and* `"答案: " + answerN()`, where `answerN()` is `protected abstract`. Subclasses shrink to three one-line `return "b";` methods. The client changes only its declared type to `TestPaper`, gaining polymorphic reuse. Adding a third student is one tiny class; changing a question is one edit in the parent.

Why it works: the invariant part (question + print format) now lives in exactly one place, and the compiler forces every student to fill in every answer.

## Key Takeaways
1. If two subclasses look alike except for a few lines, the shared lines belong in the parent, wrapped as a template method.
2. Keep abstracting until the subclass contains *only* what varies; a leftover `super.x()` call is a sign you stopped early.
3. Declare client variables as the abstract type so the template dispatches polymorphically.
4. Template Method is the most common way inheritance earns its keep; it is what class libraries do to share behavior.
5. The template step order is fixed by the parent; subclasses can change *what* a step does, never *whether* or *when* it runs.

## Connects To
- **[ch13](ch13-builder.md)**: Builder's `Director` also fixes a step sequence, but via composition of a builder object instead of inheritance hooks.
- **[ch08](ch08-factory-method.md)**: Factory Method is a template method whose deferred step is "which object to create".
- **[ch22](ch22-bridge.md)** / **合成/聚合复用原则**: when the varying behavior should be swappable at runtime, prefer Strategy ([ch02](ch02-strategy.md)) over subclass hooks.
- **[ch29](ch29-pattern-summary.md)**: behavioral pattern group one; the judges rank Template Method as the simplest reuse platform.
