from collections import Counter


def bounding_box(grid):
    # Get bounding box
    min_x, min_y = 1_000_000, 1_000_000
    max_x, max_y = -1_000_000, -1_000_000
    for (x, y) in grid:
        min_x = min(min_x, x)
        min_y = min(min_y, y)
        max_x = max(max_x, x)
        max_y = max(max_y, y)
    return ((min_x, min_y), (max_x, max_y))


def print_grid(grid):
    ((min_x, min_y), (max_x, max_y)) = bounding_box(grid)
    for y in range(min_y, max_y + 1):
        for x in range(min_x, max_x + 1):
            if (x, y) in grid:
                print("#", end="")
            else:
                print(".", end="")
        print("")


def print_grid_positions(grid):
    s = list(grid)
    s.sort()
    print(s)


def all_adjacent(pos):
    return [
        (pos[0] + dx, pos[1] + dy)
        for dx in [-1, 0, 1]
        for dy in [-1, 0, 1]
        if (dx, dy) != (0, 0)
    ]


def turn(grid, directions):
    # Make proposal stage
    proposals = {}
    for elf in grid:
        proposals[elf] = elf  # Default to not moving
        # If the elf has at least one neighbour, consider moving
        if any([p in grid for p in all_adjacent(elf)]):
            for (dx, dy) in directions:
                destination = (elf[0] + dx, elf[1] + dy)
                deltas = (
                    [(-1, 0), (0, 0), (1, 0)] if dx == 0 else [(0, -1), (0, 0), (0, 1)]
                )
                move_in_direction = not (
                    any(
                        [
                            (destination[0] + dx, destination[1] + dy) in grid
                            for (dx, dy) in deltas
                        ]
                    )
                )
                if move_in_direction:
                    proposals[elf] = destination
                    break

    # Get occurrence counts
    proposal_counts = Counter()
    for cell in proposals.values():
        proposal_counts[cell] += 1

    # Retract any proposed moves that collide
    for elf, proposed in proposals.items():
        if proposal_counts[proposed] > 1:
            proposals[elf] = elf

    return set(proposals.values())


def part1(input_grid):
    directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]  # North, South, West, East
    grid = set(input_grid)
    for _ in range(10):
        grid = turn(grid, directions)
        directions = directions[1:] + [directions[0]]
    ((min_x, min_y), (max_x, max_y)) = bounding_box(grid)
    return sum(
        [
            1
            for x in range(min_x, max_x + 1)
            for y in range(min_y, max_y + 1)
            if (x, y) not in grid
        ]
    )


def part2(input_grid):
    directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]  # North, South, West, East
    grid = set(input_grid)
    i = 1
    while True:
        new_grid = turn(grid, directions)
        if grid == new_grid:
            return i
        grid = new_grid
        directions = directions[1:] + [directions[0]]
        i += 1


input_grid = set()
with open("./day23/input.txt") as f:
    for y, line in enumerate(f.read().splitlines()):
        for x, c in enumerate(list(line)):
            if c == "#":
                input_grid.add((x, y))

print(f"Part 1: {part1(input_grid)}")
print(f"Part 2: {part2(input_grid)}")
