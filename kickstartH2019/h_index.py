DEV = False

sample_text = """4
3
5 1 2
6
1 3 3 2 2 15
5
10 8 5 4 3
5
25 8 5 3 3
"""


if DEV:
    from collections import deque
    from unittest.mock import MagicMock
    sample_lines = deque(sample_text.split("\n"))

    input = MagicMock(side_effect=lambda : sample_lines.popleft())



def parse_input():
    T = int(input())
    test_cases = []
    for t in range(T):
        N = int(input())
        tc = list(map(int, input().split()))
        test_cases.append(tc)

    return test_cases

def h_index(papers):
    N = len(papers)

    h_indices = [0]*N
    citations = [0]*(N+1)
    for i, count in enumerate(papers):
        citations[min(count,N)] += 1
        result = cumsum = 0
        for j in reversed(range(1, N+1)):
            cumsum += citations[j]
            result = max(result, min(j, cumsum))
        h_indices[i] = result

    return " ".join(map(str, h_indices))


def main():
    for i, test_case in enumerate(parse_input()):
        print("Case #{}: {}".format(i+1, h_index(test_case)))

if __name__ == '__main__':
    main()
