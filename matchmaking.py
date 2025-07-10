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
        self.active_matches: List[Match] = []
        self.completed_matches: List[Match] = []

    def add_player(self, player: Player):
        self.queue.append(player)

    def step(self, current_time: int, stay_chance: float = 0.5, match_duration: int = 5):
        # Finish active matches
        finished = [m for m in self.active_matches if current_time - m.start_time >= match_duration]
        self.active_matches = [m for m in self.active_matches if m not in finished]
        for match in finished:
            self.completed_matches.append(match)
            for player in match.players:
                if random.random() < stay_chance:
                    player.join_time = current_time
                    self.queue.append(player)

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
                    self.active_matches.append(Match([player, candidate], current_time, region))
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
    regions = REGIONS
    elo = int(random.gauss(1500, 200))
    elo = max(800, min(2200, elo))
    level = int(random.gauss(25, 10))
    level = max(1, min(50, level))
    return Player(
        id=pid,
        region=random.choice(regions),
        elo=elo,
        level=level,
        join_time=current_time,
    )


REGIONS = ["NA", "EU", "ASIA"]


def run_simulation(
    steps: int = 100,
    join_chance: float = 0.5,
    stay_chance: float = 0.5,
    match_duration: int = 5,
):
    mm = MatchmakingQueue()
    player_id = 0
    history = []  # Keep queue sizes for visualization
    for t in range(steps):
        if random.random() < join_chance:
            mm.add_player(random_player(player_id, t))
            player_id += 1
        mm.step(t, stay_chance=stay_chance, match_duration=match_duration)
        history.append(len(mm.queue))

    queue_dist = [len([p for p in mm.queue if p.region == r]) for r in REGIONS]
    match_regions = REGIONS + ["Cross"]
    match_dist = [len([m for m in mm.completed_matches if m.region == r]) for r in match_regions]
    return mm, history, queue_dist, match_dist, match_regions


def simulation_generator(
    join_chance: float = 0.5,
    stay_chance: float = 0.5,
    match_duration: int = 5,
):
    """Yield queue and match distributions step by step."""
    mm = MatchmakingQueue()
    player_id = 0
    t = 0
    while True:
        if random.random() < join_chance:
            mm.add_player(random_player(player_id, t))
            player_id += 1
        mm.step(t, stay_chance=stay_chance, match_duration=match_duration)
        qdist = [len([p for p in mm.queue if p.region == r]) for r in REGIONS]
        match_regions = REGIONS + ["Cross"]
        mdist = [len([m for m in mm.completed_matches if m.region == r]) for r in match_regions]
        yield t, qdist, mdist, match_regions
        t += 1


if __name__ == "__main__":
    mm, history, qdist, mdist, _ = run_simulation()
    print(f"Total matches: {len(mm.completed_matches)}")
    print("Queue distribution:", dict(zip(REGIONS, qdist)))
