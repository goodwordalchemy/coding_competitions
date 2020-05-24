DEV = True

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
sample_text = """1
5
.####
#.###
##.##
###.#
#####
"""

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
        for r in range(n_rows):
            matrix.append(list(map(f, input())))
        test_cases.append(matrix)

    return test_cases


def get_diagonals(matrix):
    M, N = len(matrix), len(matrix[0])
    fdiag = [[] for _ in range(M+N-1)]
    bdiag = [[] for _ in range(len(fdiag))]

    min_bdiag = -M + 1

    for j in range(N):
        for i in range(M):
            fdiag[i+j].append((i, j))
            bdiag[j-i-min_bdiag].append((i,j))

    mainf = fdiag[(M+N-1) // 2]
    mainb = bdiag[(M+N-1) // 2]

    return mainf, mainb, fdiag, bdiag

def flip(matrix, diagonal_cells):
    for row, col in diagonal_cells:
        matrix[row][col] = not matrix[row][col]

    return 1

def solve_diagonals(matrix):
    # key insight is that a solutions is guaranteed, and one would never
    # flip the same diagonal twice.

    main_diagonal_flip_cases = [
        (False, False),
        (True, False),
        (False, True),
        (True, True),
    ]

    mainf, mainb, fdiag, bdiag = get_diagonals(matrix)
    # print("\nfdiags:")
    # for fd in fdiag:
    #     print(fd)
    # print("\nbdiags:")
    # for bd in bdiag:
    #     print(bd)
    # print("\nmainf: {}".format(mainf)) 
    # print("\nmainb: {}".format(mainb)) 
    # import ipdb; ipdb.set_trace()

    best = float('inf')
    for flip_f, flip_b in main_diagonal_flip_cases:
        n_flips = 0

        if flip_f:
            n_flips += flip(matrix, mainf)
        if flip_b:
            n_flips += flip(matrix, mainb)

        for i, (row, col) in enumerate(mainf):
            if not matrix[row][col]:
                n_flips += flip(matrix, bdiag[i*2])

        for i, (row, col) in enumerate(mainb):
            if not matrix[row][col]:
                n_flips += flip(matrix, fdiag[i*2])

        if all(map(all, matrix)):
            best = min(best, n_flips)

    return best


def main():
    for i, test_case in enumerate(parse_input()):
        print("Case #{}: {}".format(i+1, solve_diagonals(test_case)))

if __name__ == '__main__':
    main()
