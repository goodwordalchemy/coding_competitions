DEBUG = False
test_data = """5
12 3
1 2 3 7 9 3 2 1 8 3 2 1
4 2
101 100 99 98
9 6
100 7 6 5 4 3 2 1 100
5 1
1 1 1 1 1
12 3
3 2 2 1 3 3 2 1 3 2 1 1
"""

if DEBUG:
    from unittest.mock import MagicMock

    input = MagicMock(side_effect=test_data.split("\n"))

def parse_input():
    cases = []
    n_cases = int(input())
    for _ in range(n_cases):
        n, k = list(map(int, input().split()))
        case = list(map(int, input().split()))
        cases.append((k, case))

    return cases

def countdown(nums, k):
    result = 0

    cur = 0
    for i in reversed(range(len(nums))):
        n = nums[i]
        if n == 1:
            cur = 1
        elif n == cur + 1:
            cur += 1
        else:
            cur = 0

        if cur == k:
            result += 1
            cur = 0
    return result

def main():
    cases = parse_input()
    for i, (k, nums) in enumerate(cases):
        print("Case #{}: {}".format(i+1, countdown(nums, k)))



if __name__ == '__main__':
    main()

