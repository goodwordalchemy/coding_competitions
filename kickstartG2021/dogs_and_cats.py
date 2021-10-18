DEV = True

sample_text = """8
6 10 4 0
CCDCDD
4 1 2 0
CCCC
4 2 1 0
DCCD
12 4 2 2
CDCCCDCCDCDC
8 2 1 3
DCCCCCDC
3 1 1 1
DCCCCCC
3 1 1 1
DCCCD
3 1 1 1
DCCC
"""

# case where all dogs are fed, and not enough cat food.
# case where we run out of cat food and a dog is waiting
# case where run out of cat food and no dogs waiting


if DEV:
    from collections import deque
    from unittest.mock import MagicMock
    sample_lines = deque(sample_text.split("\n"))

    input = MagicMock(side_effect=lambda : sample_lines.popleft())



def parse_input():
    t_test_cases = int(input())
    test_cases = []
    for t in range(t_test_cases):
        N, D, C, M = list(map(int, input().split()))
        line = input()
        yield (D, C, M, line)


def solution(D, C, M, line):
    for i, elt in enumerate(line):
        if D == 0:
            break
        i += 1

        if elt == "D":
            D -= 1
            C += M
        elif elt == "C":
            if C == 0:
                break
            C -= 1
        else:
            raise Exception("unknown animal")


    dogs_unfed = sum(1 for l in line[i:] if l == "D")

    if dogs_unfed > 0:
        return "NO"
    else:
        return "YES"


def main():
    for i, test_case in enumerate(parse_input()):
        print("Case #{}: {}".format(i+1, solution(*test_case)))

if __name__ == '__main__':
    main()
