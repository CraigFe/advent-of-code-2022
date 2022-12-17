import re
from collections import defaultdict

with open("./day15/input.txt") as f:
    lines = f.read().splitlines()

space=defaultdict(lambda: defaultdict(lambda: None))

def part1():
    for line in lines:
        [ x1, y1, x2, y2 ] = map(int, re.search(r'^Sensor at x=(.*), y=(.*): closest beacon is at x=(.*), y=(.*)$', line).groups())

        space[x1][y1] = 'S'
        space[x2][y2] = 'B'

        max_dist = abs(y2 - y1) + abs(x2 - x1)
        for x in range(x1 - max_dist, x1 + max_dist + 1):
            max_y_dist = max_dist - abs(x1 - x)
            if y1 - max_y_dist <= 2_000_000 and 2_000_000 <= y1 + max_y_dist:
                y = 2_000_000
                if space[x][y] == None:
                    space[x][y] = '#'

    part1 = sum([ 1 for col in space.values() if col[2_000_0000] == '#'])
    print(f"Part 1: {part1}")

            # for y in range(y1 - max_y_dist, y1 + max_y_dist + 1):
            #     if space[x][y] == None:
            #         space[x][y] = '#'

space_boundary = 4_000_000
# space_boundary = 20

sensor_beacon_pairs = set()
points_to_check = set()
for line in lines:
    [ x1, y1, x2, y2 ] = map(int, re.search(r'^Sensor at x=(.*), y=(.*): closest beacon is at x=(.*), y=(.*)$', line).groups())
    sensor_beacon_pairs.add(((x1, y1), (x2, y2)))

    radius = abs(y2 - y1) + abs(x2 - x1) + 1
    for x in range(x1 - radius, x1 + radius + 1):
        if x >= 0 and x <= space_boundary:
            y_dist = radius - abs(x1 - x)
            if y1 + y_dist >= 0 and y1 + y_dist < space_boundary:
                points_to_check.add((x, y1 + y_dist))
            if y1 - y_dist >= 0 and y1 - y_dist < space_boundary:
                points_to_check.add((x, y1 - y_dist))

def distance(src, target):
    return abs(target[0] - src[0]) + abs(target[1] - src[1])

def check_in_range(point):
    for (sensor, beacon) in sensor_beacon_pairs:
        if distance(sensor, point) <= distance(sensor, beacon):
            return True
    return False

points_count = len(points_to_check)
def part2():
    i = 0
    for point in points_to_check:
        if i % 10_000 == 0:
            print(f"{i} / {points_count}: {point}")
        i += 1
        if not check_in_range(point):
            return point[0] * 4_000_000 + point[1]

print(f"Part 2: {part2()}")
