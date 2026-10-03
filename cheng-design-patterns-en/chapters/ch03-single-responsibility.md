# Chapter 3: 电子阅读器vs.手机——单一职责原则 — E-reader vs. Phone: Single Responsibility Principle

## Core Idea
A class should have exactly one reason to change. The e-reader reads better than the phone because it does only one thing; a Tetris game whose window class holds both drawing code and game logic cannot be ported, tested or reused because two unrelated reasons to change are welded together. Most of real design work is “发现职责并把那些职责相互分离” (discovering responsibilities and separating them).

## Frameworks Introduced
- **单一职责原则 (Single Responsibility Principle, SRP)** — “就一个类而言，应该仅有一个引起它变化的原因。”[ASD]
  - Story analogy: the phone is “不纯粹” (impure): reading on it is constantly interrupted by messages, news and ads; the e-ink reader “只针对阅读来设计产品，做到了功能上的纯粹”.
  - When to use: as a test on every class, especially the "Form1"/window/controller class where beginners dump business rules and SQL.
  - How: (1) ask “能够想到多于一个的动机去改变一个类吗？” (can I think of more than one motive to change this class?); if yes, it has more than one responsibility [ASD]; (2) list what is stable versus what is volatile (game rules vs. rendering); (3) split into one class per responsibility; (4) let the volatile side depend on the stable side.
- **职责耦合的代价 (Cost of coupled responsibilities)** — “如果一个类承担的职责过多，就等于把这些职责耦合在一起，一个职责的变化可能会削弱或者抑制这个类完成其他职责的能力。这种耦合会导致脆弱的设计，当变化发生时，设计会遭受到意想不到的破坏。”[ASD]

## Key Concepts
- **职责 (Responsibility)**: a reason to change; not "a feature" but "an axis of variation".
- **界面表示逻辑 (Presentation logic)**: drawing/erasing blocks, mapping key presses to calls; volatile.
- **游戏逻辑 (Game logic)**: fall, rotate, collision, move, stack, clear lines; stable.
- **沉浸/心流 (Immersion / flow)**: the author's metaphor for what a single-purpose design achieves.
- **整合 vs 单一 (Integration vs. single purpose)**: both valid product strategies (smartphone vs. e-reader); in code, prefer single purpose per class.

## Mental Models
- **Use "how many reasons could this class change for?" as the SRP probe.** One is right; two means split.
- **Think of a class's volatile half and stable half as different classes waiting to be separated.** UI changes often; rules rarely.
- **Model the domain as data, not as pixels.** Tetris is a `int[10][20]` grid; falling is `arr[x][y]` → `arr[x][y+1]`; a left-move collision is `x-1 < 0 || arr[x-1][y] == 1`; a full row is all ones across `x = 0..9`. Once the logic is data operations, the UI is just a renderer over it.
- **Both the phone and the e-reader are good products.** SRP is about classes, not about arguing that integration is always wrong.

## Anti-patterns
- **The god window class**: business algorithms, database SQL and event handlers all in `Form1`/`窗体.java`; any requirement touches it; nothing is reusable.
- **Thinking in event handlers**: “关键在于各种事件代码如何写吧，这里有什么类可言呢？” is the procedural mindset; events are entry points, not the design.
- **Copy-and-tweak porting**: moving Tetris to 3D/web/desktop by copying the window class and editing it, because logic and drawing were never separated.
- **Splitting for its own sake**: SRP asks for one reason to change, not for the maximum number of classes.

## Code Examples
No listings in the chapter; the design is described. A minimal shape of the separation the author describes:

```java
// 游戏逻辑：stable, UI-free, independently testable
public class TetrisGame {
    private int[][] arraySquare = new int[10][20];   // 1 = block present

    public boolean canMoveLeft(int x, int y) {
        return x - 1 >= 0 && arraySquare[x - 1][y] == 0;
    }
    public boolean isLanded(int x, int y) {
        return y + 1 >= 20 || arraySquare[x][y + 1] == 1;
    }
    public void clearFullRows() {
        for (int y = 0; y < 20; y++) {
            boolean full = true;
            for (int x = 0; x < 10; x++) if (arraySquare[x][y] == 0) { full = false; break; }
            if (full) { /* zero row y, shift rows above down by one */ }
        }
    }
    public int[][] snapshot() { return arraySquare; }
}

// 界面：volatile; only draws the grid and forwards key presses
public class TetrisForm {
    private final TetrisGame game = new TetrisGame();
    void onTimerTick()  { /* erase, ask game to advance, draw game.snapshot() */ }
    void onLeftKey()    { /* if (game.canMoveLeft(x, y)) move */ }
}
```
- **What it demonstrates**: swapping `TetrisForm` for a 3D or web renderer leaves `TetrisGame` untouched; the game rules can be unit-tested with no window at all.

## Worked Example
小菜 is asked how he would build mobile Tetris. His plan: a window, a game panel control, a Start button, a timer whose tick draws and erases four squares, key handlers for left/right/down/rotate, some GDI+ drawing, plus collision, stacking and line-clearing "somewhere in the handlers".

大鸟's challenge: divide this into classes. 小菜 cannot: “这里有什么类可言呢？” His procedural habit is “根深蒂固” (deep-rooted).

The pivot question: if you now need a 3D version, a web version and a desktop version, what can you reuse? Answer: nothing, everything is in one window class. Yet fall, rotate, collision, move and stack never change across versions.

The separation: represent the board as `int[10][20]`. Every rule becomes an array operation: moving is an index change, collision is a neighbour check, landing is `arr[x][y+1] == 1`, clearing a line is a row scan plus shift-down. That is the game-logic class. The window class only renders the array and translates key presses into calls. When the UI changes, only the window class changes; the logic is reused as-is.

小菜's honest reaction: “这个听起来容易，真正要做起来还是有难度的哦！” 大鸟's reply is the chapter's thesis: discovering and separating responsibilities *is* the hard part of software design [ASD].

## Key Takeaways
1. One class, one reason to change.
2. Test a class with: "can I think of more than one motive to change it?" If yes, split.
3. Separate volatile presentation from stable rules; make presentation depend on rules, never the reverse.
4. Reformulate domain behaviour as operations on data; the UI becomes a thin renderer.
5. Coupled responsibilities make designs fragile: a change for one reason breaks the class's ability to serve the other.
6. Finding responsibilities is most of design; do not expect it to be easy.

## Connects To
- **[ch01](ch01-simple-factory.md)**: separating `Operation` from the console UI was SRP in miniature.
- **[ch04](ch04-open-closed.md)**: SRP-separated classes are the ones you can close to modification.
- **[ch11](ch11-law-of-demeter.md)**: the other "keep classes narrow" principle: minimise what a class knows, not just what it does.
- **[ch12](ch12-facade.md)**: a facade lets a UI depend on one responsibility-focused entry point instead of many subsystems.
- **[ch29](ch29-pattern-summary.md)**: 单一职责 sits on the judging panel; every pattern is scored against it.
