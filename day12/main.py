import queue

with open("./day12/input.txt") as f:
    lines = f.read().splitlines()

start = (0, 0)
max_x, max_y = len(lines[0]) - 1, len(lines) - 1
grid = [[0 for _ in range(max_x + 1)] for _ in range(max_y + 1)]

x, y = 0, 0
for line in lines:
    x = 0
    for c in line:
        if c == "S":
            start = (x, y)
            c = "a"
        if c == "E":
            end = (x, y)
            c = "z"
        grid[y][x] = ord(c) - ord("a")
        x += 1
    y += 1


def flatten(xs):
    [item for sublist in xs for item in sublist]


def get_adj(x, y):
    return list(
        filter(
            (lambda p: p[0] >= 0 and p[0] <= max_x and p[1] >= 0 and p[1] <= max_y),
            [(x, y - 1), (x, y + 1), (x - 1, y), (x + 1, y)],
        )
    )


def find_end(start, stop_condition):
    seen = set()
    seen.add(start)
    frontier = queue.Queue()
    frontier.put((start, 0))

    while True:
        here, n = frontier.get()
        if stop_condition(here):
            return n

        for next in get_adj(here[0], here[1]):
            if (
                next not in seen
                and grid[here[1]][here[0]] - grid[next[1]][next[0]] <= 1
            ):
                seen.add(next)
                frontier.put((next, n + 1))


print(find_end(end, lambda p: p == start))
print(find_end(end, lambda p: grid[p[1]][p[0]] == 0))
