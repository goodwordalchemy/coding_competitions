DEV = True

samples = [(
"""11 1 2
8
2 3""", 7
), (
"""11 11 11
1 2 3 4 5 6 7 8 9 10 11
1 2 3 4 5 6 7 8 9 10 11""", 9
), (
"""1000 6 1
4 8 15 16 23 42
1""", 994
)]

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
        N, M, Q = map(int, input().split())
        P = map(int, input().split())
        R = map(int, input().split())
        yield (N, P, R)


def book_reading(N, pages, readers):
    pages = set(pages)
    result = 0
    for r in readers:
        for m in range(r, N+1, r):
            if m in pages:
                continue
            result += 1
            # print("reader={}, just read = {}, n read={},  pages={}".format(r, m, result, pages))

    return result

def main():
    for i, test_case in enumerate(parse_input()):
        print("Case #{}: {}".format(i+1, book_reading(*test_case)))

if __name__ == '__main__':
    main()
