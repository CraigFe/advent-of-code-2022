from collections import defaultdict

with open("./day07/input.txt") as f:
    lines = [x.split() for x in f.read().splitlines()[1:]]

cwd = []
relation = defaultdict(set)
sizes = defaultdict(int)


def track_relationship(parent, child):
    parent_path = "/".join([""] + cwd)
    child_path = "/".join([""] + cwd + [child])
    relation[parent_path].add(child_path)


for line in lines:
    match line[0]:
        case "$":
            if line[1] == "cd":
                if line[2] == "..":
                    del cwd[-1:]
                else:
                    track_relationship(cwd, line[2])
                    cwd.append(line[2])

        case "dir":
            track_relationship(cwd, line[1])

        case _:
            cwd_path = "/".join([""] + cwd)
            sizes[cwd_path] += int(line[0])

# Iterate over all parents, deepest first
parents = list(relation.keys())
parents.sort(key=(lambda x: x.count("/")), reverse=True)
for parent in parents:
    sizes[parent] += sum([sizes[child] for child in relation.get(parent, [])])

part1 = sum([x for x in sizes.values() if x < 100_000])
print(f"Part 1: {part1}")

unused_space = 70000000 - sizes[""]
space_to_free = 30000000 - unused_space
directories = list(sizes.items())
directories.sort(key=(lambda x: x[1]), reverse=True)
part2 = [size for _, size in directories if size >= space_to_free][-1]
print(f"Part 2: {part2}")
