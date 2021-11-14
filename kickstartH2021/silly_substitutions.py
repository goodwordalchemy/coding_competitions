DEV = False

sample_text = """7
3
012
4
0145
5
00000
11
98765432101
2
01
1
1
2
10
"""


if DEV:
    from collections import deque
    from unittest.mock import MagicMock

    sample_lines = deque(sample_text.split("\n"))

    input = MagicMock(side_effect=lambda: sample_lines.popleft())


substitutions = [
    ("01", "2"),
    ("12", "3"),
    ("23", "4"),
    ("34", "5"),
    ("45", "6"),
    ("56", "7"),
    ("67", "8"),
    ("78", "9"),
    ("89", "0"),
    ("90", "1"),
]


def parse_input():
    n_test_cases = int(input())
    for t in range(n_test_cases):
        _ = input()
        N = input()
        yield (N,)


def do_substitutions(N):
    cur = list(N)

    for to_sub, sub_to in substitutions:
        i = 0
        result = []
        while i < len(cur):
            if i == len(cur) - 1:
                result.append(cur[-1])
                break

            two = "".join(cur[i : i + 2])
            if two == to_sub:
                result.append(sub_to)
                i += 1
            else:
                result.append(cur[i])
            i += 1
        cur = result

    # print("N", "".join(N))
    # print("cur", "".join(cur))
    return cur


def solution(N):
    prev = list(N)
    cur = do_substitutions(prev)

    while prev != cur:
        prev = cur
        cur = do_substitutions(prev)

    return "".join(cur)


def main():
    for i, test_case in enumerate(parse_input()):
        print("Case #{}: {}".format(i + 1, solution(*test_case)))


if __name__ == "__main__":
    main()
