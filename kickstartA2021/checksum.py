"""
Ok, this one is a dynamic programming exercise I think.  

You need a strategy to get each -1 either alone in a row or alone in a columns.

So one way you can minimize costs is to use logic well.  This is a must.
The other way you can minimize costs is by spending small amounts of time recovering.

What is most brute force way to solve this?

It would be to try every path of uncovering.  So this would basically be O(N!).

Would pass first test case, which is good, but let's give it a few minutes and 
see if I can do better.  I think some kind of greedy algorithm would help.

Okay I will program brute force and then see if I can do better with some greedy
heuristic.
"""
from collections import defaultdict
from itertools import permutations
DEV = True

sample_text = """2
3
1 -1 0
0 1 0
1 1 1
0 1 0
0 0 0
0 0 0
1 1 1
0 0 1
2
-1 -1
-1 -1
1 10
100 1000
1 0
0 1"""



if DEV:
    from collections import deque
    from unittest.mock import MagicMock
    sample_lines = deque(sample_text.split("\n"))

    input = MagicMock(side_effect=lambda : sample_lines.popleft())



def parse_input():
    n_test_cases = int(input())
    test_cases = []
    for t in range(n_test_cases):
        n = int(input())
        A = []
        for _ in range(n):
            A.append(list(map(int, input().split())))
        B = []
        for _ in range(n):
            B.append(list(map(int, input().split())))
        R = list(map(int, input().split()))
        C = list(map(int, input().split()))
        test_cases.append((A, B, R, C))

    return test_cases

def get_missing_cells(A):
    missing = set()

    missing_by_row = defaultdict(set)
    missing_by_col = defaultdict(set)
    for i in range(len(A)):
        for j in range(len(A[0])):
            if A[i][j] == -1:
                missing_by_row[i].add(j)
                missing_by_col[j].add(i)
                missing.add((i, j))

    n = len(missing)
    while True:
        to_discard = set()
        for (i, j) in missing:
            if len(missing_by_row[i]) <= 1:
                to_discard.add((i, j))
                missing_by_row[i].discard(j)
                missing_by_col[j].discard(i)
        missing -= to_discard
        if len(missing) == n:
            break
        n = len(missing)

    return missing





def checksum(A, B, R, C):
    missing_cells = get_missing_cells(A)

    # get all permutations of missing cells array
    result = float('inf')
    for perm in permutations(missing_cells):
        A_copy = [a[:] for a in A]
        cost = 0
        mc = set(list(missing_cells))
        for i, j in perm:
            if (i, j) not in mc:
                continue
            A[i][j] = 1
            cost += B[i][j]
            mc = get_missing_cells(A_copy)
            if not mc:
                break

        result = min(result, cost)
    return result

    # for each permutation, for each element in permutation, check matrix 


def main():
    for i, test_case in enumerate(parse_input()):
        print("Case #{}: {}".format(i+1, checksum(*test_case)))

if __name__ == '__main__':
    main()
