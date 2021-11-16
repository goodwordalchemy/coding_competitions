from itertools import permutations
from collections import defaultdict

DEV = True

def _debug(*x, enabled=False):
    if DEV and enabled:
        print(*x)

sample_text = """3
4 3 3
1 3 1
1 1 1
2 4 1
2 3 1
0 1
1 2
2 3
4 5 3
1 3 1
1 1 1
2 4 1
2 3 1
0 1
1 2
2 3
3 0
0 2
4 1 2
0 4 1
0 4 1
0 4 2
0 4 2
0 1
"""
# sample_text = """1
# 4 3 3
# 1 3 1
# 1 1 1
# 2 4 1
# 2 3 1
# 0 1
# 1 2
# 2 3
# """

"""
other cases:
* gets to end
* empty stuff
"""


if DEV:
    from collections import deque
    from unittest.mock import MagicMock
    sample_lines = deque(sample_text.split("\n"))

    input = MagicMock(side_effect=lambda : sample_lines.popleft())



def parse_input():
    t_test_cases = int(input())
    for t in range(t_test_cases):
        N, M, K = list(map(int, input().split()))
        rooms = []
        for _ in range(N):
            Li, Ri, Ai = list(map(int, input().split()))
            rooms.append((Li, Ri, Ai))
        corridors = []
        for _ in range(M):
            Xj, Yj = list(map(int, input().split()))
            corridors.append((Xj, Yj))

        yield (K, rooms, corridors)


L_IDX = 0
R_IDX = 1
A_IDX = 2

def is_ith_bit_set(x, i):
    return (x >> i) & 1

def solution(K, rooms, corridors):
    N = len(rooms)

    # find total magic points for every combination of rooms
    combinations_to_points = {}
    for i in range(2**N):
        combo_points = 0
        for j in range(N):
            # if i >> (N-j-1) & 1:
            if is_ith_bit_set(i, j):
                combo_points += rooms[j][A_IDX]

        combinations_to_points[i] = combo_points

    # create adjacency bitmasks
    adjacency_bitmasks = [0 for _ in range(N)]
    for x, y in corridors:
        adjacency_bitmasks[x] |= (1 << y)
        adjacency_bitmasks[y] |= (1 << x)

    # for each combination of rooms, determine if a new room can be visited
    can_visit = [set() for _ in range(2**N)]
    for j in range(N):
        can_visit[0].add(j)

    for i in range(2**N):
        for j in range(N):
            _debug(bin(i)[2:], j)
            # if (i >> (N-j-1)) & 1:
            if is_ith_bit_set(i, j):
                continue
            if not (adjacency_bitmasks[j] & i):
                continue
            if combinations_to_points[i] < rooms[j][L_IDX]:
                continue
            if combinations_to_points[i] > rooms[j][R_IDX]:
                continue
            can_visit[i].add(j)
            

    # which combinations are reachable from any single room starting point
    reachable = [0 for _ in range(2**N)]
    reachable[0] = 1
    for i in range(1, 2**N):
        for j in range(N):
            if not is_ith_bit_set(i,j):
                continue
            prev  = i & ~(1 << j)
            if j not in can_visit[prev]:
                continue
            reachable[i] += reachable[prev]

    _debug("K", K)
    _debug("rooms",rooms)
    _debug("corridors", corridors)
    _debug("combinations_to_points", combinations_to_points)
    _debug("combinations_to_points_binary", {bin(k)[2:]:v for k,v  in  combinations_to_points.items()})
    _debug("adjacency_bitmasks",[(i,bin(k)[2:]) for i, k in enumerate(adjacency_bitmasks)])
    _debug("can_visit",[(bin(i)[2:],k) for i,k in enumerate(can_visit)])
    _debug("reachable",reachable)

    # filter down to combinations with K points
    result = 0
    for i in range(2**N):
        if combinations_to_points[i] != K:
            continue
        result += reachable[i]

    return result



def main():
    for i, test_case in enumerate(parse_input()):
        print("Case #{}: {}".format(i+1, solution(*test_case)))

if __name__ == '__main__':
    main()
