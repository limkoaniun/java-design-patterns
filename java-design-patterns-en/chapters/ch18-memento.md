# Chapter 18: 如果再回到从前——备忘录模式 — Memento

## Core Idea
To let an object roll back to an earlier state without exposing its internals, have the object itself package the state it wants saved into a separate memento object, and hand that to a caretaker that stores but never inspects it. The client then knows nothing about which fields exist.

## Frameworks Introduced
- **备忘录模式 (Memento)** — “在不破坏封装性的前提下，捕获一个对象的内部状态，并在该对象之外保存这个状态。这样以后就可将该对象恢复到原先保存的状态。”[DP]
  - Structure: `Originator` (`state`, `createMemento()`, `recoveryMemento(Memento)`) → `Memento` (holds the saved state); `Caretaker` (`memento` property — get/set only).
  - When to use: a class is "功能比较复杂的，但需要维护或记录属性历史的", or "需要保存的属性只是众多属性中的一小部分"; also to implement undo for Command.
  - How: (1) the Originator decides which fields go into the memento; (2) `createMemento()` returns a new Memento built from those fields; (3) the Caretaker holds it; (4) `recoveryMemento(m)` copies fields back.
- **宽接口 / 窄接口 (wide vs narrow interface)** — the Originator sees the memento's wide interface (all saved data); the Caretaker sees only a narrow one and "只能将备忘录传递给其他对象".

## Key Concepts
- **Originator (发起人)**: "负责创建一个备忘录Memento，用以记录当前时刻它的内部状态，并可使用备忘录恢复内部状态"; it alone decides what is saved.
- **Memento (备忘录)**: "负责存储Originator对象的内部状态，并可防止Originator以外的其他对象访问备忘录".
- **Caretaker (管理者)**: "负责保存好备忘录Memento，不能对备忘录的内容进行操作或检查".
- **职责分离 (responsibility separation)**: the client should not know a role has vitality/attack/defense, let alone copy them field by field.
- **部分状态 (partial state)**: a memento need not hold everything — only the fields worth restoring.
- **Clone as memento**: acceptable when *all* state must be saved, but it exposes the Originator's full public interface to the upper layer.
- **内存成本 (memory cost)**: each memento is a full copy of the saved fields; large or frequent snapshots are expensive.

## Mental Models
- Think of the memento as a **sealed envelope**: the originator writes and reads it, the caretaker only carries it.
- Use Memento for in-memory undo/back/regret-move; use disk persistence for save-and-quit.
- Ask "who needs to know the field list?" — only the Originator. If the client does, encapsulation has leaked.
- Pair Memento with Command when a command must be undoable: the command stores a memento of pre-execution state.

## Anti-patterns
- **Client-side backup by copying fields**: `backup.setVitality(role.getVitality()); …` in the client — "把整个游戏角色的细节暴露给了客户端"; adding 魔法力 or renaming 生命力 to 经验值 breaks the client.
- **Using a second Originator instance as the backup**: works only when everything must be saved and opens the whole public API to the caller.
- **Letting the caretaker read or edit the memento**: violates the narrow-interface rule and re-couples the client to the state layout.
- **Snapshotting huge state on every change**: the pattern is not free; "也不是用得越多越好".

## Code Examples
Generic structure:
```java
class Originator {
    private String state;
    public String getState() { return state; }
    public void setState(String value) { this.state = value; }
    public void show() { System.out.println("State:" + state); }
    public Memento createMemento() { return new Memento(state); }            // originator decides what to save
    public void recoveryMemento(Memento memento) { setState(memento.getState()); }
}
class Memento {
    private String state;
    public Memento(String state) { this.state = state; }
    public String getState() { return state; }
}
class Caretaker {
    private Memento memento;
    public Memento getMemento() { return memento; }
    public void setMemento(Memento value) { this.memento = value; }   // store only, never inspect
}

Originator o = new Originator(); o.setState("On"); o.show();
Caretaker c = new Caretaker();
c.setMemento(o.createMemento());
o.setState("Off"); o.show();
o.recoveryMemento(c.getMemento()); o.show();      // back to "On"
```
- **What it demonstrates**: the client never touches `state` directly; the save/restore protocol is two method calls.

