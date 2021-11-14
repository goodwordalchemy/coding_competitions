DEV = True

sample_text = """3
9
YYYBBBYYY
6
YYGGBB
5
ROAOR
"""


if DEV:
    from collections import deque
    from unittest.mock import MagicMock
    sample_lines = deque(sample_text.split("\n"))

    input = MagicMock(side_effect=lambda : sample_lines.popleft())


color_mapping = {
    "U": set(),
    "R": set("R"),
    "Y": set("Y"),
    "B": set("B"),
    "O": set("RY"),
    "P": set("RB"),
    "G": set("YB"),
    "A": set("RYB"),
}


def parse_input():
    n_test_cases = int(input())
    for t in range(n_test_cases):
        _ = input()
        P = input()
        yield (P,)


def solution(P):
    cells = [color_mapping[elt] for elt in P]

    total_strokes = 0
    for primary_color in "RYB":
        in_stroke = False
        for c in cells:
            if primary_color in c:
                in_stroke = True
            else:
                total_strokes += in_stroke
                in_stroke = False
        total_strokes += in_stroke

    return total_strokes


def main():
    for i, test_case in enumerate(parse_input()):
        print("Case #{}: {}".format(i+1, solution(*test_case)))

if __name__ == '__main__':
    main()
