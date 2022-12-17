from collections import defaultdict
import functools

with open("./day10/input.txt") as f:
    lines = f.read().splitlines()

register_x = 1
saved_registers = {}

pc = 0
for line in lines:
    cmd = line.split(' ')

    match cmd[0]:
        case 'noop':
            pc += 1
            saved_registers[pc] = register_x

        case 'addx':
            pc += 1
            saved_registers[pc] = register_x
            pc += 1
            saved_registers[pc] = register_x
            register_x += int(cmd[1])

part1 = sum([ i * saved_registers[i] for i in [20, 60, 100, 140, 180, 220 ] ])
print(f"Part 1: {part1}")

print("Part 2:")
for i, v in saved_registers.items():
    if i % 40 == 0: print()
    if abs(v + 1 - (i % 40)) <= 1:
        print('#', end='')
    else:
        print('.', end='')