Game-progress version:
```java
class GameRole {
    private int vitality, attack, defense;
    public void getInitState() { vitality = attack = defense = 100; }
    public void fight()        { vitality = attack = defense = 0; }     // Boss battle drains everything
    public void displayState() { System.out.println("体力:" + vitality + " 攻击力:" + attack + " 防御力:" + defense); }

    public RoleStateMemento saveState() { return new RoleStateMemento(vitality, attack, defense); }
    public void recoveryState(RoleStateMemento m) {
        vitality = m.getVitality(); attack = m.getAttack(); defense = m.getDefense();
    }
}
class RoleStateMemento {                 // 角色状态存储箱
    private int vitality, attack, defense;
    public RoleStateMemento(int vitality, int attack, int defense) { this.vitality = vitality; this.attack = attack; this.defense = defense; }
    public int getVitality() { return vitality; }  public int getAttack() { return attack; }  public int getDefense() { return defense; }
}
class RoleStateCaretaker {               // 角色状态管理者
    private RoleStateMemento memento;
    public RoleStateMemento getRoleStateMemento() { return memento; }
    public void setRoleStateMemento(RoleStateMemento value) { this.memento = value; }
}

GameRole role = new GameRole(); role.getInitState(); role.displayState();
RoleStateCaretaker stateAdmin = new RoleStateCaretaker();
stateAdmin.setRoleStateMemento(role.saveState());     // 保存进度
role.fight(); role.displayState();                     // all zeros
role.recoveryState(stateAdmin.getRoleStateMemento()); // 恢复
role.displayState();                                   // back to 100/100/100
```
- **What it demonstrates**: adding a new stat means editing `GameRole` and `RoleStateMemento` only; the client is unchanged.

## Worked Example
大鸟's scenario: a game character has 生命力/攻击力/防御力; the player may restore to the pre-Boss state after a bad fight.

1. **Naive**: `GameRole` with three properties; client creates `backup = new GameRole()` and copies each field across before `fight()`, then copies each back. It works — "代码无错未必优".
2. **Diagnosis**: the client's responsibility is too large: it must know every field and perform the backup. Any new field or rename edits both the save and the restore blocks in the client.
3. **Requirement**: encapsulate the save/restore details "封装在外部的类当中，以体现职责分离".
4. **Refactor**: `GameRole` gains `saveState()` → `RoleStateMemento` and `recoveryState(memento)`. `RoleStateMemento` holds only the three ints. `RoleStateCaretaker` holds one memento with get/set.
5. **Client after**: `stateAdmin.setRoleStateMemento(role.saveState()); role.fight(); role.recoveryState(stateAdmin.getRoleStateMemento());` — no field names anywhere.
6. **Caveat**: 大鸟 warns that a memento is a full copy of the saved fields; with large state, memory grows fast.

Why it works: the Originator owns both the knowledge of its fields and the two conversion methods, so encapsulation stays intact while state still lives outside the object.

## Key Takeaways
1. Let the Originator create and consume the memento; never let the client copy fields.
2. Save only the fields that need restoring — the memento is a subset, not a clone, unless everything is needed.
3. The Caretaker is a dumb holder: get and set, no reads of contents.
4. Use it for undo, back, regret-move, and pre-checkpoint snapshots kept in memory; persist to disk separately.
5. Command + Memento is the standard way to implement undoable operations.
6. Budget memory: frequent large snapshots are the pattern's main cost.

## Connects To
- **[ch23](ch23-command.md)**: "命令模式可以使用备忘录模式来存储可撤销操作的状态"[DP].
- **[ch09](ch09-prototype.md)**: clone is the alternative when the whole object must be saved; Memento is preferred when only part is.
- **[ch03](ch03-single-responsibility.md)**: the refactor is driven by pulling save/restore responsibility out of the client.
- **[ch16](ch16-state.md)**: State changes behaviour with state; Memento snapshots and restores state.
- **[ch29](ch29-pattern-summary.md)**: Memento appears in the behavioural group of the contest.
