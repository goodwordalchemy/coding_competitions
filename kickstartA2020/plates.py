from functools import lru_cache

DEV = True

sample_text = """2
2 4 5
10 10 100 30
80 50 10 50
3 2 3
80 80
15 50
20 10"""


if DEV:
    from collections import deque
    from unittest.mock import MagicMock
    sample_lines = deque(sample_text.split("\n"))

    input = MagicMock(side_effect=lambda : sample_lines.popleft())



def parse_input():
    n_test_cases = int(input())
    test_cases = []
    for t in range(n_test_cases):
        N, K, P = map(int, input().split())
        tc = []
        for stack in range(N):
            tc.append(list(map(int, input().split())))
        test_cases.append((P, tc))

    return test_cases


def plates(p, plates):
    if not plates or not p or not plates[0]:
        return 0
    N = len(plates)
    K = len(plates[0])

    prefixes = []
    for stack in plates:
        prefix = [0]
        for elt in stack:
            prefix.append(prefix[-1]+elt)
        prefixes.append(prefix)

    @lru_cache(None)
    def dp(i, p):
        if i == N:
            return 0
        elif p == 0:
            return 0
        elif p < 0:
            return -float('inf')

        result = 0
        for j in range(min(K, p)+1):
            result = max(
                result,
                prefixes[i][j] + dp(i+1, p-j)
            )
        return result

    return dp(0, p)


def main():
    for i, test_case in enumerate(parse_input()):
        print("Case #{}: {}".format(i+1, plates(*test_case)))

if __name__ == '__main__':
    main()
