import heapq

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
    citations = []
    for i, count in enumerate(papers):
        # slightly buggy to go around the corner here...
        h_indices[i] = h_indices[i-1]

        if count > h_indices[i]:
            heapq.heappush(citations, count)

        while citations and citations[0] <= h_indices[i]:
            heapq.heappop(citations)

        if len(citations) >= h_indices[i] + 1:
            h_indices[i] += 1

    return " ".join(map(str, h_indices))


def main():
    for i, test_case in enumerate(parse_input()):
        print("Case #{}: {}".format(i+1, h_index(test_case)))

if __name__ == '__main__':
    main()
