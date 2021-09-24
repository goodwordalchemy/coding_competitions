from functools import lru_cache

@lru_cache(None)
def dp(bricks, prev_height):
    if bricks == 0:
        return 1
    elif prev_height == 1:
        return 0

    result = 0
    for i in reversed(range(1, prev_height)):
        result += dp(bricks - i, i)

    return result


def solution(n):
    result = 0
    for i in reversed(range(1, n)):
        result += dp(n-i, i)

    print(result)
    return result


test_cases = [
    (solution(3), 1),
    (solution(4), 1),
    (solution(5), 2),
    (solution(6), 3),
    (solution(7), 4),
    (solution(8), 5),
    (solution(9), 7),
    (solution(200), 487067745),
]

for a, e in test_cases:
    print("{} == {}".format(a, e))
    print()
