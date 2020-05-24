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

if DEV:
    from collections import deque
    from unittest.mock import MagicMock
    sample_lines = deque(sample_text.split("\n"))

    input = MagicMock(side_effect=lambda : sample_lines.popleft())



def parse_input():
    f = lambda x: True if x == "#" else False
    n_test_cases = int(input())
    test_cases = []
    for t in range(n_test_cases):
        n_rows = int(input())
        matrix = []
        for r in range(n_rows):
            matrix.append(list(map(f, input())))
        test_cases.append(matrix)

    return test_cases


def get_diagonals(matrix, second_largest_backward=False):
    M, N = len(matrix), len(matrix[0])
    fdiag = [[] for _ in range(M+N-1)]
    bdiag = [[] for _ in range(len(fdiag))]

    min_bdiag = -M + 1

    for j in range(N):
        for i in range(M):
            fdiag[i+j].append((i, j))
            bdiag[j-i-min_bdiag].append((i,j))

    mainf = fdiag[(M+N-1) // 2]

    if second_largest_backward:
        mainb = bdiag[max(0, (M+N-1) // 2-1)]
    else:
        mainb = bdiag[(M+N-1) // 2]

    return mainf, mainb, fdiag, bdiag

def flip(matrix, diagonal_cells):
    for row, col in diagonal_cells:
        matrix[row][col] = not matrix[row][col]

    return 1

def print_matrix(matrix):
    for r in matrix:
        print(r)

def solve_diagonals(matrix):
    # key insight is that a solutions is guaranteed, and one would never
    # flip the same diagonal twice.

    # print("orig...")
    # print_matrix(matrix)
    # print()

    main_diagonal_flip_cases = [
        (False, False),
        (True, False),
        (False, True),
        (True, True),
    ]

    is_odd = len(matrix)&1
    mainf, mainb, fdiag, bdiag = get_diagonals(matrix, is_odd)

    matrix_copy = matrix

    best = float('inf')
    for flip_f, flip_b in main_diagonal_flip_cases:
        matrix = [r.copy() for r in matrix_copy]
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
                n_flips += flip(matrix, fdiag[i*2+is_odd])

        for fd in fdiag:
            if all(not matrix[f[0]][f[1]] for f in fd):
                n_flips += flip(matrix, fd)


        if all(map(all, matrix)):
            best = min(best, n_flips)

        #print("\nfor case of flip_f={}, flip_b={}".format(flip_f, flip_b))
        #print_matrix(matrix)

    return best


def main():
    for i, test_case in enumerate(parse_input()):
        print("Case #{}: {}".format(i+1, solve_diagonals(test_case)))

if __name__ == '__main__':
    main()
