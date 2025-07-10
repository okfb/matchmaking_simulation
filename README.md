# Matchmaking Simulation

This project demonstrates a simple matchmaking system for an online game.
Players are queued and matched according to region, ELO rating, level and
time spent waiting.

## Usage

Run a basic simulation:

```bash
python matchmaking.py
```

Generate a visualization of queue size over time (requires matplotlib):

```bash
python visualize.py
```

The script will output `queue_size.png` with a plot of the queue length at
each timestep.

### Interactive Demo

To experiment with different parameters interactively, launch:

```bash
python interactive.py
```

A window will open with sliders for the number of steps and player join chance.
Use the **Stay Chance** slider to control the probability that players queue
for another match after finishing one. Press **Run** to update the charts
showing how many players remain in the queue and how many matches are created
per region.

### Building an Executable

If you have `pyinstaller` installed you can build a standalone Windows binary:

```bash
pip install pyinstaller
pyinstaller --onefile interactive.py
```

The resulting executable will be placed in the `dist` folder. Cross–compiling
from Linux may require additional setup.
