import math

DEBUG = False
test_data = """4
3
2 2 6
5
30 30 9 1 30
4
4 0 0 16
4
4 -1 1 16
"""

if DEBUG:
    from unittest.mock import MagicMock

    input = MagicMock(side_effect=test_data.split("\n"))

def parse_input():
    cases = []
    n_cases = int(input())
    for _ in range(n_cases):
        __ = input()
        cases.append(map(int, input().split()))

    return cases

def perfect_squares(nums):
    prefix = [0]
    for elt in nums:
        prefix.append(prefix[-1]+elt)

    result = 0
    N = len(prefix)

    for start in range(N-1):
        for end in range(start+1, N):
            diff = prefix[end] - prefix[start]
            if diff < 0:
                continue
            root = math.sqrt(diff)
            if root == int(root):
                result += 1

    return result

def main():
    cases = parse_input()
    for i, nums in enumerate(cases):
        print("Case #{}: {}".format(i+1, perfect_squares(nums)))



if __name__ == '__main__':
    main()

