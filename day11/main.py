import itertools
import functools
import re
import math
import operator


def split_by(xs, sep):
    return [
        list(group)
        for is_sep, group in itertools.groupby(xs, lambda x: x == sep)
        if not is_sep
    ]


with open("./day11/input.txt") as f:
    lines = f.read().splitlines()


def parse_monkey(lines):
    starting_items = list(
        map(
            int, re.search(r"^  Starting items: (.*)", lines[1]).groups()[0].split(", ")
        )
    )
    op = parse_operation(lines[2])
    test_denominator = int(
        re.search(r"^  Test: divisible by (\d+)$", lines[3]).groups()[0]
    )
    if_true = int(
        re.search(r"^    If true: throw to monkey (\d+)$", lines[4]).groups()[0]
    )
    if_false = int(
        re.search(r"^    If false: throw to monkey (\d+)$", lines[5]).groups()[0]
    )
    return {
        "items": starting_items,
        "op": op,
        "test_denominator": test_denominator,
        "if_true": if_true,
        "if_false": if_false,
        "items_inspected": 0,
    }


def parse_operation(op):
    groups = re.search(r"^  Operation: new = (.*) ([\*\+]) (.*)$", op).groups()
    op = operator.add if groups[1] == "+" else operator.mul
    return lambda x: op(
        (x if groups[0] == "old" else int(groups[0])),
        (x if groups[2] == "old" else int(groups[2])),
    )


def compute_lcm(a, b):
    return (a * b) // math.gcd(a, b)


def solve(part, rounds):
    monkeys = [parse_monkey(x) for x in split_by(lines, "")]
    lcm = functools.reduce(compute_lcm, map(lambda x: x["test_denominator"], monkeys))
    for _ in range(rounds):
        for monkey in monkeys:
            for item in monkey["items"]:
                monkey["items_inspected"] += 1
                if part == 1:
                    worry_level = monkey["op"](item) // 3
                else:
                    worry_level = monkey["op"](item) % lcm
                test = worry_level % monkey["test_denominator"] == 0
                next_monkey = monkey["if_true"] if test else monkey["if_false"]
                monkeys[next_monkey]["items"].append(worry_level)
            monkey["items"] = []

    inspect_count = [monkey["items_inspected"] for monkey in monkeys]
    inspect_count.sort()
    return inspect_count[-1] * inspect_count[-2]


print(f"Part 1: {solve(1, 20)}")
print(f"Part 2: {solve(2, 10_000)}")
