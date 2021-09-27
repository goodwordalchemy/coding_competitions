from collections import Counter, defaultdict

"""
sources:

algorithm for 2d counting:
https://arxiv.org/pdf/1711.04563.pdf

basics and 1d version:
https://www.researchgate.net/publication/220858726_Cellular_Automata_Preimages_Count_and_List_Algorithm



"""

def int2row(i, row_length):
    return tuple([bool(int(b)) for b in bin(i)[2:].rjust(row_length, '0')])


"""
dfs.

The idea with the new way to get these is to walk across C[i] and generate
each possible f-1(C[i]). If it is a legal neighbor to the precursor, then continue.
Otherwise backtrack.

if you get to the end of C[i], then you have a top to bottom mapping for the row
that can be put in the cache.

caveat is that first row of precursor should be all 0s.

"""
def chunks(lst, n):
    result = []
    for i in range(0, len(lst), n):
        result.append( lst[i:i + n])
    return result

ALL_PRECUSORS = [chunks(int2row(i, 4), 2) for i in range(2**4)]
ON_PRECURSORS = [p for p in ALL_PRECUSORS if sum(map(sum, p)) == 1]
OFF_PRECURSORS = [p for p in ALL_PRECUSORS if sum(map(sum, p)) == 0]

def _dfs_for_preimage(
    i, c, p, result, top_row_precursors, all_row_configs, is_first=False
):
    """
    i = column in row
    c = current row
    p = preimage so far (2 rows for this CA)
    result = defaultdict to store top->bottom mappings
    is_first = if true, top will always have a row of zeros
    """
    if i == len(c):
        # should memoize

        if is_first:
            top_prec = top_row_precursors
        else:
            top_prec = all_row_configs
        
        for top in top_prec:
            result[(top, tuple(p[1]))].append(tuple(map(tuple, p)))

        return

    if c[i]:
        precursor_gen = ON_PRECURSORS
    else:
        precursor_gen = OFF_PRECURSORS

    for cand in precursor_gen:
        if len(p[0]) == 0 or (p[0][-1] == cand[0][0] and p[1][-1] == cand[1][0]):
            p[0].append(cand[1][0])
            p[1].append(cand[1][1])
            _dfs_for_preimage(i+1, c, p, result, top_row_precursors, all_row_configs)
            p[0].pop()
            p[1].pop()
    
    
    
def _get_top_to_bottom_maps_for_each_row2(C):
    row_length = len(C[0])
    result = {}

    n_possible_rows = 2**(row_length+1)
    all_row_configs = [int2row(i, row_length+1) for i in range(n_possible_rows)]
    top_row_precursor = [int2row(0, row_length+1)]

    i = 0
    result[i+1] = defaultdict(list)
    row = C[i]
    _dfs_for_preimage(0, row, [[False],[False]], result[i+1], top_row_precursor, all_row_configs, is_first=True)
    _dfs_for_preimage(0, row, [[True],[False]], result[i+1], top_row_precursor, all_row_configs, is_first=True)
    _dfs_for_preimage(0, row, [[False],[True]], result[i+1], top_row_precursor, all_row_configs, is_first=True)
    _dfs_for_preimage(0, row, [[True],[True]], result[i+1], top_row_precursor, all_row_configs, is_first=True)
    print(result)
    
    for i in range(1, len(C)):
        result[i+1] = defaultdict(list)
        row = C[i]
        _dfs_for_preimage(0, row, [[False],[False]], result[i+1], top_row_precursor, all_row_configs)
        _dfs_for_preimage(0, row, [[True],[False]], result[i+1], top_row_precursor, all_row_configs)
        _dfs_for_preimage(0, row, [[False],[True]], result[i+1], top_row_precursor, all_row_configs)
        _dfs_for_preimage(0, row, [[True],[True]], result[i+1], top_row_precursor, all_row_configs)

    return result

def _get_top_to_bottom_maps_for_each_row(C):
    row_length = len(C[0])
    result = {1: defaultdict(list)}

    n_possible_rows = 2**(row_length+1)
    all_row_configs = [int2row(i, row_length+1) for i in range(n_possible_rows)]

    
    top_row_precursor = int2row(0, row_length+1)
    row = C[0]
    for r1 in all_row_configs:
        for r2 in all_row_configs:
            for c in range(row_length):
                s = r1[c] + r1[c+1] + r2[c] + r2[c+1]
                if (s == 1 and not row[c]) or (s != 1 and row[c]):
                    break
            else:
                result[1][(top_row_precursor, r1)].append((r1, r2))


    for i in range(1, len(C)):
        row = C[i]
        result[i+1] = defaultdict(list) 

        for r1 in all_row_configs:
            for r2 in all_row_configs:
                # check if bottom (r1, r2) is a valid precursor
                for c in range(row_length):
                    s = r1[c] + r1[c+1] + r2[c] + r2[c+1]
                    if (s == 1 and not row[c]) or (s != 1 and row[c]):
                        break
                else:
                    tops = [(top, r1) for top in all_row_configs]
                    for t in tops:
                        result[i+1][t].append((r1, r2))

    # for t, bs in result[1].items():
    #     print(t)
    #     for b in bs:
    #         print("\t{}".format(b[1]))
    #     print()
    return result


def aggregate_over_precursors(C):
    # row-indexed maps from the 2-bottoms of the partial precursors of C:1,r to
    # counts
    B_r_A = {} 

    # Cr-indexed (row config) from the 2-tops of all row precursors to 
    # corresponding sets of matching 2-bottoms
    T_Cr_Bs = _get_top_to_bottom_maps_for_each_row2(C)


    # initialize first row
    B_r_A[1] = Counter()
    for bs in T_Cr_Bs[1].values():
        for b in bs:
            B_r_A[1][b] += 1

    # process each subsequent row
    for r in range(2, len(C) + 1):
        B_r_A[r] = Counter()
        for b, a in B_r_A[r-1].items(): 
            for b_prime in T_Cr_Bs[r][b]:
                B_r_A[r][b_prime] += a 

    # return final aggregate
    return sum(B_r_A[len(C)].values())


def _transpose(l):
    return list(map(list, zip(*l)))


def solution(g):
    C = _transpose(g)

    return aggregate_over_precursors(C)




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
