# Chapter 27: 其实你不懂老板的心——解释器模式 — Interpreter

## Core Idea
When a class of problem recurs often enough, express each instance as a sentence in a small language and build an interpreter for that language; grammar rules become classes, so extending the grammar means adding a subclass rather than editing an algorithm.

## Frameworks Introduced
- **解释器模式 (Interpreter)** — “给定一个语言，定义它的文法的一种表示，并定义一个解释器，这个解释器使用该表示来解释语言中的句子。”[DP]
  - Structure: `AbstractExpression` (declares `interpret(Context)` shared by every node of the abstract syntax tree) → `TerminalExpression` (one per terminal symbol in the grammar) and `NonterminalExpression` (one per grammar rule R1..Rn, recursively interpreting the symbols it contains); `Context` holds global information outside the interpreter; the client builds the syntax tree for a sentence and calls `interpret`.
  - When to use: “当有一个语言需要解释执行，并且你可将该语言中的句子表示为一个抽象语法树时”[DP]. Regular expressions, browsers interpreting HTML, robot command scripts, phone ringtone notation.
  - How: (1) define the grammar; (2) one class per terminal and per rule, all deriving from `AbstractExpression`; (3) put shared input/output in `Context`; (4) client tokenises the sentence and dispatches each token to the right expression class.
  - Why it works / failure mode: grammar rules are classes, so the grammar is easy to change and extend by inheritance, and the node classes are similar and simple to write. But every rule needs at least one class, so a complex grammar becomes hard to manage; for those, the author defers to parsers and compiler generators.

## Key Concepts
- **文法 (grammar)**: the rules of the mini-language; the pattern represents it as a class hierarchy.
- **抽象语法树 (abstract syntax tree)**: the tree of expression objects representing one sentence.
- **终结符 / 非终结符 (terminal / nonterminal)**: leaf symbols versus rules composed of other symbols; the music example only has terminals, which the author flags as an incomplete picture of the pattern.
- **Context**: the object carrying the remaining input and accumulated output.
- **迷你语言 / 迷你程序**: 小菜's phrase, a tiny language to state the problem and tiny programs written in it.
- **潜台词 (subtext)**: the chapter's story hook; the boss's praise "你在公司表现格外出色" means more work is coming, and "梅星是个普通员工" means 梅星 is on the way out.

## Mental Models
- Think of Interpreter as writing a scripting language for yourself; that is why it is hard, and why it pays off only when the sentences recur.
- Use the regex test: rather than a bespoke function per string pattern (email, phone), one general algorithm interprets a pattern language.
- Prefer adding a grammar subclass over editing a switch when a new command appears; dependency inversion makes the grammar extension cheap.
- Treat a switch in the client that maps tokens to expression classes as an instantiation problem; a simple factory plus reflection removes the client edit.

## Anti-patterns
- **Hand-written function per sentence type**: a new command means a new algorithm instead of a new grammar rule.
- **Interpreter for a complex grammar**: dozens of rule classes become unmanageable; use a parser generator instead.
- **Client switch growth**: adding `T` (tempo) required a new `case` in the client; the author accepts it for the lesson but names the fix.
- **Mistaking the music demo for the full pattern**: it has no nonterminal expressions, so recursion over rules is not shown.

## Code Examples
The music notation interpreter. Grammar: `O n` sets the scale (1 low, 2 mid, 3 high), `C D E F G A B` are notes, `P` is a rest, numbers are beat lengths, tokens separated by spaces.

