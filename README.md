# Signal Tower

A tower defense game built with Python and Pygame, made to practice low-level system design and object-oriented programming.

Enemies travel along a winding path toward the end of the map. Build towers on the pads next to the path to destroy them before they get through. Every enemy that reaches the end costs you health. Lose all your health and the game is over. The game gets harder the longer you survive enemies spawn more often and move faster.

All graphics are simple shapes drawn with Pygame, so no image files are needed.


# Showcase:



## Requirements

- **Python 3.10 or newer** (the game uses `itertools.pairwise`, which was added in 3.10)
- **Pygame** (listed in `requirements.txt`)

Check your Python version with:

```bash
python --version
```

On macOS or Linux, you may need to use `python3` instead of `python` in every command below.

## How to run

1. **Download the project.** Clone it with Git:
   ```bash
   git clone https://github.com/jtsui23-code/signal_tower.git
   cd signal_tower
   ```
   Or download the ZIP from GitHub, unzip it, and open a terminal in that folder.

2. **(Optional) Create a virtual environment** so Pygame installs only for this project:
   ```bash
   python -m venv venv
   ```
   Then activate it:
   - Windows: `venv\Scripts\activate`
   - macOS/Linux: `source venv/bin/activate`

3. **Install the dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Start the game:**
   ```bash
   python Game.py
   ```

## How to play

| Control | Action |
|---|---|
| **Enter** | Start the game (also restarts after a game over) |
| **1** | Select the Basic Tower |
| **2** | Select the Super Tower |
| **Left click** on a pad | Build the selected tower there (if you have enough coins) |
| **Close the window** | Quit |

- Gray squares are **build pads**. Each pad can hold one tower.
- The ring around each tower shows its **range**. Towers automatically damage every enemy inside their range.
- You earn **1 coin** for every enemy you destroy.
- The top of the screen shows your health, your coins, and which tower is selected.

### Towers

| Tower | Cost | Range | Fires every | Damage | Special |
|---|---|---|---|---|---|
| Basic (teal) | 3 | 130 | 0.4 s | 0.5 | Fast, steady damage |
| Super (purple) | 5 | 150 | 1.2 s | 2 | 25% chance of a critical hit for double damage |

### Enemies

| Enemy | Health | Speed | Armor | Health lost if it gets through |
|---|---|---|---|---|
| Basic (red circle) | 4 | 65 | None | 1 |
| Super (green oval) | 7 | 75 | 3 | 2 |

Armor reduces each hit by its value, but every hit always does at least 1 damage.

You start with **30 health** and **3 coins**. Difficulty increases every 7 seconds: enemies spawn more often and move faster, up to a set limit.

## Project structure

| File | Purpose |
|---|---|
| `Game.py` | Entry point. Runs the game loop, screens, spawning, building, and drawing. |
| `Path.py` | The enemy route as a list of waypoints. Converts "distance traveled" into an (x, y) position. |
| `Enemy.py` | `Enemy` and `SuperEnemy`. Movement and taking damage, including armor. |
| `Tower.py` | `Tower` and `SuperTower`. Cooldowns, range checks, and firing. |
| `Class_Design.txt` | The class design written before coding. |
| `requirements.txt` | Python dependencies. |

## Design notes

- **Each class owns its own data and rules.** Enemies only track how far they've traveled, and `Path` turns that into a screen position, so enemies never need to know about corners.
- **Inheritance changes behavior, not just numbers.** `SuperEnemy` overrides `takeDMG` to apply armor, and `SuperTower` overrides `fire` to add critical hits. `Game` calls the same methods on every tower and enemy without checking their type.
- **Tower cost is a class attribute,** so `Game` can check the price of the selected tower type before creating one.
- **All movement and timers use delta time (`dt`)**, so the game runs at the same speed on any computer.