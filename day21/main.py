import re
import operator

monkeys = {}

operations = {
    "+": operator.add,
    "-": operator.sub,
    "*": operator.mul,
    "/": operator.floordiv,
}

with open("./day21/input.txt") as f:
    for line in f.read().splitlines():
        x = re.search(r"^([a-z]+): ([0-9]+)$", line)
        if x is not None:
            x = x.groups()
            monkeys[x[0]] = int(x[1])
            continue

        x = re.search(r"^([a-z]+): ([a-z]+) (.) ([a-z]+)$", line).groups()
        monkeys[x[0]] = (x[1], x[2], x[3])


def eval(monkey, part):
    if monkey == "humn" and part == 2:
        raise Exception("humn")
    match monkeys[monkey]:
        case int(m):
            return m
        case (m1, op, m2):
            return operations[op](eval(m1, part), eval(m2, part))


def rev_eval(monkey, target):
    if monkey == "humn":
        return target
    (l, op, r) = monkeys[monkey]
    try:
        left = eval(l, part=2)
        match op:
            case "+":
                new_target = target - left
            case "-":
                new_target = left - target
            case "*":
                new_target = target // left
            case "/":
                new_target = left // target
        return rev_eval(r, new_target)
    except:
        right = eval(r, part=2)
        match op:
            case "+":
                new_target = target - right
            case "-":
                new_target = target + right
            case "*":
                new_target = target // right
            case "/":
                new_target = target * right
        return rev_eval(l, new_target)


def part1():
    return eval("root", part=1)


def part2():
    (left, _, right) = monkeys["root"]
    try:
        return rev_eval(right, eval(left, part=2))
    except:
        return rev_eval(left, eval(right, part=2))


print(f"Part 1: {part1()}")
print(f"Part 2: {part2()}")
