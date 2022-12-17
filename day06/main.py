with open("./day06/input.txt") as f:
    message = f.read().splitlines()[0]

window_size = 14  # 4
i = window_size
while len(set(message[i-window_size:i])) < window_size:
    i += 1
print(i)
