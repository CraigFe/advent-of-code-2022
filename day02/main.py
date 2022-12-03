def score(them, us):
    win_score = 0
    match them, us:
        # Win cases
        case ("C", "A") | ("A", "B") | ("B", "C"):
            win_score = 6
        case x, y if x == y:
            win_score = 3  # Draw

    play_score = ord(us) - ord("A") + 1
    return win_score + play_score


def interpretation1(them, second_col):
    # Our move is the second column shifted back ('X' - 'A') places.
    us = chr(ord(second_col) - ord("X") + ord("A"))
    return score(them, us)


def interpretation2(them, second_col):
    # Could do some modular arithmetic here but it's faster to just enumerate
    # all the cases...
    match them, second_col:
        case "A", "X": us = "C"
        case "B", "X": us = "A"
        case "C", "X": us = "B"
        case _  , "Y": us = them
        case "A", "Z": us = "B"
        case "B", "Z": us = "C"
        case "C", "Z": us = "A"
        case _, _: raise Exception(f"unrecognised column: {them} {second_col}")
    return score(them, us)


with open("./day02/input.txt") as f:
    entries = f.read().splitlines()
    scores1 = [interpretation1(x[0], x[2]) for x in entries] 
    scores2 = [interpretation2(x[0], x[2]) for x in entries] 

    print(f"Part 1: {sum(scores1)}")
    print(f"Part 2: {sum(scores2)}")
