"""
improved approach to this problem...

for the optimal x coordinate, 
    let a(x) = number of right sides of objects x is to the right of.
    let b(x) = number of left sides of objects x is to the left of.

* when a(x) == b(x), that is the optimal coordinate.
* after this point, any movement to the right improves the solution by
b(x) - a(x).
* this works when there is an even number of objects, 
* works when there is an odd number of objects
* works when there is an overlap.

One open question is whether it matters where in the range when a(x) == b(x)
we are.

"""
DEV = True

sample_text = """5
3
0 0 1 1
2 3 4 6
0 3 5 9
1
0 0 1 1
2
1 2 2 3
3 1 4 2
3
1 3 2 4
3 1 4 2 
5 2 6 4
2
1 3 3 4
2 1 4 2
"""



if DEV:
    from collections import deque
    from unittest.mock import MagicMock
    sample_lines = deque(sample_text.split("\n"))

    input = MagicMock(side_effect=lambda : sample_lines.popleft())



def parse_input():
    t_test_cases = int(input())
    test_cases = []
    for t in range(t_test_cases):
        K = int(input())
        objects = []
        for _ in range(K):
            objects.append(list(map(int, input().split())))

        yield objects


START = 1
END = 0

def line_sweep_for_optimal_coordinate(coords):
    """
    let a(x) = number of right sides of objects x is to the right of.
    let b(x) = number of left sides of objects x is to the left of.
    """
    assert len(coords) % 2 == 0

    a = len(coords) // 2
    b = 0

    for c, side, _ in coords:
        if side == START:
            b += 1
        else:
            a -= 1

        if a <= b:
            return c


def solution(objects):
    xs = []
    ys = []

    for i, (x1, y1, x2, y2) in enumerate(objects):
        xs.append((x1, START, i))
        xs.append((x2, END, i))
        ys.append((y1, START, i))
        ys.append((y2, END, i))

    xs.sort()
    ys.sort()

    x = line_sweep_for_optimal_coordinate(xs)
    y = line_sweep_for_optimal_coordinate(ys)

    return "{} {}".format(x, y)




def main():
    for i, test_case in enumerate(parse_input()):
        print("Case #{}: {}".format(i+1, solution(test_case)))

if __name__ == '__main__':
    main()
