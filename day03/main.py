import functools


def item_priority(x):
    if x.islower():
        return ord(x) - ord("a") + 1
    else:
        return ord(x) - ord("A") + 27


def priority_of_duplicated_item(bag):
    compartment_size = len(bag) // 2
    duplicated = set(bag[:compartment_size]).intersection(bag[compartment_size:])
    return item_priority(duplicated.pop())


def priority_of_group_item(group):
    duplicated = functools.reduce(lambda a, b: a.intersection(b), map(set, group))
    return item_priority(duplicated.pop())


with open("./day03/input.txt") as f:
    lines = f.read().splitlines()

    part1 = sum(map(priority_of_duplicated_item, lines))
    print(f"Part 1: {part1}")

    groups = []
    for i in range(0, len(lines), 3):
        groups.append(lines[i : i + 3])
    part2 = sum(map(priority_of_group_item, groups))
    print(f"Part 2: {part2}")
