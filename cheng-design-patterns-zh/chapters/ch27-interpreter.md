# 第27章：其实你不懂老板的心——解释器模式（Interpreter）

## 核心思想
当某类问题反复出现时，把每个实例表示为一门小语言中的一个句子，并为这门语言构建解释器；文法规则变成类，因此扩展文法意味着添加子类，而不是修改算法。

## 引入的框架
- **解释器模式（Interpreter）** — “给定一个语言，定义它的文法的一种表示，并定义一个解释器，这个解释器使用该表示来解释语言中的句子。”[DP]
  - 结构：`AbstractExpression`（声明抽象语法树中每个节点共有的 `interpret(Context)`）→ `TerminalExpression`（文法中每个终结符一个）和 `NonterminalExpression`（每条文法规则 R1..Rn 一个，递归地解释它所包含的符号）；`Context` 保存解释器之外的全局信息；客户端为一个句子构建语法树并调用 `interpret`。
  - 适用场景：“当有一个语言需要解释执行，并且你可将该语言中的句子表示为一个抽象语法树时”[DP]。例如正则表达式、浏览器解释 HTML、机器人命令脚本、手机铃声记谱。
  - 做法：(1) 定义文法；(2) 每个终结符和每条规则各一个类，全部继承自 `AbstractExpression`；(3) 把共享的输入/输出放进 `Context`；(4) 客户端对句子分词，并把每个词元分派给相应的表达式类。
  - 为何有效 / 失败模式：文法规则就是类，所以文法易于通过继承来修改和扩展，节点类也相似且易于编写。但每条规则至少需要一个类，复杂的文法因此难以管理；对于这类文法，作者转而推荐解析器和编译器生成器。

## 关键概念
- **文法（grammar）**：迷你语言的规则；该模式用一个类层次结构来表示它。
- **抽象语法树（abstract syntax tree）**：表示一个句子的表达式对象树。
- **终结符 / 非终结符（terminal / nonterminal）**：叶子符号与由其他符号组成的规则；音乐示例只有终结符，作者指出这是对该模式不完整的呈现。
- **Context**：承载剩余输入和累积输出的对象。
- **迷你语言 / 迷你程序**：小菜的说法，即用来陈述问题的微型语言，以及用它写成的微型程序。
- **潜台词（subtext）**：本章的故事引子；老板称赞"你在公司表现格外出色"其实意味着还有更多工作，而"梅星是个普通员工"意味着梅星要走人了。

## 心智模型
- 把解释器模式看作为自己编写一门脚本语言；这正是它难的原因，也是只有句子反复出现时才值得的原因。
- 用正则表达式来检验：不必为每种字符串模式（邮箱、电话）各写一个专用函数，一个通用算法就能解释一门模式语言。
- 出现新命令时，优先添加文法子类，而不是修改 switch；依赖倒转原则（DIP）让文法扩展的成本很低。
- 把客户端中将词元映射到表达式类的 switch 视为实例化问题；简单工厂模式（Simple Factory）加反射可以免去对客户端的修改。

## 反模式
- **为每种句子类型手写一个函数**：新增一条命令就要新增一个算法，而不是新增一条文法规则。
- **为复杂文法使用解释器模式**：数十个规则类会变得无法管理；应改用解析器生成器。
- **客户端 switch 不断增长**：添加 `T`（速度）需要在客户端新增一个 `case`；作者为了教学接受了这一点，但指出了修复办法。
- **把音乐演示误当作完整的模式**：它没有非终结符表达式，因此没有展示对规则的递归。

## 代码示例
音乐记谱解释器。文法：`O n` 设置音阶（1 低、2 中、3 高），`C D E F G A B` 是音符，`P` 是休止符，数字是节拍长度，词元以空格分隔。

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
- **它展示了什么**：`Expression.interpret` 中的模板只做一次分词；每个终结符类只需实现 `excute`。添加速度只需多一个子类加一个 `case`：

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

## 实战示例
1. **问题**：根据记谱字符串演奏《上海滩》的第一个乐句，就像 QBASIC 的 `PLAY` 语句或旧式手机铃声编辑器那样。记谱是一门迷你语言；每个乐句就是一个句子。
2. **设计**：`PlayContext` 承载剩余文本。`Expression.interpret` 读取一个字母及其数字，并交给 `excute`。`Note` 把字母映射为简谱数字；`Scale` 把 `O 1/2/3` 映射为低音/中音/高音。客户端循环处理文本，按开头字母选择表达式类。
3. **输出**：`中音 3 5 6 3 5 2 3 5 6 高音 1 中音 6 5 1 3 2 ...` 打印到控制台；目标是模式本身，而不是音频。
4. **扩展**：大鸟要求加入速度 `T 1000`。小菜添加了 `Speed extends Expression` 和一个 `case "T"`。大鸟指出客户端仍然被修改了；解决办法是在 switch 处使用带反射的简单工厂模式，小菜立刻就明白了。
5. **注意事项**：这个示例只有终结符表达式，没有非终结符，因此没有展示对递归规则的解释。要完整理解该模式，应研究带有组合规则的文法。

## 关键要点
1. 当一个反复出现的问题可以表述为一门小语言中的句子，并且你能把句子表示为语法树时，使用解释器模式。
2. 把每条文法规则表示为一个类；通过继承来扩展文法，而不是修改算法。
3. 把共享的输入和输出放在 `Context` 对象中；把分词放在抽象表达式的模板里，使终结符保持简单。
4. 如果文法很大，就停下来；使用解析器或编译器生成器，而不是数十个规则类。
5. 客户端中词元到类的 switch 是一种实例化坏味道；工厂加反射可以消除它。
6. 正则表达式是典型应用：用一个通用解释器取代为每种模式各写一个函数。

## 关联章节
- **[ch10](ch10-template-method.md)**：`Expression.interpret` 是一个模板方法；子类补全 `excute`。
- **[ch01](ch01-simple-factory.md)** / **[ch15](ch15-abstract-factory.md)**：为客户端 switch 所建议的基于反射的工厂。
- **[ch05](ch05-dependency-inversion.md)**：文法扩展依赖于抽象 `Expression`，这正是它成本低的原因。
- **[ch19](ch19-composite.md)**：带有非终结符的完整语法树就是表达式的组合模式（Composite）。
- **[ch29](ch29-pattern-summary.md)**：解释器模式在比赛中的答案重申了正则表达式这一动机。
