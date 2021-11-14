DEV = True

sample_text = """5
abcd
a
pppp
p
pqrst
ou
abd
abd
aaaaaaaaaaaaaaab
aceg
"""


if DEV:
    from collections import deque
    from unittest.mock import MagicMock
    sample_lines = deque(sample_text.split("\n"))

    input = MagicMock(side_effect=lambda : sample_lines.popleft())



def parse_input():
    n_test_cases = int(input())
    for t in range(n_test_cases):
        S = input()
        F = input()
        yield (S, F)


def solution1(S, F):
    f = ord(F[0]) - ord('a')

    result = 0
    for elt in S:
        s_elt = ord(elt) - ord('a')
        result += min((s_elt-f)%26, (f-s_elt)%26)


    return result

def solution(S, F):
    if len(F) == 1:
        return solution1(S, F)
    
    f = {ord(elt)-ord('a') for elt in F}

    result = 0
    for elt in S:
        s_elt = ord(elt) - ord('a')

        for up in range(26):
            if (s_elt + up) % 26 in f:
                break

        if up <= 1:
            result += up
            continue

        for down in range(26):
            if (s_elt - down) % 26 in f:
                break

        result += min(up, down)

    return result


def main():
    for i, test_case in enumerate(parse_input()):
        print("Case #{}: {}".format(i+1, solution(*test_case)))

if __name__ == '__main__':
    main()
