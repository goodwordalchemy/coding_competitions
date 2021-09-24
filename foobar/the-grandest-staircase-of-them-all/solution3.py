
from functools import lru_cache


MAX = 210

def get_leader_height_by_n():
    E = [0] * (MAX + 4)
    idx = 1
    for i in range(1, MAX):
        for j in range(i):
            E[idx] = i
            idx += 1
            if idx >= len(E):
                return E

    return E


def solution(n):
    E = get_leader_height_by_n()


    dp = [[0 for _ in range(MAX+1)] for __ in range(MAX+1)]

    for i in range(MAX+1):
        dp[i][0] = 1

    for i in range(1, MAX+1):
        dp[i][1] = 1

    for i in range(2, MAX+1):
        dp[i][2] = 1


    for bricks in range(3, MAX+1):
        leader_height = E[bricks]

        dp[leader_height][bricks] = dp[leader_height-1][bricks-leader_height]
        for max_height in range(leader_height+1, bricks):
            dp[max_height][bricks] = (
                dp[max_height-1][bricks] + 
                dp[max_height-1][bricks - max_height]
            )

        dp[bricks][bricks] = dp[bricks-1][bricks] + 1

        for height in range(bricks+1, MAX+1):
            dp[height][bricks] = dp[height-1][bricks]


    return dp[n-1][n] 


print(get_leader_height_by_n())
print()

test_cases = [
    (solution(3), 1),
    (solution(4), 1),
    (solution(5), 2),
    (solution(6), 3),
    (solution(7), 4),
    (solution(8), 5),
    (solution(9), 7),
    (solution(10), 9),
    (solution(11), 12),
    (solution(200), 487067745),
]

print(list(enumerate(get_leader_height_by_n())))

for a, e in test_cases:
    print("{} == {}".format(a, e))
    print()

