DEV = False

sample_text = """4
3
10 20 14
4
7 7 7 7
5
10 90 20 90 10
3
10 3 10
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
        n_checkpoints = int(input())
        tc = list(map(int, input().split()))
        test_cases.append(tc)

    return test_cases

def num_peaks(path):
    return sum(
        path[i] > path[i-1] and path[i] > path[i+1]
        for i in range(1, len(path)-1)
    )



def main():
    for i, test_case in enumerate(parse_input()):
        print("Case #{}: {}".format(i+1, num_peaks(test_case)))

if __name__ == '__main__':
    main()
