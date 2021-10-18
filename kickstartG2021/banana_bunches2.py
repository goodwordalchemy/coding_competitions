"""
this solution improves on the previous by iterating all triplets
and then finding an end for interval2 that makes the sum of bananas = K.

"""
from collections import defaultdict

DEV = False
DEBUG = DEV and False
if DEV and not DEBUG:
    print("(dev is on but debug mode is off)")

def _debug(*args, debug=DEBUG):
    if debug:
        print(*args)

# lives outside of DEV conditional because easier to format
test_cases = [(
"""6 8
1 2 3 1 2 3
""", 3
),(
"""4 10
6 7 5 2
""", -1
),(
"""6 8
3 1 2 1 3 1
""", 4 
),(
"""4 6
3 1 2 0
""", 3
),(
"""4 3
10 1 2 10
""", 2
),(
"""3 1
10 1 10
""", 1
),(
"""4 12
10 0 2 3
""", 2
),(
"""6 12
10 0 1 0 1 3
""", 4
),(
"""7 12
10 0 0 1 0 1 3
""", 4
),(
"""7 12
10 0 1 0 0 1 3
""", 4
),(
"""7 15
10 0 1 0 1 0 0 0 3
""", 6
)]


if DEV:
    from collections import deque
    from unittest.mock import MagicMock


    test_inputs, test_outputs = zip(*test_cases)

    sample_text = str(len(test_cases)) + "\n" + "".join(test_inputs)

    sample_lines = deque(sample_text.split("\n"))
    input = MagicMock(side_effect=lambda : sample_lines.popleft())


def parse_input():
    t_test_cases = int(input())
    test_cases = []
    for t in range(t_test_cases):
        N, K = list(map(int, input().split()))
        B = list(map(int, input().split()))
        yield (K, B)


def solution(K, B):
    prefix = [0]
    for elt in B:
        if elt == K:
            return 1
        prefix.append(prefix[-1] + elt)

    N = len(B)
    result = float('inf')

    for i in range(N):
        if prefix[N] - prefix[i] < K:
            break
        for y in range(i+1, N):
            cur_sum = prefix[y+1] - prefix[i]
            if cur_sum == K:
                _debug("cur_sum == K...i={}, y={}".format(i, y))
                result = min(result, y - i + 1)
            elif cur_sum < K:
                continue

            j = i+1
            for x in range(j, y):
                diff = prefix[x+1] - prefix[j]
                if cur_sum - diff == K:
                    _debug("yo", i, j, x, y)
                    result = min(result, y - i + 1  - (x - j + 1))
                while j < x and cur_sum - diff <= K:
                    if B[x] == 0 and B[j] == 0:
                        break
                    j += 1
                    diff = prefix[x+1] - prefix[j]
                    if cur_sum - diff == K:
                        _debug("this", i, j, x, y, y - i + 1  - (x - j + 1))
                        result = min(result, y - i + 1  - (x - j + 1))
                    else:
                        _debug("else", i, j, x, y)

    return result if result < float('inf') else -1


# deprecated
def solution_binary_search(K, B):
    prefix = [0]
    for elt in B:
        if elt == K:
            return 1
        prefix.append(prefix[-1] + elt)



    N = len(B)
    result = float('inf')
    for i in range(N-1):
        for j in range(i, N-1):
            for x in range(j+1, N):
                sum_so_far = prefix[j+1] - prefix[i]
                low = x
                high = N-1
                while low < high:
                    guess = (low + high) // 2
                    if prefix[guess+1] - prefix[x] < K - sum_so_far:
                        low = guess + 1
                    else:
                        high = guess
                assert low == high
                _debug(i, j, x, high)
                if prefix[high+1] - prefix[x] == K - sum_so_far:
                    _debug(prefix[j+1]-prefix[i], prefix[high+1]-prefix[x])
                    tmp = j - i + 1 + high - x + 1
                    _debug("found: {}".format(tmp))
                    result = min(result, tmp)

    return result if result < float('inf') else -1



def main():
    for i, test_case in enumerate(parse_input()):
        _debug("Data #{}: {}".format(i+1, test_case))
        result = solution(*test_case)
        if DEV:
            assert result == test_outputs[i], "\ngot:\n{}\n\nexpected:\n{}".format(
                result, test_outputs[i]
            )
        print("Case #{}: {}".format(i+1, result))
        _debug()

if __name__ == '__main__':
    main()
