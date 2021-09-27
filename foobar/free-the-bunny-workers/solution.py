from itertools import combinations

def solution(num_buns, num_required):
    result = [[] for _ in range(num_buns)]

    combos = combinations(range(num_buns), num_buns - num_required + 1)

    for i, comb in enumerate(sorted(combos)):
        for bun in comb:
            result[bun].append(i)

    return result

test_cases = [
    (
        (6, 4),
        ["whatever"]
    ), (
        (5, 2),
        ["whatever"]
    ), (
        (3, 1),
        [ [0], [0], [0], ]
    ), (
        (2, 2),
        [ [0], [1], ]
    ), (
        (2, 1),
        [[0], [0]]
    ), (
        (3, 2),
        [
          [0, 1],
          [0, 2],
          [1, 2],
        ]
    ), (
        (5, 3),
        [[0, 1, 2, 3, 4, 5], [0, 1, 2, 6, 7, 8], [0, 3, 4, 6, 7, 9], [1, 3, 5, 6, 8, 9], [2, 4, 5, 7, 8, 9]]
    ), (
        (4, 4),
        [[0], [1], [2], [3]]
    )
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
            "expected:\n{}".format("\n".join(map(str,ans))),
            "actual:\n{}".format("\n".join(map(str,result))),
        ]))

