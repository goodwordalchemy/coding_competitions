from scipy.optimize import fsolve

DEV = True

sample_text = """2
4 36
5 2
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

def segments(p):
    return zip(p, p[1:] + [p[0]])

def area(p):
    return 0.5 * abs(sum(x0*y1 - x1*y0
                         for ((x0, y0), (x1, y1)) in segments(p)))
    


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
