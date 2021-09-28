from collections import Counter, defaultdict

"""
sources:

algorithm for 2d counting:
https://arxiv.org/pdf/1711.04563.pdf

basics and 1d version:
https://www.researchgate.net/publication/220858726_Cellular_Automata_Preimages_Count_and_List_Algorithm


new idea.  kinda based on the first.

go layer by layer and output possible (configuration, count) tuples.

"""

def int2row(i, row_length):
    return tuple([bool(int(b)) for b in bin(i)[2:].rjust(row_length, '0')])


def chunks(lst, n):
    result = []
    for i in range(0, len(lst), n):
        result.append( lst[i:i + n])
    return result

ALL_PRECUSORS = [chunks(int2row(i, 4), 2) for i in range(2**4)]
ON_PRECURSORS = [p for p in ALL_PRECUSORS if sum(map(sum, p)) == 1]
OFF_PRECURSORS = [p for p in ALL_PRECUSORS if sum(map(sum, p)) != 1]


"""problem with function below is that top block is not defined by 0s.

We need to do what we did before where the top row stiches together all 
precursors that result in the desired configuration
"""


def init_dp(row, cur, dp):
    if len(cur[0]) == len(row) + 1:
        dp[tuple(cur[1])] += 1
        return

    col = len(cur[0])
    if row[col-1]:
        precursors = ON_PRECURSORS
    else:
        precursors = OFF_PRECURSORS

    for p in precursors:
        if cur[0][-1] == p[0][0] and cur[1][-1] == p[1][0]:

            cur[0].append(p[0][1])
            cur[1].append(p[1][1])
            init_dp(row, cur, dp)
            cur[0].pop()
            cur[1].pop()



def dfs_for_configs(row, top, cur, candidates):
    if len(cur) == len(row)+1:
        candidates.append(tuple(cur))
        return

    col = len(cur)
    if row[col-1]:
        if top[col-1] + top[col] + cur[col-1] + 1 == 1:
            cur.append(True)
            dfs_for_configs(row, top, cur, candidates)
            cur.pop()
        elif top[col-1] + top[col] + cur[col-1] == 1:
            cur.append(False)
            dfs_for_configs(row, top, cur, candidates)
            cur.pop()
    else:
        if top[col-1] + top[col] + cur[col-1] + 1 != 1:
            cur.append(True)
            dfs_for_configs(row, top, cur, candidates)
            cur.pop()

        if top[col-1] + top[col] + cur[col-1] != 1:
            cur.append(False)
            dfs_for_configs(row, top, cur, candidates)
            cur.pop()


def aggregate_over_precursors2(C):
    M, N = len(C), len(C[0])
    dp = Counter()
    init_dp(C[0], [[0],[0]], dp)
    init_dp(C[0], [[1],[0]], dp)
    init_dp(C[0], [[0],[1]], dp)
    init_dp(C[0], [[1],[1]], dp)

    for i in range(1,M):
        row = C[i]
        prev = dp
        dp = Counter()
        for top, a in prev.items():
            candidates = []
            dfs_for_configs(row, top, [False], candidates)
            dfs_for_configs(row, top, [True], candidates)

            for c in candidates:
                dp[c] += a

    return sum(dp.values())



def _transpose(l):
    return list(map(list, zip(*l)))


def solution(g):
    C = _transpose(g)

    return aggregate_over_precursors2(C)




test_cases = [
    (
        ([[True, False, True], [False, True, False], [True, False, True]],),
        4,
    ),
    (
        ([[True, False, True, False, False, True, True, True], [True, False, True, False, False, False, True, False], [True, True, True, False, False, False, True, False], [True, False, True, False, False, False, True, False], [True, False, True, False, False, True, True, True]],),
        254
    ),
    (
        ([[True, True, False, True, False, True, False, True, True, False], [True, True, False, False, False, False, True, True, True, False], [True, True, False, False, False, False, False, False, False, True], [False, True, False, False, False, False, True, True, False, False]],),
        11567
    ), 
]

test_cases += [
    (
        (
            [
                [True, False, False],
                [True, False, False],
                [False, False, True],
            ],
        ), 
        156
    ),
    (
        (
            [
                [True, True, True, False],
                [False, False, True, False],
                [False, False, False, True],
            ],
        ),
        196
    ),
    (
        (
            [
                [False, True, False],
                [False, True, False],
                [False, False, True],
                [True, True, True],
            ],
        ),
        56
    ),
    (([[False, False, False], [False, False, False], [False, False, True], [False, False, True], [True, False, True]],),3370),
    (([[False, True, False, True, False], [False, False, False, False, True], [True, True, False, True, False]],),50),
]


for args, ans in test_cases:
    result = solution(*args)
    print("=" * 100 + "\n")
    if result == ans:
        print("pass (args={})".format(args))
    else:
        print("\n\n".join([
            "result is not correct.",
            "args:\n{}".format(args),
            "expected:\n{}".format(ans),
            "actual:\n{}".format(result),
        ]))

from big_boards import bb
for i, b in enumerate(bb):
    print("bb: ", i)
    print(solution(b))
