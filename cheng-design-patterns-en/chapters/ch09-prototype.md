# Chapter 9: 简历复印——原型模式 — Prototype

## Core Idea
When you need many objects that are mostly alike, create one, then clone it and tweak the copies instead of running the constructor again and again. The story: printing twenty résumés by copying one, not hand-writing each. The trap the chapter is really about: Java's default `clone()` is shallow, so referenced objects are shared unless you clone them too.

## Frameworks Introduced
- **原型模式 (Prototype)** — “用原型实例指定创建对象的种类，并且通过复制这些原型创建新的对象。”[DP]
  - Structure: `Prototype { +clone() }` (declares the self-cloning interface); `ConcretePrototype1/2 { +clone() }` (implement cloning themselves). In Java the abstract `Prototype` is unnecessary: implement `Cloneable` and override `clone()`.
  - When to use: object initialisation is costly or the initial state is stable and you need several near-identical instances; you want to capture an object's runtime state and reproduce it ("不用重新初始化对象，而是动态地获得对象运行时的状态").
  - How: (1) `class X implements Cloneable`; (2) override `public X clone()` that calls `super.clone()` inside a `try/catch(CloneNotSupportedException)`; (3) if `X` holds reference-typed fields that must be independent, clone those too inside `clone()` (deep copy); (4) clients call `x.clone()` then adjust the copy.
  - Why it works: `super.clone()` bypasses the constructor and copies fields bitwise, so repeated creation avoids re-running expensive initialisation. Failure mode: shallow copy shares referenced objects, so editing one copy silently edits all.
- **浅复制 (shallow copy)**: "被复制对象的所有变量都含有与原来的对象相同的值，而所有的对其他对象的引用都仍然指向原来的对象。" What `super.clone()` gives you.
- **深复制 (deep copy)**: "把引用对象的变量指向复制过的新对象，而不是原有的被引用的对象." You implement it by cloning each referenced object inside `clone()`. Decide the depth up front and watch for circular references.

## Key Concepts
- **Cloneable**: Java's marker interface; without it `super.clone()` throws `CloneNotSupportedException`.
- **super.clone()**: copies value-type fields bit for bit and copies references without copying the referenced objects.
- **传引用 vs 传值**: `resume2 = resume1` creates a second name for the same object, not a second résumé; the chapter's first wrong shortcut.
- **String's special status**: a reference type that behaves like a value for cloning purposes, which is why the first `Resume` version "worked" by accident.
- **WorkExperience**: the referenced object that exposes the shallow-copy bug once `Resume` holds it.
- **深复制的层数**: how many levels of references to clone; decide in advance, beware cycles.

## Mental Models
- Think of `clone()` as photocopying: fast, no constructor cost, but a photocopy of a page that says "see attached sheet" still points to the same attached sheet.
- Use "does the copy need its own X?" for every reference field; if yes, clone X inside `clone()`.
- Prefer clone over `new` when initialisation is stable and expensive: each `new` reruns the constructor.
- Use prototype in code, but not for job applications: the author's closing point is that hand-written cover letters stand out precisely because everyone copies.

## Anti-patterns
- **N instantiations for N near-identical objects**: three résumés = three `new Resume(...)` with the same setter calls; a single typo must be fixed N times.
- **Assignment instead of copy**: `Resume resume2 = resume1;` shares one object; all three "résumés" show the last edit.
- **Shallow clone with reference fields**: after adding `WorkExperience`, all three cloned résumés display the final `setWorkExperience` because they share one `WorkExperience` instance.
- **Unbounded deep copy**: résumé → experience → company → position …; cloning every level blindly is expensive and can loop on circular references.

## Code Examples
Textbook prototype in Java:

```java
abstract class Prototype implements Cloneable {
    private String id;
    public Prototype(String id) { this.id = id; }
    public String getID() { return id; }
    public Object clone() {                       // the key of the pattern
        Object object = null;
        try { object = super.clone(); }
        catch (CloneNotSupportedException e) { System.err.println("Clone异常。"); }
        return object;
    }
}
class ConcretePrototype extends Prototype {
    public ConcretePrototype(String id) { super(id); }
}

ConcretePrototype p1 = new ConcretePrototype("编号123456");
ConcretePrototype c1 = (ConcretePrototype) p1.clone();   // no constructor run
```
- **What it demonstrates**: clone-based creation; in Java `Cloneable` + `clone()` is all you need.

