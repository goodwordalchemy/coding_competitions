import heapq
from math import ceil

DEV = True

samples = [(
"""3 1
100 200 230""", 50
), (
"""3 1
100 201 230""", 51
), (
"""3 1
1 2 3""", 1
), (
"""3 1
1 5 9""", 4
), (
"""5 2
10 13 15 16 17""", 2
), (
"""5 6
9 10 20 26 30""", 3
), (
"""8 3
1 2 3 4 5 6 7 10""", 1
),
]

sample_inputs, sample_outputs = zip(*samples)

sample_text  = str(len(samples))+'\n'+"\n".join(sample_inputs)
if DEV:
    print("expected output:\n")
    print("\n".join("EXPECT Case {}: {}".format(i+1, o) for i, o in enumerate(sample_outputs)))
    print()



if DEV:
    from collections import deque
    from unittest.mock import MagicMock
    sample_lines = deque(sample_text.split("\n"))

    input = MagicMock(side_effect=lambda : sample_lines.popleft())



def parse_input():
    n_test_cases = int(input())
    test_cases = []
    for t in range(n_test_cases):
        N, K = map(int, input().split())
        M = list(map(int, input().split()))
        test_cases.append((K, M))

    return test_cases


def workout_k_is_1(k, sessions):
    N = len(sessions)
    diffs = []
    for i in range(1, N):
        diffs.append(-(sessions[i]-sessions[i-1]))

    heapq.heapify(diffs)
    max_diff = -heapq.heappop(diffs)
    divided = max_diff // 2

    return max([
        divided,
        max_diff - divided,
        -heapq.heappop(diffs) if diffs else 0,
    ])

def count_ks(d_optimal, diffs):
    k = 0
    for d in diffs:
        # the "-1" is because one endpoint is not included
        k += ceil(d / d_optimal) - 1

    return k


def workout(k, sessions):
    N = len(sessions)
    diffs = []
    for i in range(1, N):
        diffs.append(sessions[i]-sessions[i-1])

    low = 1
    high = max(diffs)

    while low < high:
        guess = (low + high) // 2
        if count_ks(guess, diffs) > k:
            low = guess + 1
        else:
            high = guess

    return low



def main():
    for i, test_case in enumerate(parse_input()):
        print("Case #{}: {}".format(i+1, workout(*test_case)))

if __name__ == '__main__':
    main()
