import queue


def adjacent(p):
    x, y, z = p[0], p[1], p[2]
    return [
        (x - 1, y, z),
        (x + 1, y, z),
        (x, y - 1, z),
        (x, y + 1, z),
        (x, y, z - 1),
        (x, y, z + 1),
    ]


def cube_perimeter(cubes):
    p = next(iter(cubes))
    minimums, maximums = list(p), list(p)
    for cube in cubes:
        for i, coord in enumerate(cube):
            minimums[i] = min(minimums[i], coord)
            maximums[i] = max(maximums[i], coord)
    return lambda pos: all(
        [(pos[i] < minimums[i] or pos[i] > maximums[i]) for i in range(3)]
    )


def search_for_perimeter(cubes, pos):
    visited = set()
    visited.add(pos)

    frontier = queue.Queue()
    frontier.put(pos)

    outside_perimeter = cube_perimeter(cubes)

    while not frontier.empty():
        coord = frontier.get()
        if coord in cubes:
            continue
        if outside_perimeter(coord):
            return True
        for next in adjacent(coord):
            if next not in visited:
                visited.add(next)
                frontier.put(next)

    return False


cubes = {}

with open("./day18/input.txt") as f:
    for line in f.read().splitlines():
        [x, y, z] = map(int, line.split(","))
        cubes[(x, y, z)] = True

part1 = sum(
    [sum([1 for coord in adjacent(cube) if coord not in cubes]) for cube in cubes]
)
print(f"Part 1: {part1}")

part2 = sum(
    # Could make this much maintaining by caching negative / positive results
    # between starting positions, but this is plenty fast enough to be run once.
    [
        sum([1 for coord in adjacent(cube) if search_for_perimeter(cubes, coord)])
        for cube in cubes
    ]
)
print(f"Part 2: {part2}")
