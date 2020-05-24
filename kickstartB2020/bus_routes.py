import heapq


DEV = True
sample_text = """3
3 10
3 7 2
4 100
11 10 5 50
1 1
1
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
        N, D = input().split()
        freqs = list(map(int, input().split()))
        assert len(freqs) == int(N)
        test_cases.append((int(D), freqs))

    return test_cases


def try_day(end, freqs):
    freqs = freqs.copy()[:]
    start = end
    while freqs:
        cur = freqs.pop()
        while start % cur != 0:
            start -= 1

    return start


def bus_route(n_days, freqs):
    start = try_day(n_days, freqs)
    for end in reversed(range(n_days-max(freqs), n_days)):

        start = max(start, try_day(end, freqs))

    return start


def main():
    for i, test_case in enumerate(parse_input()):
        print("Case #{}: {}".format(i+1, bus_route(*test_case)))

if __name__ == '__main__':
    main()
