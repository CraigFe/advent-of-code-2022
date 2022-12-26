import math
import sys
from collections import defaultdict

with open("./day24/input.txt") as f:
    lines = f.read().splitlines()

max_x, max_y = len(lines[0]) - 3, len(lines) - 3
initial_blizzards = defaultdict(
    lambda: [],
    {
        (x, y): [cell]
        for y, line in enumerate(lines[1:-1])
        for x, cell in enumerate(line[1:-1])
        if cell != "."
    },
)


def lcm(a, b):
    return (a * b) // math.gcd(a, b)


def advance_blizzards(blizzards):
    def move_blizzard(pos, dir):
        dx, dy = 0, 0
        match dir:
            case ">":
                dx = 1
            case "<":
                dx = -1
            case "^":
                dy = -1
            case "v":
                dy = 1
        return ((pos[0] + dx) % (max_x + 1), (pos[1] + dy) % (max_y + 1))

    result = defaultdict(lambda: [])
    for pos, dirs in blizzards.items():
        for dir in dirs:
            next_pos = move_blizzard(pos, dir)
            result[next_pos].append(dir)
    return result


cycle_time = lcm(max_x + 1, max_y + 1)
blizzards = [defaultdict(lambda: [])] * cycle_time
blizzards[0] = initial_blizzards

for i in range(1, cycle_time):
    blizzards[i] = advance_blizzards(blizzards[i - 1])

assert advance_blizzards(blizzards[-1]) == blizzards[0]

entrance = (0, -1)
exit = (max_x, max_y + 1)


def compute_free_slots(blizzards):
    acc = {
        (x, y)
        for x in range(0, max_x + 1)
        for y in range(0, max_y + 1)
        if len(blizzards[(x, y)]) == 0
    }
    acc.add(entrance)
    acc.add(exit)
    return acc


free_slots = list(map(compute_free_slots, blizzards))


def adjacent(pos):
    to_consider = [
        (pos[0], pos[1] + 1),
        (pos[0], pos[1] - 1),
        (pos[0] - 1, pos[1]),
        (pos[0] + 1, pos[1]),
    ]
    return [
        (x, y)
        for (x, y) in to_consider
        if (x, y) == entrance
        or (x, y) == exit
        or (x >= 0 and y >= 0 and x <= max_x and y <= max_y)
    ]


def solve(pos, target, time, table, best_so_far):
    if pos == target:
        return time  # Done

    if time >= best_so_far:
        return 1_000_000

    key = (pos, time % cycle_time)
    if key in table:
        time_last = table[key]
        if time >= time_last:
            return 1_000_000

    table[key] = time

    adjacents = adjacent(pos) + [pos]  # Allow for wait turn
    frees = free_slots[(time + 1) % cycle_time]
    for next in adjacents:
        if next in frees:
            result = solve(next, target, time + 1, table, best_so_far)
            best_so_far = min(best_so_far, result)
    return best_so_far


sys.setrecursionlimit(1_000_000)
there = solve(entrance, exit, 0, {}, 1_000_000)
print(f"Part 1: {there}")
back_again = solve(exit, entrance, there, {}, 1_000_000)
there_again = solve(entrance, exit, back_again, {}, 1_000_000)
print(f"Part 2: {there_again}")


def print_grid(blizzards, pos):
    print("\n#", end="")
    print(".", end="")
    for _ in range(max_y + 3):
        print("#", end="")
    print("")

    for y in range(max_y + 1):
        print("#", end="")
        for x in range(max_x + 1):
            if (x, y) == pos:
                print("E", end="")
            else:
                bliz = blizzards[(x, y)]
                match len(bliz):
                    case 0:
                        print(".", end="")
                    case 1:
                        print(bliz[0], end="")
                    case l:
                        print(l, end="")
        print("#")

    for _ in range(max_y + 3):
        print("#", end="")
    print(".", end="")
    print("#", end="")
    print("\n")
