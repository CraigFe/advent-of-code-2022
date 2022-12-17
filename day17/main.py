from collections import defaultdict

rocks = [
    [["#", "#", "#", "#"]],
    [[None, "#", None], ["#", "#", "#"], [None, "#", None]],
    [[None, None, "#"], [None, None, "#"], ["#", "#", "#"]],
    [["#"], ["#"], ["#"], ["#"]],
    [["#", "#"], ["#", "#"]],
]


def collides(chamber, rock, x, y):
    if x == -1:
        return True  # colliding with left wall
    for rock_y, row in enumerate(rock):
        if y - rock_y == -1:
            return True  # colliding with ground
        for rock_x, cell in enumerate(row):
            if x + rock_x >= 7:
                return True  # colliding with right wall
            if cell == "#":
                if chamber[y - rock_y][x + rock_x] == "#":
                    return True  # colliding with a rock
    return False


def add_to_chamber(chamber, rock, x, y):
    if collides(chamber, rock, x, y):
        raise Exception("Can't add a rock that would collide")
    for rock_y, row in enumerate(rock):
        for rock_x, cell in enumerate(row):
            if cell == "#":
                chamber[y - rock_y][x + rock_x] = "#"


def print_chamber(chamber):
    max_y = max(chamber.keys(), default=0) + 2
    for y in range(max_y, -1, -1):
        print("|", end="")
        for x in chamber[y]:
            if x == None:
                print(".", end="")
            else:
                print("#", end="")
        print("|")
    print("+-------+")


def max_y_in_chamber(chamber):
    for row in range(max(chamber.keys(), default=0), -1, -1):
        if "#" in chamber[row]:
            return row
    return -1


# chamber_shape is a rough approximation of the shape of the _top_ frontier of
# the chamber using column heights; the idea being that chambers with equal
# shapes behave equally with respect to subsequent rock drops (except for their
# max height).
#
# This isn't exactly correct: the shape accounts only for the height of the top
# rock in each column and not any inlets beneath those, but it seems to be
# enough to pass the test case given. A fully correct shape implementation would
# account for the entire top surface of the chamber.
def chamber_shape(chamber):
    y_max = max_y_in_chamber(chamber)
    if y_max == -1:
        return "floor"

    shape = [None] * 7
    for i in range(7):
        depth = 0
        y = y_max
        while True:
            if y == -1:
                return y_max + 1
            if chamber[y][i] == "#":
                break
            y -= 1
            depth += 1
        shape[i] = str(depth)
    return "-".join(shape)


def add_rock_to_chamber(chamber, rock, x, y, wind_directions, wind_time):

    while True:
        # Move with the wind
        match wind_directions[wind_time % len(wind_directions)]:
            case ">":
                # First check that the rock won't be colliding with anything
                if not collides(chamber, rock, x + 1, y):
                    x += 1
            case "<":
                if not collides(chamber, rock, x - 1, y):
                    x -= 1
            case x:
                raise Exception("Unexpected direction: " + x)
        wind_time += 1
        if collides(chamber, rock, x, y - 1):
            add_to_chamber(chamber, rock, x, y)
            break
        y -= 1

    return wind_time


def solve(wind_directions, total_rocks_to_place):
    chamber = defaultdict(lambda: [None] * 7)
    wind_time = 0
    rocks_placed = 0  # number of rocks placed
    max_y_off = 0  # y-height gained via interpolating cycles forwards in time
    shapes_seen = defaultdict(
        lambda: {}
    )  # (rock, wind) -> shape -> (rocks_placed, max_height)

    while rocks_placed < total_rocks_to_place:
        rock_index = rocks_placed % len(rocks)
        wind_index = wind_time % len(wind_directions)
        shape = chamber_shape(chamber)
        max_y = max_y_in_chamber(chamber)

        # Trick to spot cycles in the shape of the chamber:
        #
        # If we've seen this "shape" of the top of the chamber before (while placing
        # the same rock and with the same wind cycle), then fast-forward through as
        # many of these cycles as possible before reaching our target number of
        # rocks placed
        if shape in shapes_seen[(rock_index, wind_index)]:
            rock, max_y_prev = shapes_seen[(rock_index, wind_index)][shape]

            rocks_in_cycle = rocks_placed - rock
            y_height_in_cycle = max_y - max_y_prev

            remaining_rocks_to_place = total_rocks_to_place - rocks_placed
            cycles = remaining_rocks_to_place // rocks_in_cycle

            rocks_placed += cycles * rocks_in_cycle
            max_y_off += cycles * y_height_in_cycle

            shapes_seen = defaultdict(lambda: {})  # We only need to do this once

        shapes_seen[(rock_index, wind_index)][shape] = (rocks_placed, max_y)

        rock = rocks[rock_index % len(rocks)]

        # Each rock appears so that its left edge is two units away from the left
        # wall and its bottom edge is three units above the highest rock in the room
        # (or the floor, if there isn't one).
        x = 2
        y = len(rock) + max_y + 3
        wind_time = add_rock_to_chamber(chamber, rock, x, y, wind_directions, wind_time)

        rocks_placed += 1

    return max_y_in_chamber(chamber) + 1 + max_y_off


with open("./day17/input.txt") as f:
    wind_directions = f.read().splitlines()[0]

print(f"Part 1: {solve(wind_directions, 2022)}")
print(f"Part 2: {solve(wind_directions, 1000000000000)}")
