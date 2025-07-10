import matplotlib.pyplot as plt
from matchmaking import run_simulation


if __name__ == "__main__":
    _, history, _, _, _ = run_simulation(steps=200)

    plt.figure(figsize=(8, 4))
    plt.plot(history, label="Players in queue")
    plt.xlabel("Time step")
    plt.ylabel("Queue size")
    plt.title("Matchmaking Queue Size Over Time")
    plt.legend()
    plt.tight_layout()
    plt.savefig("queue_size.png")
    print("Saved queue_size.png")
