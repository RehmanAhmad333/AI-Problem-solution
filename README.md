# 🧭 Maze Solver using Depth-First Search (Python)

A clean, object-oriented Python implementation of a maze solver that uses **Depth-First Search (DFS)** with a stack-based frontier. It reads a maze from a text file, finds a path from start (`A`) to goal (`B`), prints the solution in the terminal, and saves a color-coded image.

![Language](https://img.shields.io/badge/Language-Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Algorithm](https://img.shields.io/badge/Algorithm-DFS-2563EB?style=for-the-badge)
![License](https://img.shields.io/badge/License-Not%20Specified-lightgrey?style=for-the-badge)

---

## ✨ Features

- 🔎 **Depth-First Search** using a `StackFrontier`
- 🧱 Simple text-based maze format (`#` walls, `A` start, `B` goal)
- 🖥️ Pretty terminal output with the solution path marked by `*`
- 🖼️ Image export (`maze.png`) with walls, start, goal, solution, and optionally explored cells
- 🧩 Clean OOP design: `Node`, `StackFrontier`, `QueueFrontier`, `Maze`

---

## 📂 Project Structure

```text
.
├── Maze_Problem.py      # Solver and visualizer
└── README.md
```

---

## 🧩 Maze Format

Create a `maze.txt` file. Use these characters:

| Symbol | Meaning |
|:---:|---|
| `#` | Wall |
| ` ` (space) | Open path |
| `A` | Start (exactly one) |
| `B` | Goal (exactly one) |

Example:

```text
##########
#A   #   #
# ## # # #
#    #   #
###### ###
#      B #
##########
```

> The code treats any character other than `A`, `B`, or a space as a wall.

---

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- [Pillow](https://pypi.org/project/Pillow/) for image output

```bash
pip install pillow
```

### Run

```bash
python Maze_Problem.py
```

**Output**
- The original maze and the solved maze in the terminal
- `maze.png` saved in the same folder

---

## 🖼️ Output Legend

| Color | Meaning |
|---|---|
| ⬛ Dark gray | Wall |
| 🟥 Red | Start (`A`) |
| 🟩 Green | Goal (`B`) |
| 🟨 Yellow | Solution path |
| 🟧 Orange | Explored cells (when `show_explored=True`) |
| ⬜ Light | Open cell |

---

## 🧠 How It Works

1. **Parse** the maze file and build a 2D grid of walls and open cells.
2. **Start** a frontier with the start node.
3. **Pop** the last node from the stack (DFS behaviour).
4. If it is the goal, **rebuild the path** by following `parent` links.
5. Otherwise, **add unexplored neighbours** (up, down, left, right) to the frontier.

Swapping `StackFrontier` for `QueueFrontier` in `solve()` turns this into **Breadth-First Search**, which finds the shortest path.

---

## 🛠️ Customization

```python
m.output_image("maze.png", show_solution=True, show_explored=True)
```

- Change `cell_size` or colors inside `output_image()`.
- Try `QueueFrontier()` instead of `StackFrontier()` to compare DFS and BFS.

---

## ⚠️ Known Limitations

- `contains_state()` should return `False` only after checking all nodes (see the fix above).
- `Image(...)` at the bottom only displays inside Jupyter/IPython notebooks.
- The maze must contain exactly one `A` and one `B`, or the program raises an error.

---

## 🤝 Contributing

Pull requests are welcome. Please keep the code readable and add comments where the logic is non-obvious.

---

## 📄 License

No license has been specified yet. Add a `LICENSE` file (MIT is a common choice) before publishing for reuse.

---

⭐ If this helped you learn search algorithms, consider starring the repo!
