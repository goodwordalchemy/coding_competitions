DEV = True

sample_text = """2
10 4 2
800 2 8
1500 6 9
200 4 7
400 3 5
5 3 3
400 1 3
500 5 5
300 2 3
"""


if DEV:
    from collections import deque
    from unittest.mock import MagicMock
    sample_lines = deque(sample_text.split("\n"))

    input = MagicMock(side_effect=lambda : sample_lines.popleft())



def parse_input():
    n_test_cases = int(input())
    for t in range(n_test_cases):
        D, N, K = list(map(int, input().split()))
        rides = []
        for _ in range(N):
            h, s, e = list(map(int, input().split()))
            rides.append((h, s, e))
        yield (D, K, rides)


def solution(D, K, rides):
    days = [[] for _ in range(D)]

    for h, s, e in rides:
        for d in range(s-1, e):
            days[d].append(h)

    best_score = -1
    for d in days:
        d.sort()
        best_score = max(best_score, sum(d[-K:]))
        
    return best_score



def main():
    for i, test_case in enumerate(parse_input()):
        print("Case #{}: {}".format(i+1, solution(*test_case)))

if __name__ == '__main__':
    main()
