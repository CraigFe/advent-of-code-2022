#!/usr/bin/env python3
import itertools


def split_by(xs, sep):
    return [
        list(group)
        for is_sep, group in itertools.groupby(xs, lambda x: x == sep)
        if not is_sep
    ]


def compute_sum(lines):
    return sum(map(int, lines))


with open("./day01/input.txt") as f:
    line_chunks = split_by(f.read().splitlines(), "")

    elves = list(map(compute_sum, line_chunks))
    elves.sort()

    print(f"Part 1: {elves[-1]}")
    print(f"Part 2: {sum(elves[-3:])}")
