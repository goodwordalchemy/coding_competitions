"""
My plan for this one is to find all of the intersections.  Then at each intersection, extend as far as possible in each direction and check if double that length exists on either perpendicular section.

Another way to do this is to cache the length of the run in every direction at every point.  So keep 4 grids.  Then at each point, you still have to walk in every direction from that point, but you don't have to then walk in the long direction because you have that cached.

A way to speed this up is to notice that we only need to start with the longest length
then work backwards until we find a match.  If we find a match, then we can increment by several
And in fact, we can binary search for the first match.

So, binary search in [0, length of run] in each of the perpendiculars.

this will take a half hour to implement.

"""

DEV = True

sample_text = """2
4 3
1 0 0
1 0 1
1 0 0
1 1 0
6 4
1 0 0 0
1 0 0 1
1 1 1 1
1 0 1 0
1 0 1 0
1 1 1 0"""



if DEV:
    from collections import deque
    from unittest.mock import MagicMock
    sample_lines = deque(sample_text.split("\n"))

    input = MagicMock(side_effect=lambda : sample_lines.popleft())



def parse_input():
    n_test_cases = int(input())
    test_cases = []
    for t in range(n_test_cases):
        r, _ = list(map(int, input().split()))
        grid = []
        for _ in range(r):
            grid.append(list(map(int, input().split())))

        test_cases.append(grid)

    return test_cases

def get_runs(grid, iter1, iter2, swap=False):
    iter1 = list(iter1)
    iter2 = list(iter2)
    R, C = len(grid), len(grid[0])
    runs = [[0]*C for _ in range(R)]
    for i in iter1:
        run = 0
        for j in iter2:
            cell = grid[i][j] if not swap else grid[j][i]
            if cell:
                run += 1
            else:
                run = 0

            if not swap:
                runs[i][j] = run

            else:
                runs[j][i] = run
    return runs


def l_shaped_plots_slow(grid):
    R, C = len(grid), len(grid[0])

    lefts = get_runs(grid, range(R), range(C))
    rights = get_runs(grid, range(R), reversed(range(C)))
    downs = get_runs(grid, range(C), range(R), True)
    ups = get_runs(grid, range(C), reversed(range(R)), True)
    
    configs = [
        [lefts, (downs, ups)],
        [rights, (downs, ups)],
        [downs, (lefts, rights)],
        [ups, (lefts, rights)],
    ]

    # print(">>>>>>>>>>")
    # print("lefts")
    # cur = lefts
    # for row in cur:
    #     print(row)
    # print("rights")
    # cur = rights
    # for row in cur:
    #     print(row)
    # print("grid")
    # cur = grid
    # for row in cur:
    #     print(row)
    # print("<<<<<<<<<<")

    result = 0
    for i in range(R):
        for j in range(C):
            l = 2
            while True:
                candidates = [c for c in configs if c[0][i][j] >= l]
                if not candidates:
                    break
                for c in candidates:
                    for k in range(2):
                        if c[1][k][i][j] >= l*2:
                            result += 1
                l += 1

    return result



def l_shaped_plots(grid):
    R, C = len(grid), len(grid[0])

    lefts = get_runs(grid, range(R), range(C))
    rights = get_runs(grid, range(R), reversed(range(C)))
    downs = get_runs(grid, range(C), range(R), True)
    ups = get_runs(grid, range(C), reversed(range(R)), True)
    
    configs = [
        [lefts, (downs, ups)],
        [rights, (downs, ups)],
        [downs, (lefts, rights)],
        [ups, (lefts, rights)],
    ]

    result = 0
    for i in range(R):
        for j in range(C):
            for c, ns in configs:
                if c[i][j] < 4:
                    continue
                for n in ns:
                    if n[i][j] < 2:
                        continue
                    low = 2
                    high = c[i][j] // 2
                    while low < high:
                        guess = (low + high) // 2
                        if n[i][j] > guess:
                            low = guess + 1
                        else:
                            high = guess

                    result += low-1

    return result


def main():
    for i, test_case in enumerate(parse_input()):
        print("Case #{}: {}".format(i+1, l_shaped_plots(test_case)))

if __name__ == '__main__':
    main()
