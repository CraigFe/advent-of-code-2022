from collections import defaultdict
import math

# This one turned into a real mess
#
# At first didn't realise that the y axis is "inverted" so there's some nonsense
# to compensate for that, but this interacts poorly with then needing to put a
# floor in the cave. It works – praise `defaultdict`.

with open("./day14/input.txt") as f:
    lines = f.read().splitlines()

cave = defaultdict(lambda: ["#"])


def mark(pos, typ):
    x, y = pos
    if len(cave[x]) <= y:
        cave[x] += [None] * (y - len(cave[x]) + 1)
    cave[x][y] = typ


# get the largest 'y' value to make our base
max_y = max(
    [
        segment[1]
        for line in lines
        for segment in [
            tuple(map(int, coord.split(","))) for coord in line.split(" -> ")
        ]
    ]
)

for line in lines:
    segments = [tuple(map(int, x.split(","))) for x in line.split(" -> ")]
    segments = list(map(lambda p: (p[0], max_y - p[1] + 2), segments))  # invert y axis

    cursor = segments[0]
    mark(cursor, "#")
    for segment in segments[1:]:
        while cursor != segment:
            cursor = (
                cursor[0]
                + (
                    int(math.copysign(1, segment[0] - cursor[0]))
                    if segment[0] != cursor[0]
                    else 0
                ),
                cursor[1]
                + (
                    int(math.copysign(1, segment[1] - cursor[1]))
                    if segment[1] != cursor[1]
                    else 0
                ),
            )
            mark(cursor, "#")


def index_cave(x, y):
    if y == 0:
        return "#"  # floor
    return cave[x][y] if y < len(cave[x]) else None


def find_position(x, y):
    if cave[x] == [] or all(cell == None for cell in cave[x][:y]):
        return None
    if index_cave(x, y - 1) == None:
        return find_position(x, y - 1)
    if index_cave(x - 1, y - 1) == None:
        return find_position(x - 1, min(y - 1, len(cave[x - 1])))
    if index_cave(x + 1, y - 1) == None:
        return find_position(x + 1, min(y - 1, len(cave[x + 1])))
    return (x, y)


def add_sand():
    sand_added = 0
    stop_point = (500, max_y + 2)  # +2 to account for our floor
    while True:
        next_pos = find_position(500, len(cave[500]))
        if next_pos == None or next_pos == stop_point:
            return sand_added
        mark(next_pos, "o")
        sand_added += 1


def print_grid():
    min_x, max_x = min(cave.keys()), max(cave.keys())
    max_y = max(map(len, cave.values())) - 1

    for y in range(max_y, -1, -1):
        for x in range(min_x, max_x + 1):
            cell = index_cave(x, y)
            if cell == None:
                print(".", end="")
            else:
                print(cell, end="")
        print()


print(add_sand() + 1)
print_grid()
