import itertools
import functools


def split_by(xs, sep):
    return [
        list(group)
        for is_sep, group in itertools.groupby(xs, lambda x: x == sep)
        if not is_sep
    ]


with open("./day13/input.txt") as f:
    lines = split_by(f.read().splitlines(), "")


def compare_packets(a, b):
    match a, b:
        case int(a), int(b): return (a > b) - (a < b)  # cmp
        case int(a), list(b): return compare_packets([a], b)
        case list(a), int(b): return compare_packets(a, [b])
        case list(a), list(b):
            if a == []: return -1
            if b == []: return 1
            head = compare_packets(a[0], b[0])
            if head != 0: return head
            return compare_packets(a[1:], b[1:])


packet_pairs = [(eval(a), eval(b)) for (a, b) in lines]
part1 = sum(
    [i + 1 for i, [a, b] in enumerate(packet_pairs) if compare_packets(a, b) < 0]
)
print(f"Part 1: {part1}")

div_1, div_2 = [[2]], [[6]]
all_packets = [x for y in packet_pairs for x in y] + [div_1, div_2]
all_packets.sort(key=functools.cmp_to_key(compare_packets))
part2 = (all_packets.index(div_1) + 1) * (all_packets.index(div_2) + 1)
print(f"Part 2: {part2}")
