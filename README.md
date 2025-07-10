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

To see the simulation evolve in real time, launch:

```bash
python interactive.py
```

A window appears with sliders for join and stay probabilities. Press **Start**
to begin an animated run of the simulation. The plots update every few hundred
milliseconds, showing how players move through the queue and how many matches
are formed per region. Use **Pause** to stop the animation and adjust the
sliders; press **Start** again to restart with the new settings.

### Building an Executable

If you have `pyinstaller` installed you can build a standalone Windows binary:

```bash
pip install pyinstaller
pyinstaller --onefile interactive.py
```

The resulting executable will be placed in the `dist` folder. Cross–compiling
from Linux may require additional setup.
