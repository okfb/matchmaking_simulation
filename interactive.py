import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button
from matplotlib import animation

from matchmaking import simulation_generator, REGIONS


gen = None
running = False


def start(_=None):
    global gen, running
    join = join_slider.val
    stay = stay_slider.val
    gen = simulation_generator(join_chance=join, stay_chance=stay)
    running = True
    ani.event_source.start()


def pause(_=None):
    global running
    running = False
    ani.event_source.stop()


def update(_):
    if not running or gen is None:
        return queue_bars + match_bars

    t, qdist, mdist, match_regions = next(gen)

    for bar, val in zip(queue_bars, qdist):
        bar.set_height(val)
    ax_queue.set_ylim(0, max(max(qdist), 1) + 1)
    ax_queue.set_title(f"Players in Queue by Region (t={t})")

    if len(match_bars) != len(match_regions):
        ax_matches.clear()
        match_bars[:] = ax_matches.bar(match_regions, mdist)
    else:
        for bar, val in zip(match_bars, mdist):
            bar.set_height(val)
    ax_matches.set_ylim(0, max(max(mdist), 1) + 1)
    ax_matches.set_title("Matches per Region")
    return queue_bars + match_bars


fig, (ax_queue, ax_matches) = plt.subplots(1, 2, figsize=(10, 4))
queue_bars = ax_queue.bar(REGIONS, [0 for _ in REGIONS])
match_bars = ax_matches.bar(REGIONS + ["Cross"], [0] * (len(REGIONS) + 1))
ax_queue.set_ylim(0, 1)
ax_matches.set_ylim(0, 1)

axcolor = "lightgoldenrodyellow"
ax_join = plt.axes([0.2, 0.02, 0.65, 0.03], facecolor=axcolor)
join_slider = Slider(ax_join, "Join Chance", 0.1, 1.0, valinit=0.5)

ax_stay = plt.axes([0.2, 0.06, 0.65, 0.03], facecolor=axcolor)
stay_slider = Slider(ax_stay, "Stay Chance", 0.0, 1.0, valinit=0.5)

start_ax = plt.axes([0.85, 0.85, 0.1, 0.05])
start_btn = Button(start_ax, "Start")
start_btn.on_clicked(start)

pause_ax = plt.axes([0.85, 0.78, 0.1, 0.05])
pause_btn = Button(pause_ax, "Pause")
pause_btn.on_clicked(pause)

ani = animation.FuncAnimation(fig, update, interval=300, blit=False)
plt.show()

