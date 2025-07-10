import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button
from matchmaking import run_simulation, REGIONS


def run_and_update(_=None):
    steps = int(steps_slider.val)
    join_chance = join_slider.val
    _, _, qdist, mdist, match_regions = run_simulation(steps, join_chance)

    for bar, val in zip(queue_bars, qdist):
        bar.set_height(val)
    ax_queue.set_ylim(0, max(max(qdist), 1) + 1)

    ax_matches.clear()
    global match_bars
    match_bars = ax_matches.bar(match_regions, mdist)
    ax_matches.set_title("Matches per Region")
    ax_matches.set_ylim(0, max(max(mdist), 1) + 1)
    fig.canvas.draw_idle()

# initial simulation
_, _, qdist, mdist, match_regions = run_simulation()

fig, (ax_queue, ax_matches) = plt.subplots(1, 2, figsize=(10, 4))
queue_bars = ax_queue.bar(REGIONS, qdist)
ax_queue.set_title("Players in Queue by Region")
ax_queue.set_ylim(0, max(max(qdist), 1) + 1)

match_bars = ax_matches.bar(match_regions, mdist)
ax_matches.set_title("Matches per Region")
ax_matches.set_ylim(0, max(max(mdist), 1) + 1)

axcolor = 'lightgoldenrodyellow'
ax_join = plt.axes([0.2, 0.02, 0.65, 0.03], facecolor=axcolor)
join_slider = Slider(ax_join, 'Join Chance', 0.1, 1.0, valinit=0.5)

ax_steps = plt.axes([0.2, 0.06, 0.65, 0.03], facecolor=axcolor)
steps_slider = Slider(ax_steps, 'Steps', 50, 200, valinit=100, valfmt='%0.0f')

join_slider.on_changed(run_and_update)
steps_slider.on_changed(run_and_update)

run_button_ax = plt.axes([0.85, 0.85, 0.1, 0.05])
run_button = Button(run_button_ax, 'Run')
run_button.on_clicked(run_and_update)

plt.show()
