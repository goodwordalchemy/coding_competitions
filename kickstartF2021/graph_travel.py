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


"""
for this one, 
1. construct the graph.
2. try all 40320 permutations of the 8 indices (in worst case)

what does it mean to "try" a path.

* start with the amount of points in the first room of the path.
* start with an accessible set containing just the first room.
* create a frontier set of accessible neighbors

* loop as follows:
    x. if the next element in the path is not a neighbor of current, fail
    x. if the current amount of points is not in range for neighbor, fail.
    x. set current to next element.  update amount of points.  add current 
       element to accessible set.  add it's neighbors to frontier.
    x. if the current amount of points is K, SUCCEED
* if you get to this step, fail.

"""

L_IDX = 0
R_IDX = 1
A_IDX = 2

def try_path(path, graph, K, rooms):
    elt = path[0]
    points = 0
    frontier = set()

    points += rooms[elt][A_IDX]
    if points == K:
        return path[:1]

    frontier.update(graph[elt]) 




    for i in range(1, len(path)):
        elt = path[i]
        if elt not in frontier:
            return None
        if points < rooms[elt][L_IDX] or points > rooms[elt][R_IDX]:
            return None
        if points > K:
            return None

        points += rooms[elt][A_IDX]
        if points == K:
            return path[:i+1]

        frontier.update(graph[elt]) 

    return None


def solution(K, rooms, corridors):
    _debug(K, rooms, corridors)
    graph = defaultdict(set)

    for Xj, Yj in corridors:
        graph[Xj].add(Yj)
        graph[Yj].add(Xj)


    result = 0
    ways = set()
    for path in permutations(range(len(rooms))):
        _debug(path)
        result = try_path(path, graph, K, rooms)
        if result is not None:
            ways.add(tuple(result))
            _debug(result)

    return len(ways)


def main():
    for i, test_case in enumerate(parse_input()):
        print("Case #{}: {}".format(i+1, solution(*test_case)))

if __name__ == '__main__':
    main()
