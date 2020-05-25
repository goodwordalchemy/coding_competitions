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
    ("3 3 3 1 3 2", 0.5),
    ("100000 100000 2 2 2 2", 0.5),
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


class Log2Factorial:
    """
    cache[i] = log2(i!)
    because log of products is sum of logs
    """
    def __init__(self):
        cache = [0]
        for i in range(1, 200001): 
            cache.append(cache[-1]+log2(i))

        self.cache = cache

    def query(self, i):
        return self.cache[i]


log2factorial = Log2Factorial().query


def parse_input():
    n_test_cases = int(input())
    test_cases = []
    for t in range(n_test_cases):
        test_cases.append(list(map(lambda x: int(x), input().split())))

    return test_cases

def walk(w, h, l, u, r, d):
    def reduced_combinations(n, k):
        exponent = (
            log2factorial(n)
            - log2factorial(k)
            - log2factorial(n-k)
            - n
        )

        return 2**exponent

    def probability(x, y):
        n_moves_to_pos = x + y
        return reduced_combinations(n_moves_to_pos, y)

    if u == 1 and d == h:
        return 0.0
    elif l == 1 and r == w:
        return 0.0

    w -= 1
    h -= 1
    l -= 1
    u -= 1
    r -= 1
    d -= 1

    p = 0
    if u != 0:
        for x in range(l, min(r+1, w)):
            p += probability(x, u-1)

    if l != 0:
        for y in range(u, min(d+1, h)):
            p += probability(l-1, y)

    if r == w:
        for y in range(u):
            p += probability(r-1, y)
    if d == h:
        for x in range(l):
            p += probability(x, h-1)

    return 1 - p / 2



def walk_fuck(w, h, l, u, r, d):
    if u == 1 and d == h:
        return 0.0
    elif l == 1 and r == w:
        return 0.0

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
            log2factorial(n)
            - log2factorial(k)
            - log2factorial(n-k)
            - n
        )

        return 2**exponent

    def get_position_probability(y, x, depth=0):
        assert depth <= 1
        n_moves_to_pos = x + y - 2

        if x != w and y != h:
            p = reduced_combinations(n_moves_to_pos, y-1)

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
                p += 0.5 * get_position_probability(yy, x-1, depth+1)
        if y == h:
            p = 0.5**(h-1)
            for xx in range(2, x+1):
                p += 0.5 * get_position_probability(y-1, xx, depth+1)

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
