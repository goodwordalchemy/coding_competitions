import random

def int2row(i, row_length):
    return tuple([bool(int(b)) for b in bin(i)[2:].rjust(row_length, '0')])


def gen_board(rows, cols):
    assert 3 <= rows <= 50
    assert 3 <= cols <= 9

    return [
        [random.random() > 0.5 for c in range(cols)]
        for r in range(rows)
    ]
    
def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    result = []
    for i in range(0, len(lst), n):
        result.append( lst[i:i + n])
    return result

def is_valid_preimage(preimage, board):
    rows = len(board)
    cols = len(board[0])

    for row in range(rows):
        for col in range(cols):
            s = sum([
                preimage[row][col],
                preimage[row+1][col],
                preimage[row][col+1],
                preimage[row+1][col+1],
            ])
            if (s == 1 and not board[row][col]) or (s != 1 and board[row][col]):
                return False
    return True

def count_solutions(board):
    rows = len(board)
    cols = len(board[0])

    result = 0
    for i in range(2**((rows+1) * (cols+1))):
        candidate = chunks(int2row(i, (rows+1) * (cols+1)), (cols+1))

        result += is_valid_preimage(candidate, board)

    return result




test_cases = [
    (
        ([[True, False, True], [False, True, False], [True, False, True]],),
        4,
    ),
]

for (board,), ans in test_cases:
    assert count_solutions(board) == ans, (count_solutions(board), ans)


sizes = [
    # (3, 3),
    # (3, 4),
    # (4, 3),
	# (5, 3),
	# (3, 5),	
	# (50, 9),
	# (50, 9),
	# (50, 9),
]

for rows, cols in sizes:
	board = gen_board(rows, cols)
	
	print("(({},),{}),".format(board, count_solutions(board)))
	

