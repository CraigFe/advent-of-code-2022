with open("./day20/input.txt") as f:
    file = [int(line) for line in f.read().splitlines()]


def print_list(list, inv_reorder_map):
    print("[" + ", ".join([str(list[v]) for v in inv_reorder_map]) + "]")


def move(reorder_map, inv_reorder_map, original_idx, delta):
    if delta % len(reorder_map) == 0:
        return
    delta = delta % (len(reorder_map) - 1)

    # I find the semantics of "moving" an element in this puzzle a bit odd: the
    # number of displaced elements depends on whether we wrap around or not. In
    # the end this doesn't actually matter for the puzzle result, but the
    # implementation is more complex in order to exactly match the example given
    # in the question.
    #
    #  0 X 1 2 3 4 5 6 7   (X = 3)     0 1 2 3 4 X 5 6 7   (X = -3)
    #     / / /                             \ \ \
    #  0 1 2 3 X 4 5 6 7               0 1 X 2 3 4 5 6 7
    #
    #  0 1 2 3 4 5 6 X 7   (X = 3)     0 X 1 2 3 4 5 6 7   (X = -3)
    #       \ \ \ \ \                     / / / / /
    #  0 1 X 2 3 4 5 6 7               0 1 2 3 4 5 X 6 7
    #
    # The implementation handles wrapped cases separately for this reason.
    current_pos = reorder_map[original_idx]
    next_pos = (current_pos + delta) % len(reorder_map)

    wrap_occurs = (current_pos + delta) != next_pos
    if not wrap_occurs:
        # Move each displaced element towards `current_pos` (against the delta)
        shift = 1 if delta > 0 else -1
        for i in range(current_pos + shift, next_pos + shift, shift):
            i_original = inv_reorder_map[i]
            reorder_map[i_original] = i - shift
            inv_reorder_map[i - shift] = i_original
        reorder_map[original_idx] = next_pos
        inv_reorder_map[next_pos] = original_idx
    else:
        # Move each displaced element towards `current_pos` (against the delta)
        shift = (
            -1 if delta > 0 else 1
        )  # actual shift direction is negated since we're wrapping
        next_pos = (current_pos + delta - shift) % len(reorder_map)
        for i in range(current_pos + shift, next_pos + shift, shift):
            i_original = inv_reorder_map[i]
            reorder_map[i_original] = i - shift
            inv_reorder_map[i - shift] = i_original
        reorder_map[original_idx] = next_pos
        inv_reorder_map[next_pos] = original_idx


def solve(file, decryption_key, iterations):
    l = [v * decryption_key for v in file]

    reorder_map = list(range(len(l)))
    inv_reorder_map = list(range(len(l)))

    for _ in range(iterations):
        for i, v in enumerate(l):
            move(reorder_map, inv_reorder_map, i, v)

    # Get original coordinate of [0]
    zero_idx_original = [i for i, v in enumerate(l) if v == 0].pop()
    zero_idx = reorder_map[zero_idx_original]

    return sum(
        [
            l[inv_reorder_map[(zero_idx + offset) % len(inv_reorder_map)]]
            for offset in [1000, 2000, 3000]
        ]
    )


print(f"Part 1: {solve(file, 1, 1)}")
print(f"Part 2: {solve(file, 811589153, 10)}")
