# 🌐 Browser History Simulator (Doubly Linked List Engine)

A high-performance, lightweight prototype simulating real-world browser history navigation using a **Doubly Linked List (DLL)** data structure.

---

## 🚀 Key Features

- **Bidirectional Navigation**: Instant $O(1)$ backward (`prev`) and forward (`next`) movement.
- **Forward History Pruning**: Real browser behavior where navigating to a new URL after going back severs and truncates the forward history chain.
- **Multiple Step Jumps**: Support for jumping $k$ steps backward (`back(k)`) or forward (`forward(k)`).
- **Interactive Visual Prototype (`index.html`)**:
  - Live visual inspection of Doubly Linked List nodes and bi-directional pointers (`⟵ ⟶`).
  - Active node highlighting and real-time pointer inspection (`prev`, `next`).
  - Address bar (Omnibox), bookmark shortcuts, and simulated web viewport.
  - Live pointer & memory operation event log.
- **Python CLI Simulator (`browser_history.py`)**:
  - Pure Python (no external dependencies).
  - Built-in verification test suite (`--test`).
  - Interactive REPL terminal with ASCII pointer tree rendering.

---

## 🧠 Data Structure Design & Time Complexity

```
[HEAD: Google] ⟵ ⟶ [Node 1: GitHub] ⟵ ⟶ [*CURRENT: Wikipedia*] ⟵ ⟶ [TAIL: YouTube]
```

| Operation | Doubly Linked List | 2 Stacks Alternative | Dynamic Array |
| :--- | :---: | :---: | :---: |
| **`visit(url)`** | **$O(1)$** pointer update | $O(1)$ push + clear | $O(N)$ truncation/shift |
| **`back(1)`** | **$O(1)$** (`current = current.prev`) | $O(1)$ pop/push | $O(1)$ index decrement |
| **`forward(1)`** | **$O(1)$** (`current = current.next`) | $O(1)$ pop/push | $O(1)$ index increment |
| **`back(k)` / `forward(k)`** | **$O(\min(k, N))$** traversal | $O(k)$ stack transfers | $O(1)$ index offset |
| **Node Pruning (Branching)** | **$O(1)$** (`current.next = null`) | $O(F)$ stack clear | $O(F)$ array slice |
| **Direct Node Pointer Jump** | **$O(1)$** reference assignment | Not supported directly | $O(1)$ index lookup |

### Why Doubly Linked List for Browsers?
1. In a browser tab, history is fundamentally a sequence of states with a bidirectional cursor (`current`).
2. Moving backward or forward 1 step is an instantaneous pointer hop: `current = current.prev` or `current = current.next`.
3. When a user navigates to a new page from the middle of history, all forward history is discarded. In a Doubly Linked List, this is achieved in $O(1)$ by severing `current.next = null`.

---

## 💻 How to Run

### 1. Python Interactive Simulator

Run the interactive CLI session:
```bash
python browser_history.py
```

Run the automated test suite:
```bash
python browser_history.py --test
```

#### CLI Commands:
- `visit <url> [title]` : Navigate to a new webpage
- `back [steps]`        : Move backward by $N$ steps (default 1)
- `forward [steps]`     : Move forward by $N$ steps (default 1)
- `history`             : Print visual ASCII linked list structure
- `current`             : Print active node info & pointer addresses
- `test`                : Execute test assertions
- `clear`                : Reset history to homepage

---

### 2. Interactive Web UI Prototype

Simply open `index.html` in any web browser:
```bash
# On Windows PowerShell:
Start-Process index.html
```

Or open the standalone artifact directly in your IDE preview pane.
