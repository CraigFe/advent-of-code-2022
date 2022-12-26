
def intersperse(xs, sep):
    if len(xs) <= 1:
        return xs
    return [xs[0], sep] + intersperse(xs[1:], sep)


# Test case:
#    *
#  ***
#    **
edge_length = 4
edges = {
    ((0, 1), (0, -1)): ((2, 0), (0, 1)),
    ((2, 0), (0, -1)): ((0, 1), (0, 1)),

    ((1, 1), (0, -1)): ((2, 0), (1, 0)),
    ((2, 0), (-1, 0)): ((1, 1), (0, 1)),

    ((2, 0), (1, 0)): ((3, 2), (-1, 0)),
    ((3, 2), (1, 0)): ((2, 0), (-1, 0)),

    ((2, 1), (1, 0)): ((3, 2), (0, 1)),
    ((3, 2), (-1, 0)): ((3, 2), (-1, 0)),

    ((1, 1), (0, 1)): ((2, 2), (1, 0)),
    ((2, 2), (-1, 0)): ((1, 1), (0, -1)),

    ((0, 1), (0, 1)): ((2, 2), (0, -1)),
    ((2, 2), (0, 1)): ((0, 1), (0, -1)),

    ((3, 2), (0, 1)): ((0, 1), (1, 0)),
    ((0, 1), (-1, 0)): ((3, 2), (0, -1)),
}

# Problem case:
#   **
#   *
#  **
#  * 
#  *
edge_length = 50
edges = {
    ((1, 0), (0, -1)): ((0, 3), (1, 0)),
    ((0, 3), (-1, 0)): ((1, 0), (0, 1)),

    ((2, 0), (0, -1)): ((0, 3), (0, -1)),
    ((0, 3), (0, 1)): ((2, 0), (0, 1)),

    ((2, 0), (1, 0)): ((1, 2), (-1, 0)),
    ((1, 2), (1, 0)): ((2, 0), (-1, 0)),

    ((2, 0), (0, 1)): ((1, 1), (-1, 0)),
    ((1, 1), (1, 0)): ((2, 0), (0, -1)),

    ((1, 2), (0, 1)): ((0, 3), (-1, 0)),
    ((0, 3), (1, 0)): ((1, 2), (0, -1)),

    ((0, 2), (-1, 0)): ((1, 0), (1, 0)),
    ((1, 0), (-1, 0)): ((0, 2), (1, 0)),

    ((0, 2), (0, -1)): ((1, 1), (1, 0)),
    ((1, 1), (-1, 0)): ((0, 2), (0, 1)),
}

# 5 of the edges are in the net itself, leaving 7 implicitly connected (in both directions)
assert len(edges) == 14


def get_connected_position(pos, delta):
    face_position = (pos[0] // edge_length, pos[1] // edge_length)

    # Sanity check: the next move from this position should take us off this face
    face_position_after_move = ((pos[0] + delta[0]) // edge_length, (pos[1] + delta[1]) // edge_length)
    print(f"Getting connected face from {pos}, {delta} – face position {face_position} -> {face_position_after_move}")
    assert face_position != face_position_after_move

    # How many units are we along this face (left to right along delta)?
    match delta:
        case (1, 0): edge_pos = pos[1] % edge_length # facing right
        case (0, -1): edge_pos = pos[0] % edge_length # facing up
        case (-1, 0): edge_pos = (edge_length - 1) - (pos[1] % edge_length) # facing left
        case (0, 1): edge_pos = (edge_length - 1) -  (pos[0] % edge_length) # facing down

    target_face_position, target_delta = edges[(face_position, delta)]

    # Get point that is `edge_pos` many units along the target face (left to right along delta)
    base_x, base_y = (target_face_position[0] * edge_length, target_face_position[1] * edge_length)
    match target_delta:
        case (1, 0): dest = (base_x, base_y + edge_pos) # facing right
        case (0, -1): dest = (base_x + edge_pos, base_y + (edge_length - 1)) # facing up
        case (0, 1): dest = (base_x + (edge_length - 1) - edge_pos, base_y)  # facing down
        case (-1, 0): dest = (base_x + (edge_length - 1), base_y + (edge_length - 1) - edge_pos) # facing left

    # Sanity check: our new position is in the face we expect
    assert (dest[0] // edge_length, dest[1] // edge_length) == target_face_position
    print(f"Result {dest}, {target_delta} – we're {edge_pos} units along the edge")
    return dest, target_delta


def move(map, pos, delta, part):
    x, y = pos[0], pos[1]
    dx, dy = delta[0], delta[1]

    if dx == 0: # Moving in y-direction
        if y + dy >= 0 and y + dy < len(map) and x < len(map[y + dy]) and map[y + dy][x] != ' ':
            return (x, y + dy), delta
        else: 
            # Out of bounds
            if part == 1:
                y_new = (max if dy < 0 else min)([y for (y, row) in enumerate(map) if x < len(row) and row[x] != ' '])
                return (x, y_new), delta
            if part == 2:
                return get_connected_position(pos, delta)
    
    if dy == 0: # Moving in x-direction
        if x + dx >= 0 and x + dx < len(map[y]) and map[y][x + dx] != ' ':
            return (x + dx, y), delta
        else:
            # Out of bounds
            if part == 1:
                x_new = (max if dx < 0 else min)([y for (y, cell) in enumerate(map[y]) if cell != ' '])
                return (x_new, y), delta
            if part == 2:
                return get_connected_position(pos, delta)


def spin(delta, dir):
    match dir:
        case 'L': return (delta[1], -delta[0])
        case 'R': return (-delta[1], delta[0])


def solve(map, instructions):
    pos = (min([ i for i, c in enumerate(map[0]) if c == '.' ]), 0)
    print(pos)
    delta = (1, 0)
    for instruction in instructions:
        match instruction:
            case 'L' | 'R': 
                new_delta = spin(delta, instruction)
                print(f"Rotating from {delta} to {new_delta}")
                delta = new_delta
            case i:
                for _ in range(int(i)):
                    new_pos, new_delta = move(map, pos, delta, part=2)
                    print(f"{new_pos}, {new_delta}")
                    match map[new_pos[1]][new_pos[0]]:
                        case '.': 
                            pos = new_pos
                            delta = new_delta
                        case '#': pass
                        case _: assert False


    row = pos[1] + 1
    column = pos[0] + 1
    facing = None
    match delta:
        case (1, 0): facing = 0
        case (0, 1): facing = 1
        case (-1, 0): facing = 2
        case (0, -1): facing = 3

    return 1000 * row + 4 * column + facing

map = []
instructions = []

with open("./day22/input.txt") as f:
    map_parsed = False
    for line in f.read().splitlines():
        if line == "":
            map_parsed = True
        elif not map_parsed:
            map.append(list(line))
        else:
            instructions = [
                y
                for x in intersperse(line.split("R"), "R")
                for y in intersperse(x.split("L"), "L")
            ]

print(solve(map, instructions))