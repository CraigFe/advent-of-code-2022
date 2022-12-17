import re
from collections import defaultdict
from typing import Dict, List

with open("./day16/input.txt") as f:
    lines = f.read().splitlines()

tunnels: Dict[str, List[str]] = defaultdict(list)
flow_rates: Dict[str, int] = {}

for line in lines:
    groups = re.search(
        r"^Valve (.*) has flow rate=(\d+); tunnels? leads? to valves? (.*)$", line
    ).groups()
    valve = groups[0]
    flow_rates[valve] = int(groups[1])
    for tunnel in groups[2].split(", "):
        tunnels[valve].append(tunnel)


def dijkstra(graph: Dict[str, List[str]], source: str) -> Dict[str, int]:
    queue = list(graph.keys())
    dist = {v: 999999 for v in graph}
    dist[source] = 0
    while queue:
        u = min(queue, key=dist.get)
        queue.remove(u)
        for v in graph[u]:
            alt = dist[u] + 1
            if alt < dist[v]:
                dist[v] = alt
    return dist


distances: Dict[str, Dict[str, int]] = {}
for valve in flow_rates.keys():
    if valve == "AA" or flow_rates[valve] > 0:
        distances[valve] = {
            k: v
            for k, v in dijkstra(tunnels, valve).items()
            if flow_rates[k] > 1
            and k != valve  # don't care about going to tunnels that have no flow
        }

# Depth-first search
def solve(minute, pos, unopened, pressure_released):
    if unopened == []:
        return pressure_released  # Nothing else to do
    best_so_far = pressure_released
    for next in unopened:
        minutes_from_here = minute + distances[pos][next] + 1
        if minutes_from_here >= 30:
            continue  # Can't do anything useful
        pressure_released_now = (
            pressure_released + (30 - minutes_from_here) * flow_rates[next]
        )
        unopened_now = list(filter(lambda x: x != next, unopened))
        from_here = solve(minutes_from_here, next, unopened_now, pressure_released_now)
        best_so_far = max(best_so_far, from_here)
    return best_so_far


unopened = list(filter(lambda x: x != "AA", distances.keys()))
part1 = solve(0, "AA", unopened, 0)
print(f"Part 1: {part1}")


def partition(xs):
    def all_partitions(xs):
        if xs == []:
            return [([], [])]
        sub_partitions = all_partitions(xs[1:])
        return list(map(lambda p: (p[0] + [xs[0]], p[1]), sub_partitions)) + list(
            map(lambda p: (p[0], p[1] + [xs[0]]), sub_partitions)
        )

    return list(
        filter(
            lambda p: p[0] != [] and p[1] != [] and len(p[0]) >= len(p[1]),
            all_partitions(xs),
        )
    )


partitions = partition(list(filter(lambda x: x != "AA", distances.keys())))
part2 = max(
    [solve(4, "AA", split[0], 0) + solve(4, "AA", split[1], 0) for split in partitions]
)
print(f"Part 2: {part2}")
