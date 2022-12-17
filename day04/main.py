import re

with open("./day04/input.txt") as f:
    lines = f.read().splitlines()

part1, part2 = 0, 0
for line in lines:
    [x1, x2, y1, y2] = list(map(int, re.search(r'^(\d+)-(\d+),(\d+)-(\d+)$', line).groups()))
    if (x1 <= y1 and x2 >= y2) or (y1 <= x1 and y2 >= x2):
        part1 += 1
    if (y1 >= x1 and y1 <= x2) or (x1 >= y1 and x1 <= y2):
        part2 += 1

print(f"Part 1: {part1}")
print(f"Part 2: {part2}")
