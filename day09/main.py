import math

with open("./day09/input.txt") as f:
    lines = f.read().splitlines()


def direction_to_delta(c):
    match c:
        case "L":
            return (-1, 0)
        case "R":
            return (1, 0)
        case "U":
            return (0, 1)
        case "D":
            return (0, -1)


def divide_and_round_away_from_zero(x, y):
    return (abs(x) + 1) // y * math.copysign(1, x)


def move_tail_towards_head(tail, head):
    if abs(head[0] - tail[0]) <= 1 and abs(head[1] - tail[1]) <= 1:
        return tail
    dx = divide_and_round_away_from_zero(head[0] - tail[0], 2)
    dy = divide_and_round_away_from_zero(head[1] - tail[1], 2)
    return (tail[0] + dx, tail[1] + dy)


def get_position_count(rope_size):
    positions = set()
    positions.add((0, 0))
    rope = [(0, 0) for _ in range(rope_size)]

    for line in lines:
        direction, count = line.split(" ")
        dx, dy = direction_to_delta(direction)
        for _ in range(int(count)):
            head_x, head_y = rope[0]
            rope[0] = (head_x + dx, head_y + dy)
            for i in range(1, len(rope)):
                rope[i] = move_tail_towards_head(rope[i], rope[i - 1])
            positions.add(rope[-1])

    return len(positions)


print(f"Part 1: {get_position_count(2)}")
print(f"Part 2: {get_position_count(10)}")
