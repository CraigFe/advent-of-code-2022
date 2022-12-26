def from_snafu(snafu):
    return sum({ '=': -2, '-': -1, '0': 0, '1': 1, '2': 2 }[v] * (5 ** i) for i, v in enumerate(reversed(list(snafu))))

def to_snafu(number):
    # First convert the number to base 5
    digits = []
    while number:
        digits.append(number % 5)
        number //= 5
    digits.append(0)

    # Convert overflow 3s, 4s and 5s to next digit
    for i, digit in enumerate(digits):
        if digit > 2: digits[i] -= 5; digits[i+1] += 1

    if digits[-1] == 0: digits = digits[:-1]

    return ''.join([{ -2: '=', -1: '-', 0: '0', 1: '1', 2: '2' }[x] for x in reversed(digits)])

with open("./day25/input.txt") as f:
    lines = f.read().splitlines()

part1 = to_snafu(sum([from_snafu(x) for x in lines]))
print(part1)
