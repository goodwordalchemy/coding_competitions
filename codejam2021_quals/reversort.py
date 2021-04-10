DEV = True

sample_text = """3
4
4 2 1 3
2
1 2
7
7 6 5 4 3 2 1
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
        n = int(input())
        L = list(map(int, input().split()))
        test_cases.append(L)

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




def main():
    for i, test_case in enumerate(parse_input()):
        print("Case #{}: {}".format(i+1, reversort(test_case)))

if __name__ == '__main__':
    main()
