from collections import deque
DEV = True

sample_text = """4
3 3 2 2 2 2
5 3 1 2 4 2
1 10 1 3 1 5
6 4 1 3 3 4
"""


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
    dp = [[0 for col in range(w)] for row in range(h)]
    dp[0][0] = 1

    queue = deque([(0, 0)])
    for row in range(h):
        for col in range(w):
            if in_hole(row, col, l, u, r, d):
                continue

            if row == h-1 and col == w-1:
                break

            neighbors = []
            if row < h-1:
                neighbors.append((row+1, col))
            if col < w-1:
                neighbors.append((row, col+1))

            prob = dp[row][col] / len(neighbors)

            neighbors = [
                (row, col) for row, col in neighbors
                if not in_hole(row, col, l, u, r, d)
            ]

            for n_row, n_col in neighbors:
                dp[n_row][n_col] += prob

    return str(dp[-1][-1])


def in_hole(row, col, l, u, r, d):
    if row >= u-1 and row <= d-1 and col >= l-1 and col <= r-1:
        return True
    return False


def main():
    for i, test_case in enumerate(parse_input()):
        print("Case #{}: {}".format(i+1, walk(*test_case)))

if __name__ == '__main__':
    main()
