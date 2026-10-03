# 第18章：如果再回到从前——备忘录模式（Memento）

## 核心思想
要让对象在不暴露内部细节的前提下回滚到早先的状态，就让对象自己把需要保存的状态打包进一个独立的备忘录对象，再交给管理者保存，管理者只存放、从不查看。这样客户端完全不知道有哪些字段。

## 引入的框架
- **备忘录模式（Memento）** — “在不破坏封装性的前提下，捕获一个对象的内部状态，并在该对象之外保存这个状态。这样以后就可将该对象恢复到原先保存的状态。”[DP]
  - 结构：`Originator`（`state`、`createMemento()`、`recoveryMemento(Memento)`）→ `Memento`（保存状态）；`Caretaker`（`memento` 属性，只有 get/set）。
  - 适用场景：某个类是"功能比较复杂的，但需要维护或记录属性历史的"，或者"需要保存的属性只是众多属性中的一小部分"；也用于为命令模式（Command）实现撤销。
  - 做法：(1) Originator 决定哪些字段放进备忘录；(2) `createMemento()` 用这些字段构造并返回新的 Memento；(3) Caretaker 持有它；(4) `recoveryMemento(m)` 把字段复制回去。
- **宽接口 / 窄接口（wide vs narrow interface）** — Originator 看到备忘录的宽接口（全部已保存数据）；Caretaker 只看到窄接口，并且"只能将备忘录传递给其他对象"。

## 关键概念
- **Originator（发起人）**："负责创建一个备忘录Memento，用以记录当前时刻它的内部状态，并可使用备忘录恢复内部状态"；保存什么只由它决定。
- **Memento（备忘录）**："负责存储Originator对象的内部状态，并可防止Originator以外的其他对象访问备忘录"。
- **Caretaker（管理者）**："负责保存好备忘录Memento，不能对备忘录的内容进行操作或检查"。
- **职责分离（responsibility separation）**：客户端不应该知道角色有生命力、攻击力、防御力，更不应该逐个字段去复制。
- **部分状态（partial state）**：备忘录不必保存全部内容，只保存值得恢复的字段。
- **克隆充当备忘录**：当*全部*状态都要保存时可以接受，但这会把 Originator 的完整公开接口暴露给上层。
- **内存成本（memory cost）**：每个备忘录都是所保存字段的完整副本；体量大或频繁的快照代价高昂。

## 心智模型
- 把备忘录想象成一个**封口的信封**：发起人写入并读取它，管理者只负责传递。
- 内存中的撤销、后退、悔棋用备忘录模式；存盘退出则用磁盘持久化。
- 问一句「谁需要知道字段列表？」——只有 Originator。如果客户端需要知道，封装就已经泄漏了。
- 当命令必须可撤销时，把备忘录模式与命令模式搭配使用：命令保存执行前状态的备忘录。

## 反模式
- **在客户端通过复制字段做备份**：客户端里写 `backup.setVitality(role.getVitality()); …`——"把整个游戏角色的细节暴露给了客户端"；增加魔法力，或把生命力改名为经验值，都会破坏客户端。
- **用第二个 Originator 实例当备份**：只有在全部内容都要保存时才行得通，并且会把整个公开 API 暴露给调用方。
- **让管理者读取或修改备忘录**：违反窄接口规则，并让客户端重新与状态布局耦合。
- **每次变化都为庞大的状态做快照**：这个模式不是免费的；"也不是用得越多越好"。

## 代码示例
通用结构：
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
- **演示内容**：客户端从不直接触碰 `state`；保存/恢复协议就是两次方法调用。

游戏进度版本：
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
- **演示内容**：新增一项属性只需修改 `GameRole` 和 `RoleStateMemento`；客户端保持不变。

## 实战示例
大鸟的场景：游戏角色有生命力/攻击力/防御力；玩家在一场失败的战斗之后，可以恢复到与 Boss 交战前的状态。

1. **朴素做法**：`GameRole` 有三个属性；客户端创建 `backup = new GameRole()`，在 `fight()` 之前把每个字段复制过去，之后再逐个复制回来。这样能跑——"代码无错未必优"。
2. **诊断**：客户端的职责过大：它必须知道每个字段并亲自执行备份。任何新增字段或改名，都要同时修改客户端里的保存块和恢复块。
3. **需求**：把保存/恢复的细节"封装在外部的类当中，以体现职责分离"。
4. **重构**：`GameRole` 新增 `saveState()` → `RoleStateMemento` 和 `recoveryState(memento)`。`RoleStateMemento` 只保存这三个 int。`RoleStateCaretaker` 用 get/set 持有一个备忘录。
5. **重构后的客户端**：`stateAdmin.setRoleStateMemento(role.saveState()); role.fight(); role.recoveryState(stateAdmin.getRoleStateMemento());`——没有出现任何字段名。
6. **注意事项**：大鸟提醒，备忘录是所保存字段的完整副本；状态很大时，内存增长很快。

为什么有效：Originator 同时掌握自己字段的知识和两个转换方法，所以封装保持完整，状态却仍能存放在对象之外。

## 关键要点
1. 让 Originator 创建并消费备忘录；绝不让客户端复制字段。
2. 只保存需要恢复的字段——备忘录是子集而不是克隆，除非所有内容都需要。
3. Caretaker 是个只管存放的哑持有者：get 和 set，不读取内容。
4. 用于撤销、后退、悔棋，以及保存在内存中的检查点前的快照；磁盘持久化另行处理。
5. 命令模式 + 备忘录模式是实现可撤销操作的标准做法。
6. 控制内存预算：频繁的大快照是这个模式的主要代价。

## 关联章节
- **[ch23](ch23-command.md)**："命令模式可以使用备忘录模式来存储可撤销操作的状态"[DP]。
- **[ch09](ch09-prototype.md)**：需要保存整个对象时，克隆是替代方案；只需保存一部分时，优先用备忘录模式。
- **[ch03](ch03-single-responsibility.md)**：这次重构的驱动力，是把保存/恢复的职责从客户端中抽走。
- **[ch16](ch16-state.md)**：状态模式（State）让行为随状态改变；备忘录模式对状态做快照并恢复。
- **[ch29](ch29-pattern-summary.md)**：备忘录模式在比赛中出现在行为型一组。
