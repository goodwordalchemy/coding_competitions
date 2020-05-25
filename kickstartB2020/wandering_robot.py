from math import log2, factorial

DEV = True

sample_text = """4
3 3 2 2 2 2
5 3 1 2 4 2
1 10 1 3 1 5
6 4 1 3 3 4
"""
samples = [
    ("3 3 2 2 2 2", 0.5),
    ("5 3 1 2 4 2", 0.0625),
    ("1 10 1 3 1 5", 0.0),
    ("6 4 1 3 3 4", 0.3125),
    ("5 4 3 2 4 3", 0.375),
    ("4 4 2 4 3 4", 0.5),
    ("4 4 4 2 4 3", 0.5),
    ("5 4 3 4 3 4", 0.5),
    ("3 3 2 1 2 3", 0),
    ("3 3 1 2 3 2", 0),
    ("3 3 3 1 3 2", 0),
    ("100000 100000 2 2 2 2", -1),
    ("100000 100000 99999 99999 99999 99999", -1),
]
sample_inputs, sample_outputs = zip(*samples)

sample_text  = str(len(samples))+'\n'+"\n".join(sample_inputs)
if DEV:
    print("expected output:\n")
    print("\n".join("EXPECT Case {}: {}".format(i+1, o) for i, o in enumerate(sample_outputs)))
    print()


if DEV:
    from collections import deque
    from unittest.mock import MagicMock
    sample_lines = deque(sample_text.split("\n"))

    input = MagicMock(side_effect=lambda : sample_lines.popleft())



def parse_input():
    n_test_cases = int(input())
    test_cases = []
    for t in range(n_test_cases):
        test_cases.append(list(map(lambda x: int(x), input().split())))

    return test_cases

def walk(w, h, l, u, r, d):
    def get_guarantee_positions():
        positions = []

        # upper right...
        x, y = r, u
        x += 1
        y -= 1
        while y > 0 and x <= w:
            positions.append((y, x))
            x += 1
            y -= 1

        # lower left...
        x, y = l, d
        x -= 1
        y += 1
        while y <= h and x > 0:
            positions.append((y, x))
            x -= 1
            y += 1

        return positions

    def reduced_combinations(n, k):
        exponent = (
            log2(factorial(n))
            - log2(factorial(k))
            - log2(factorial(n-k))
            - n
        )

        return 2**exponent

    def get_position_probability(y, x):
        n_moves_to_pos = x + y - 2

        if x != w and y != h:
            p = (0.5)**n_moves_to_pos
            p *= reduced_combinations(n_moves_to_pos, y-1) * 2**(n_moves_to_pos)

        """
        The thinking here is that, if we are in the last row or last column,
        the rules change a bit.  Take the case of the furthest right column.
        In that column we can only move down.  So to get a probability
        in that colunm, we add the full probability of the row above and
        half of the probability of the column to the left.
        """
        if x == w:
            p = 0.5**(w-1)
            for yy in range(2, y+1):
                p += 0.5 * get_position_probability(yy, x-1)
        if y == h:
            p = 0.5**(h-1)
            for xx in range(2, x+1):
                p += 0.5 * get_position_probability(y-1, xx)

        return p

    probabilities = [get_position_probability(*pos) for pos in get_guarantee_positions()]
    # from pprint import pprint
    # pprint(list(zip(get_guarantee_positions(), probabilities)))

    return sum(probabilities)



def walk_dp(w, h, l, u, r, d):
    def in_hole(row, col):
        if row >= u-1 and row <= d-1 and col >= l-1 and col <= r-1:
            #print("in_hole", row, col)
            return True
        return False

    dp = [0]*w
    dp[0] = 1
    for col in range(1, w):
        if in_hole(0, col):
            continue
        dp[col] = 0.5 * dp[col-1]
    #print(dp)

    for row in range(1, h):
        prev = dp
        dp = [0]*w
        up_proportion = 0.5 if w > 1 else 1
        dp[0] = up_proportion*prev[0] if not in_hole(row, 0) else 0

        for col in range(1, w):
            if in_hole(row, col):
                continue
            left_proportion = 0.5 if row < h-1 else 1
            up_proportion = 0.5 if col < w-1 else 1
            dp[col] = left_proportion*dp[col-1] + up_proportion*prev[col]
        #print(dp)


    return str(dp[-1])

def debug():
    """
    The idea with debug mode is that I get a correct but slow answer with
    my dp solution, so I can use it to check my answers for
    the fast solution and get probabilities for test cases.
    """
    print()
    print("DEBUG OUTPUT...")
    for i, test_case in enumerate(parse_input()):
        print("EXPECT Case #{}: {}".format(i+1, walk_dp(*test_case)))
        print("ACTUAL Case #{}: {}".format(i+1, walk(*test_case)))
        print()

def main():
    for i, test_case in enumerate(parse_input()):
        print("Case #{}: {}".format(i+1, walk(*test_case)))

if __name__ == '__main__':
    main()
    # debug()