Deep copy of the résumé (final version):

```java
class WorkExperience implements Cloneable {
    private String timeArea, company;
    // getters/setters omitted
    public WorkExperience clone() {
        try { return (WorkExperience) super.clone(); }
        catch (CloneNotSupportedException e) { System.err.println("Clone异常。"); return null; }
    }
}

class Resume implements Cloneable {
    private String name, sex, age;
    private WorkExperience work;                 // reference-typed field
    public Resume(String name) { this.name = name; this.work = new WorkExperience(); }
    public void setPersonalInfo(String sex, String age) { this.sex = sex; this.age = age; }
    public void setWorkExperience(String timeArea, String company) {
        work.setTimeArea(timeArea); work.setCompany(company);
    }
    public void display() {
        System.out.println(name + " " + sex + " " + age);
        System.out.println("工作经历 " + work.getTimeArea() + " " + work.getCompany());
    }
    public Resume clone() {
        Resume object = null;
        try {
            object = (Resume) super.clone();
            object.work = this.work.clone();     // deep copy: give the copy its own WorkExperience
        } catch (CloneNotSupportedException e) { System.err.println("Clone异常。"); }
        return object;
    }
}

Resume resume1 = new Resume("大鸟");
resume1.setPersonalInfo("男", "29");
resume1.setWorkExperience("1998-2000", "XX公司");
Resume resume2 = resume1.clone();
resume2.setWorkExperience("2000-2003", "YY集团");
Resume resume3 = resume1.clone();
resume3.setPersonalInfo("男", "24");
resume3.setWorkExperience("2003-2006", "ZZ公司");
resume1.display(); resume2.display(); resume3.display();   // three different work histories
```
- **What it demonstrates**: one line (`object.work = this.work.clone()`) turns the shallow copy into a deep copy at depth one, which is all this example needs.

## Worked Example
1. **Version 1 — hand-written era**: `Resume` with only `String` fields; client does `new Resume(...)` three times with identical setters. Works, but every change is N edits. Shortcut `resume2 = resume1` is rejected: that's pass-by-reference, three names for one object.
2. **Version 2 — clone**: `Resume implements Cloneable`, `clone()` returns `(Resume) super.clone()`. Client clones once per copy and edits only the differing fields. Works because all fields are `String`.
3. **What broke — version 3**: a real design extracts `WorkExperience` as its own class held by reference. Client sets different experiences on each clone, but all three print the last one: shallow copy shares the single `WorkExperience`.
4. **Refactor — version 4 (deep copy)**: make `WorkExperience` cloneable and clone it inside `Resume.clone()`. Same client code now prints the expected three histories.
5. **Why**: `super.clone()` copies references, not referents; a deep copy re-points each reference field at a fresh copy. Depth is a design decision: here one level suffices.

## Key Takeaways
1. Use prototype when you need many similar objects and initialisation is expensive or stable; clone and tweak instead of re-running constructors.
2. In Java, prototype = `implements Cloneable` + overriding `clone()` around `super.clone()`; no abstract `Prototype` class needed.
3. `super.clone()` is shallow: value fields are copied, reference fields are shared.
4. For each reference field, decide explicitly whether the copy needs its own instance; if so, clone it inside `clone()`.
5. Fix deep-copy depth in advance and guard against circular references.
6. Assignment (`b = a`) is never a copy.

## Connects To
- **[ch08](ch08-factory-method.md)**: another creational pattern; factories encapsulate `new`, prototype avoids `new` altogether.
- **[ch18](ch18-memento.md)**: memento also captures object state for later use; prototype copies the whole object, memento externalises a snapshot.
- **[ch29](ch29-pattern-summary.md)**: 原型小姐 argues "建立相应数目的原型并克隆它们通常比每次用合适的状态手工实例化该类更方便"[DP].
- **[ch00](ch00-oo-basics.md)**: value vs. reference semantics underlie the shallow/deep distinction.
