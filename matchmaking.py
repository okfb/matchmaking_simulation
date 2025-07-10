import random
from dataclasses import dataclass, field
from typing import List


@dataclass
class Player:
    id: int
    region: str
    elo: int
    level: int
    join_time: int
    matched: bool = field(default=False, compare=False)


@dataclass
class Match:
    players: List[Player]
    start_time: int
    region: str


class MatchmakingQueue:
    def __init__(self):
        self.queue: List[Player] = []
        self.matches: List[Match] = []

    def add_player(self, player: Player):
        self.queue.append(player)

    def step(self, current_time: int):
        # Sort by join time to give priority to older players
        self.queue.sort(key=lambda p: p.join_time)
        matched_ids = set()
        for i, player in enumerate(self.queue):
            if player.id in matched_ids:
                continue
            for j in range(i + 1, len(self.queue)):
                candidate = self.queue[j]
                if candidate.id in matched_ids:
                    continue
                if self.can_match(player, candidate, current_time):
                    matched_ids.add(player.id)
                    matched_ids.add(candidate.id)
                    region = player.region if player.region == candidate.region else "Cross"
                    self.matches.append(Match([player, candidate], current_time, region))
                    break
        # Remove matched players from queue
        self.queue = [p for p in self.queue if p.id not in matched_ids]

    @staticmethod
    def can_match(p1: Player, p2: Player, current_time: int) -> bool:
        # Region check with expansion after 30s
        if p1.region != p2.region:
            if (current_time - p1.join_time < 30) or (current_time - p2.join_time < 30):
                return False
        # Calculate dynamic tolerances based on time waiting
        t1 = current_time - p1.join_time
        t2 = current_time - p2.join_time
        elo_tol = 50 + max(t1, t2) * 5
        lvl_tol = 2 + max(t1, t2) * 0.1
        return abs(p1.elo - p2.elo) <= elo_tol and abs(p1.level - p2.level) <= lvl_tol


def random_player(pid: int, current_time: int) -> Player:
    regions = ["NA", "EU", "ASIA"]
    return Player(
        id=pid,
        region=random.choice(regions),
        elo=random.randint(1000, 2000),
        level=random.randint(1, 50),
        join_time=current_time,
    )


REGIONS = ["NA", "EU", "ASIA"]


def run_simulation(steps: int = 100, join_chance: float = 0.5):
    mm = MatchmakingQueue()
    player_id = 0
    history = []  # Keep queue sizes for visualization
    for t in range(steps):
        if random.random() < join_chance:
            mm.add_player(random_player(player_id, t))
            player_id += 1
        mm.step(t)
        history.append(len(mm.queue))

    queue_dist = [len([p for p in mm.queue if p.region == r]) for r in REGIONS]
    match_regions = REGIONS + ["Cross"]
    match_dist = [len([m for m in mm.matches if m.region == r]) for r in match_regions]
    return mm, history, queue_dist, match_dist, match_regions


if __name__ == "__main__":
    mm, history, qdist, mdist, _ = run_simulation()
    print(f"Total matches: {len(mm.matches)}")
    print("Queue distribution:", dict(zip(REGIONS, qdist)))
