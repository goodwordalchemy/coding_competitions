
from functools import lru_cache

@lru_cache(None)
def dp(bricks):
    if bricks == 0:
        return 0

    elif bricks <= 2:
        return 1

    result = 0
    for i in range(1, bricks):
        result += dp(bricks - i)

    return result


def solution(n):
    result = 0
    for i in range(1, n):
        result += dp(n-i)

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
    (solution(10), 10),
    (solution(11), 12),
    (solution(200), 487067745),
]

for a, e in test_cases:
    print("{} == {}".format(a, e))
    print()
