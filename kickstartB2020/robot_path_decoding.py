from collections import deque

SIZE = 10**9
DIGITS = set(map(str, range(2, 10)))

def parse_input():
    n_test_cases = int(input())
    test_cases = []
    for t in range(n_test_cases):
        test_cases.append(input())

    return test_cases


def robot(program):
    w, h = unravel(deque(program))

    return '{} {}'.format(w+1, h+1)

def move(ins, w, h):
    if ins == 'N':
        h -= 1
    elif ins == 'S':
        h += 1
    elif ins == 'W':
        w -= 1
    elif ins == 'E':
        w += 1
    else:
        raise Exception("invalid instruction: {}".format(ins))

    w %= SIZE
    h %= SIZE

    return w, h


def unravel(program):
    w, h = 0, 0
    while program:
        cur = program.popleft()
        if cur in DIGITS:
            assert program.popleft() == '('
            w_n, h_n = unravel(program)
            w += int(cur) * w_n
            h += int(cur) * h_n
            w %= SIZE
            h %= SIZE
        elif cur == ')':
            return w, h
        else:
            w, h = move(cur, w, h)

    return w, h


def main():
    for i, test_case in enumerate(parse_input()):
        print("Case #{}: {}".format(i+1, robot(test_case)))

DEV = True
sample_text = """4
SSSEEE
N
N3(S)N2(E)N
2(3(NW)2(W2(EE)W))
"""


if DEV:
    from collections import deque
    from unittest.mock import MagicMock
    sample_lines = deque(sample_text.split("\n"))

    input = MagicMock(side_effect=lambda : sample_lines.popleft())

if __name__ == '__main__':
    main()
