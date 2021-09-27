from collections import Counter, defaultdict

"""
O(n**2) where n is 2**len(row)

in this CA, top row does not matter.
for each middle row config
"""

def int2row(i, row_length):
    return tuple([bool(int(b)) for b in bin(i)[2:].rjust(row_length, '0')])


def _get_top_to_bottom_maps_for_each_row(C):
    row_length = len(C[0])
    result = {}

    n_possible_rows = 2**(row_length+1)
    all_row_configs = [int2row(i, row_length+1) for i in range(n_possible_rows)]

    for i, row in enumerate(C):
        result[i+1] = defaultdict(list) 

        for r1 in all_row_configs:
            for r2 in all_row_configs:

                # check if bottom (r1, r2) is a valid precursor
                for c in range(row_length):
                    s = r1[c] + r1[c+1] + r2[c] + r2[c+1]
                    if (s == 1 and row[c]) or (s != 1 and not row[c]):
                        tops = [(top, r1) for top in all_row_configs]
                        for t in tops:
                            result[i+1][t].append((r1, r2))
    print(result)
    return result


def aggregate_over_precursors(C):
    # row-indexed maps from the 2-bottoms of the partial precursors of C:1,r to
    # counts
    B_r_A = {} 

    # Cr-indexed (row config) from the 2-tops of all row precursors to 
    # corresponding sets of matching 2-bottoms
    T_Cr_Bs = _get_top_to_bottom_maps_for_each_row(C)


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
                B_r_A[r][b_prime] += a + 1

    # return final aggregate
    return sum(B_r_A[len(C)].values())


def _transpose(l):
    return list(map(list, zip(*l)))


def solution(g):
    C = _transpose(g)

    return aggregate_over_precursors(C)




test_cases = [
    (
        ([[False]],),
       12
    ),
    # (
    #     ([[True]],),
    #    4 
    # ),
    # (
    #     ([[True, False, True], [False, True, False], [True, False, True]],),
    #     4,
    # ),
	# (
    #     ([[True, False, True, False, False, True, True, True], [True, False, True, False, False, False, True, False], [True, True, True, False, False, False, True, False], [True, False, True, False, False, False, True, False], [True, False, True, False, False, True, True, True]],),
    #     254
    # ),
	# (
    #     ([[True, True, False, True, False, True, False, True, True, False], [True, True, False, False, False, False, True, True, True, False], [True, True, False, False, False, False, False, False, False, True], [False, True, False, False, False, False, True, True, False, False]],),
    #     11567
	# ), 
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
