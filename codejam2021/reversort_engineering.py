from itertools import permutations

DEV = True

sample_text = """5
4 6
2 1
7 12
7 2
2 1000
"""


if DEV:
    from collections import deque
    from unittest.mock import MagicMock
    sample_lines = deque(sample_text.split("\n"))

    input = MagicMock(side_effect=lambda : sample_lines.popleft())



def parse_input():
    n_test_cases = int(input())
    test_cases = []
    for t in range(n_test_cases):
        n, c = list(map(int, input().split()))
        test_cases.append((n, c))

    return test_cases

def argmin(L):
    best_val = float('inf')
    best_idx = -1
    for idx, val in enumerate(L):
        if val < best_val:
            best_val = val
            best_idx = idx
    return best_idx

def reversort(L):
    result = 0
    for i in range(len(L)-1):
        j = argmin(L[i:])
        # print(L[i:])
        # print(j)
        result += j+1
        L[i:i+j+1] = list(reversed(L[i:i+j+1]))
    return result

def reversort_engineering_slow(n, c):
    for o_perm in permutations(range(1, n+1)):
        perm = list(o_perm)
        if reversort(perm) == c:
            return " ".join(map(str, o_perm))
    return "IMPOSSIBLE"

IMPOSSIBLE = "IMPOSSIBLE"


def subset_summing_to_c(n, c):
    def dp(i, c, so_far):
        if i == n+1:
            return False

        so_far.append(i)
        c -= i

        if c == 0:
            return True

        if c < 0:
            c += i
            so_far.pop()
            return False

        for j in range(i+1, n+1):
            if dp(j, c, so_far):
                return True

        c += i
        so_far.pop()
        return False
    
    result = []
    if dp(2, c, result):
        return result
    return None
    

def reversort_engineering(n, c):
    if c < n:
        return IMPOSSIBLE

    c -= n
    if c == 0:
        return list(range(1, n+1))
    subset = subset_summing_to_c(n, c)

    if subset is None:
        return IMPOSSIBLE

    subset.sort()
    nums = list(range(1, n+1))
    for i in subset:
        nums[-1-i:] = list(reversed(nums[-1-i:]))

    return " ".join(map(str, nums))

def main():
    for i, test_case in enumerate(parse_input()):
        print("Case #{}: {}".format(i+1, reversort_engineering(*test_case)))

if __name__ == '__main__':
    main()
