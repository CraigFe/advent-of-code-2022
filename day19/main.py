import re
from collections import Counter

def parse_blueprint(str):
    groups = re.search(r'^Blueprint .*: Each ore robot costs (\d+) ore. Each clay robot costs (\d+) ore. Each obsidian robot costs (\d+) ore and (\d+) clay. Each geode robot costs (\d+) ore and (\d+) obsidian.$', str).groups()
    groups = list(map(int, groups))
    return {
        "ore": { "ore": groups[0] },
        "clay": { "ore": groups[1] },
        "obsidian": { "ore": groups[2], "clay": groups[3] },
        "geode": { "ore": groups[4], "obsidian": groups[5] }
    }

# Given a blueprint, return the maximum number of each type of robot worth
# building: if we can spend at most N of a particular resource type in a single
# turn, there's no point building more than N robots for it.
def max_worthwhile_delta(blueprint):
    return { k: max([ cost.get(k, 0) for cost in blueprint.values()]) or None for k in blueprint.keys() }

def sub(a, b):
    acc = Counter(a)
    for k, v in b.items():
        acc[k] -= v
        if acc[k] < 0:
            return None, False
    return acc, True

def find_highest_geode_count_aux(turns, blueprint, minute, resources, delta, best_so_far, bots_skipped_last_turn, max_deltas):
    remaining_turns = turns - minute
    if remaining_turns == 0:
        return resources["geode"]

    # If we have three turns to go, the maximum number of additional geodes we
    # could gain from here is `delta + (delta + 1) + (delta + 2)` (under the
    # assumption that we build a geode-cracking robot each turn). In general:
    #   N * delta + N(N-1)//2
    maximum_possible_geodes = resources["geode"] + remaining_turns * delta["geode"] + (remaining_turns * (remaining_turns - 1)) // 2
    if maximum_possible_geodes <= best_so_far:
        return resources["geode"] # No point continuing from here

    # Evaluate moves in which a robot is purchased
    buildable_robots = set()
    if remaining_turns > 1: # No point building anything on the final turn
        # Don't need to consider robots that were buildable last turn – it's
        # strictly better to build them earlier if so
        to_consider = set(blueprint.keys()) - bots_skipped_last_turn

        if remaining_turns == 2:
            # No point building these robots with only one turn after this one:
            # we can't do anything useful with the resource they would generate
            to_consider -= set({"ore", "clay", "obsidian"})

        if remaining_turns == 3:
            # No point building clay robots with oonly two turns after this one:
            # we'd need to build an obsidian robot next turn to make use of the
            # clay, and we only benefit from building geode robots next turn.
            to_consider -= set({"clay"})

        # Since we're pruning paths according to our best solution, it's better
        # to explore more promising moves first. We pick robots preferentially
        # if they're later in the tech tree.
        to_consider = list(to_consider)
        to_consider.sort(key=["geode", "obsidian", "clay", "ore"].index)

        for resource_type in to_consider:
            # Are we already saturated with these robots?
            if max_deltas[resource_type] != None and delta[resource_type] >= max_deltas[resource_type]: continue

            # Do we have enough resources available to build this?
            available, ok = sub(resources, blueprint[resource_type])
            if not ok: continue

            buildable_robots.add(resource_type)
            new_resources = available + delta
            new_delta = delta + Counter({resource_type: 1})
            best_from_here = find_highest_geode_count_aux(turns, blueprint, minute + 1, new_resources, new_delta, best_so_far, set(), max_deltas)
            best_so_far = max(best_so_far, best_from_here)

    # There are robots we can't build here (or we're on the final turn), so it's
    # viable to pass and see what to do on the next turn
    if len(buildable_robots) < len(blueprint.keys()) or remaining_turns == 1:
        best_from_here = find_highest_geode_count_aux(turns, blueprint, minute + 1, resources + delta, delta, best_so_far, buildable_robots, max_deltas)
        best_so_far = max(best_so_far, best_from_here)

    return best_so_far


def find_highest_geode_count(turns, blueprint):
    max_deltas = max_worthwhile_delta(blueprint)
    resources = Counter()
    delta = Counter({"ore": 1}) # We start with one ore bot
    return find_highest_geode_count_aux(turns, blueprint, 0, resources, delta, 0, set(), max_deltas)

with open("./day19/input.txt") as f:
    blueprints = [ parse_blueprint(line) for line in f.read().splitlines() ]

# Part 1
total_quality_level = 0
for i, blueprint in enumerate(blueprints):
    count = find_highest_geode_count(24, blueprint)
    total_quality_level += (i + 1) * count
print(f"Part 1: {total_quality_level}")

# Part 2
product = 1
for blueprint in blueprints[:3]:
    product *= find_highest_geode_count(32, blueprint)
print(f"Part 2: {product}")
