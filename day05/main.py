import re

with open("./day05/input.txt") as f:
    lines = f.read().splitlines()

empty = lines.index('')
stacks, moves = lines[0:empty-1], lines[empty+1:]

numTowers = len(stacks[0]) // 4 + 1
bottomRow = len(stacks) - 1
towers = [[] for _ in range(0, numTowers)]

for col in range(0, numTowers):
    for y in range(bottomRow, -1, -1):
        elt = stacks[y][4*col+1]
        if elt != " ":
            towers[col].append(elt)

for move in moves:
    [ count, source, target ] = map(int, re.search(r'move (\d+) from (\d+) to (\d+)', move).groups())
    source, target = source - 1, target - 1 # One-based indexing

    # toMove = towers[source][:-count-1:-1] # part 1
    toMove = towers[source][-count:]        # part 2
    del towers[source][-count:]
    towers[target].extend(toMove)

print("".join([ tower[-1] for tower in towers ]))
