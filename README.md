# Flawless Snake AI

A high-performance Snake AI built with **Python** and **Pygame** that uses a **Hamiltonian Cycle strategy with intelligent shortcuts** to guarantee survival while optimizing food collection speed.

---

# Project Overview

This project implements a fully autonomous Snake AI capable of playing the classic Snake game without human input.

The AI uses a Hamiltonian cycle path that covers every cell of the grid exactly once. By following this path, the snake is mathematically guaranteed to never trap itself.

To improve efficiency, the AI also implements a safe shortcut system that allows the snake to reach food faster while still maintaining a valid escape path.

The result is a snake player capable of filling the entire grid and achieving the maximum possible score.

---

# What We Have Achieved So Far

### Autonomous Snake AI

The snake is fully controlled by an AI algorithm and requires no player input.

---

### Hamiltonian Cycle Navigation

A Hamiltonian cycle is generated across the grid so the snake can move safely through every cell.

Benefits:

* No self-collision
* Guaranteed survival
* Complete grid coverage

---

### Intelligent Shortcut System

The AI can temporarily leave the Hamiltonian path to reach food faster.

Shortcuts are taken only when they satisfy strict safety rules:

* The snake must not skip past the food
* The snake must not trap its tail
* The snake must not collide with its body

This significantly reduces the time needed to collect food.

---

### Late-Game Safety Mode

When the snake becomes very long (approximately 85% of the grid), the AI switches to strict Hamiltonian following to eliminate risk and ensure the game finishes successfully.

---

### Dynamic Grid Rendering

The game automatically adjusts the display based on grid size.

Features include:

* Checkered board background
* Rounded snake segments
* Food glow effect
* Score and AI state display

---

### Performance Optimizations

The project includes several optimizations:

* Precomputed Hamiltonian cycle
* Efficient neighbor calculations
* Optimized rendering
* High-speed simulation capability

The game can run at high simulation speeds for AI testing.

---

# AI Strategy

The AI decision system follows this priority order:

1. Safe shortcut if it reduces travel distance without risk
2. Hamiltonian path for guaranteed safe movement
3. Victory lap mode with strict safe movement when the snake becomes large

This hybrid strategy combines safety with efficient food collection.

---

# Current Capabilities

| Feature                      | Status      |
| ---------------------------- | ----------- |
| Autonomous Snake AI          | Complete    |
| Hamiltonian Cycle Generation | Complete    |
| Safe Shortcut Logic          | Implemented |
| Late-Game Safety Mode        | Implemented |
| Dynamic Rendering            | Implemented |
| Performance Optimization     | In Progress |

---

# Technologies Used

* Python 3
* Pygame
* Deque data structure
* Graph traversal algorithms

---

# How to Run

### Install dependencies

```
pip install pygame
```

### Run the program

```
python snake_ai.py
```

---

# Example Gameplay

The AI automatically plays the game and gradually fills the grid until it reaches a perfect score.

Example:

```
Score: 4899 / 4900
AI State: Shortcut (Fast)
```

Eventually the snake enters:

```
Victory Lap (Strict)
```

and finishes the game safely.

---

# Future Improvements

Planned improvements include:

* Multiple AI strategies (A*, BFS, Reinforcement Learning)
* Performance benchmarking
* Visualization of the Hamiltonian path
* Adjustable grid sizes
* AI speed controls
* Statistics dashboard

---

# Authors

Developed as part of an AI/game algorithm project.
