with open("./day08/input.txt") as f:
    lines = f.read().splitlines()


forest = [list(map(int, row)) for row in lines]
max_y, max_x = len(forest) - 1, len(forest[0]) - 1


def is_visible(y, x):
    return (
        is_visible_with_delta(forest[y][x], y, x, -1, 0)
        or is_visible_with_delta(forest[y][x], y, x, 1, 0)
        or is_visible_with_delta(forest[y][x], y, x, 0, -1)
        or is_visible_with_delta(forest[y][x], y, x, 0, 1)
    )


def is_visible_with_delta(size, y, x, dy, dx):
    if y == 0 or y == max_y or x == 0 or x == max_x:
        return True
    return size > forest[y + dy][x + dx] and is_visible_with_delta(
        size, y + dy, x + dx, dy, dx
    )


part1 = sum(1 for y in range(max_y + 1) for x in range(max_x + 1) if is_visible(y, x))
print(f"Part 1: {part1}")


def viewing_distance_with_delta(size, y, x, dy, dx):
    if y + dy > max_y or y + dy < 0 or x + dx > max_x or x + dx < 0:
        return 0
    if forest[y + dy][x + dx] >= size:
        return 1
    return 1 + viewing_distance_with_delta(size, y + dy, x + dx, dy, dx)


def scenic_score(y, x):
    return (
        viewing_distance_with_delta(forest[y][x], y, x, -1, 0)
        * viewing_distance_with_delta(forest[y][x], y, x, 1, 0)
        * viewing_distance_with_delta(forest[y][x], y, x, 0, -1)
        * viewing_distance_with_delta(forest[y][x], y, x, 0, 1)
    )


part2 = max([scenic_score(y, x) for x in range(max_x + 1) for y in range(max_y + 1)])
print(f"Part 2: {part2}")
