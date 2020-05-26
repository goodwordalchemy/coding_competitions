from collections import defaultdict

DEBUG = False

test_data = """4
4 6
ZOAAMM
ZOAOMM
ZOOOOM
ZZZZOM
4 4
XXOO
XFFO
XFXO
XXXO
5 3
XXX
XPX
XXX
XJX
XXX
3 10
AAABBCCDDE
AABBCCDDEE
AABBCCDDEE
"""

if DEBUG:
    from unittest.mock import MagicMock

    input = MagicMock(side_effect=test_data.split("\n"))

def parse_input():
    cases = []
    n_cases = int(input())
    for _ in range(n_cases):
        r, c = list(map(int, input().split()))
        case = []
        for row in range(r):
            case.append(list(input()))
        cases.append(case)

    return cases

def stable_wall(wall):
    M, N = len(wall), len(wall[0])

    # build a graph of dependencies
    outgoing = defaultdict(set)
    incoming = defaultdict(set)
    blocks = set()

    for col in range(N):
        cur = wall[0][col]
        blocks.add(cur)
        for row in range(1, M):
            if wall[row][col] == cur:
                continue
            else:
                outgoing[wall[row][col]].add(cur)
                incoming[cur].add(wall[row][col])

            cur = wall[row][col]
            blocks.add(cur)


    # topological sort it
    result = []
    S = blocks - set(outgoing.keys())

    while S:
        cur = S.pop()
        result.append(cur)
        neighbors = incoming[cur]

        for node in list(neighbors):
            incoming[cur].remove(node)
            outgoing[node].remove(cur)
            if not outgoing[node]:
                S.add(node)

    if sum(map(len, incoming.values())):
        return -1
    return "".join(reversed(result))


def main():
    cases = parse_input()
    for i, wall in enumerate(cases):
        print("Case #{}: {}".format(i+1, stable_wall(wall)))



if __name__ == '__main__':
    main()

