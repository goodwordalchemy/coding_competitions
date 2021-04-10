DEV = True

sample_text = """6
5 1
ABCAA
4 2
ABAA
2 1
AA
2 1
AB
3 0
ABA
3 0
ABB"""


if DEV:
    from collections import deque
    from unittest.mock import MagicMock
    sample_lines = deque(sample_text.split("\n"))

    input = MagicMock(side_effect=lambda : sample_lines.popleft())



def parse_input():
    n_test_cases = int(input())
    test_cases = []
    for t in range(n_test_cases):
        _, k = list(map(int, input().split()))
        s = input()
        test_cases.append((k, s))

    return test_cases

def num_edits(k, s):
    return abs(k - sum(s[i] != s[-1-i] for i in range(len(s)//2)))


def main():
    for i, test_case in enumerate(parse_input()):
        print("Case #{}: {}".format(i+1, num_edits(*test_case)))

if __name__ == '__main__':
    main()