```java
// Context
class PlayContext {
    private String playText;
    public String getPlayText() { return this.playText; }
    public void setPlayText(String value) { this.playText = value; }
}
// AbstractExpression: peels one "key value" pair off the text, then delegates
abstract class Expression {
    public void interpret(PlayContext context) {
        if (context.getPlayText().length() == 0) return;
        String playKey = context.getPlayText().substring(0, 1);
        context.setPlayText(context.getPlayText().substring(2));
        double playValue = Double.parseDouble(
            context.getPlayText().substring(0, context.getPlayText().indexOf(" ")));
        context.setPlayText(
            context.getPlayText().substring(context.getPlayText().indexOf(" ") + 1));
        this.excute(playKey, playValue);
    }
    public abstract void excute(String key, double value);
}
// TerminalExpression: note
class Note extends Expression {
    public void excute(String key, double value) {
        String note = "";
        switch (key) {
            case "C": note = "1"; break;  case "D": note = "2"; break;
            case "E": note = "3"; break;  case "F": note = "4"; break;
            case "G": note = "5"; break;  case "A": note = "6"; break;
            case "B": note = "7"; break;
        }
        System.out.print(note + " ");
    }
}
// TerminalExpression: scale
class Scale extends Expression {
    public void excute(String key, double value) {
        String scale = "";
        switch ((int) value) {
            case 1: scale = "低音"; break;
            case 2: scale = "中音"; break;
            case 3: scale = "高音"; break;
        }
        System.out.print(scale + " ");
    }
}
// Client
PlayContext context = new PlayContext();
context.setPlayText("O 2 E 0.5 G 0.5 A 3 E 0.5 G 0.5 D 3 E 0.5 G 0.5 A 0.5 O 3 C 1 O 2 A 0.5 G 1 C 0.5 E 0.5 D 3 ");
Expression expression = null;
while (context.getPlayText().length() > 0) {
    String str = context.getPlayText().substring(0, 1);
    switch (str) {
        case "O": expression = new Scale(); break;
        case "C": case "D": case "E": case "F":
        case "G": case "A": case "B": case "P":
            expression = new Note(); break;
    }
    expression.interpret(context);
}
```
- **What it demonstrates**: the template in `Expression.interpret` does the tokenising once; each terminal class only implements `excute`. Adding tempo is one more subclass plus one `case`:

```java
class Speed extends Expression {
    public void excute(String key, double value) {
        String speed;
        if (value < 500) speed = "快速";
        else if (value >= 1000) speed = "慢速";
        else speed = "中速";
        System.out.print(speed + " ");
    }
}
// client: case "T": expression = new Speed(); break;
```

## Worked Example
1. **Problem**: play the first phrase of 上海滩 from a notation string, the way QBASIC's `PLAY` statement or old phone ringtone editors did. The notation is a mini-language; each phrase is a sentence.
2. **Design**: `PlayContext` carries the remaining text. `Expression.interpret` reads one letter plus its number and hands them to `excute`. `Note` maps letters to 简谱 digits; `Scale` maps `O 1/2/3` to 低音/中音/高音. The client loops over the text choosing the expression class by the leading letter.
3. **Output**: `中音 3 5 6 3 5 2 3 5 6 高音 1 中音 6 5 1 3 2 ...` printed to the console; the goal is the pattern, not audio.
4. **Extension**: 大鸟 asks for tempo `T 1000`. 小菜 adds `Speed extends Expression` and a `case "T"`. 大鸟 points out the client still changed; the fix is a simple factory with reflection at the switch, which 小菜 recognises immediately.
5. **Caveat**: this example has only terminal expressions, no nonterminals, so it does not show recursive rule interpretation. To understand the pattern fully, study grammars with composite rules.

## Key Takeaways
1. Use Interpreter when a recurring problem can be stated as sentences in a small language and you can represent sentences as a syntax tree.
2. Represent each grammar rule as a class; extend the grammar by inheritance, not by editing an algorithm.
3. Keep shared input and output in a `Context` object; keep tokenising in the abstract expression's template so terminals stay trivial.
4. If the grammar is large, stop; use parsers or compiler generators instead of dozens of rule classes.
5. The token-to-class switch in the client is an instantiation smell; a factory plus reflection removes it.
6. Regular expressions are the canonical application: one general interpreter instead of a function per pattern.

## Connects To
- **[ch10](ch10-template-method.md)**: `Expression.interpret` is a template method; subclasses fill in `excute`.
- **[ch01](ch01-simple-factory.md)** / **[ch15](ch15-abstract-factory.md)**: the suggested reflection-based factory for the client switch.
- **[ch05](ch05-dependency-inversion.md)**: grammar extension depends on the abstraction `Expression`, which is what makes it cheap.
- **[ch19](ch19-composite.md)**: a full syntax tree with nonterminals is a Composite of expressions.
- **[ch29](ch29-pattern-summary.md)**: 解释器's contest answer restates the regex motivation.
