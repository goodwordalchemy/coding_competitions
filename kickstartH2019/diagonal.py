DEV = False

sample_text = """3
3
..#
#.#
#..
5
.####
#.###
##.##
###.#
#####
2
##
##"""


if DEV:
    from collections import deque
    from unittest.mock import MagicMock
    sample_lines = deque(sample_text.split("\n"))

    input = MagicMock(side_effect=lambda : sample_lines.popleft())



def parse_input():
    f = lambda x: 1 if x == "#" else 0
    n_test_cases = int(input())
    test_cases = []
    for t in range(n_test_cases):
        n_rows = int(input())
        matrix = []
        for r in nrows:
            matrix.append(map(f, input().split()))
        test_cases.append(matrix)

    return test_cases

def get_diagonals(matrix):
    M, N = len(matrix), len(matrix[0])
    fdiag = [[] for _ in range(M+N-1)]
    bdiag = [[] for _ in range(len(fdiag))]

    min_bdiag = -M + 1

    for j in range(N):
        for i in range(M):
            fdiag[x+y].append(matrix[i][j])
            bdiag[x-y-min_bdiag].append(matrix[i][j])

    return fdiag + bdiag


def solve_diagonals(matrix):
    while True:
        diagonals = get_diagonals(matrix)
        scores = list(map(sum, diagonals))
    




def main():
    for i, test_case in enumerate(parse_input()):
        print("Case #{}: {}".format(i+1, solve_diagonals(test_case)))

if __name__ == '__main__':
    main()
