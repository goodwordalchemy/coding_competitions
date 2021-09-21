DEV = True

sample_text = """7
3
111
6
100100
11
00100100010
3
001
3
100
3
101
4
1001
"""


if DEV:
    from collections import deque
    from unittest.mock import MagicMock
    sample_lines = deque(sample_text.split("\n"))

    input = MagicMock(side_effect=lambda : sample_lines.popleft())



def parse_input():
    n_test_cases = int(input())
    for t in range(n_test_cases):
        n_houses = int(input())
        cans = input()
        yield cans

def solution(cans):
    """
    need to find the closest can to each house.

    well really distance to closest can.

    Can do this in two passes, forward and backward.

    initialize a vector of all infinites.

    In a pass, keep track of the position of the last bin.
    for forward, last bin starts at -infinite.
    """
    max_dist = len(cans) + 1
    distances = [max_dist] * len(cans)

    # forward pass
    last_bin = -max_dist
    for i in range(len(cans)):
        has_can = int(cans[i])
        if int(has_can):
            last_bin = i
        distances[i] = min(distances[i], abs(last_bin - i))


    # reverse pass
    last_bin = max_dist * 2
    for i in reversed(range(len(cans))):
        has_can = int(cans[i])
        if int(has_can):
            last_bin = i
        distances[i] = min(distances[i], abs(last_bin - i))


    return sum(distances)


def sum_series(n):
    return n * (n + 1) // 2

def _debug(*x):
    if DEV:
        print(*x)

def solution2(houses):
    """
    you don't need to loop over all of the cans.

    instead, you can 
    * all houses before first can must go to first can.
    * all houses after last can must go to last can.
    * for houses in between cans can be split by midpoint.  If there is an 
      odd number just break ties arbitrarily.

    key question is how to know sum of numbers between a and b.

    it's ((b - a + 1) * (a + b)) // 2
    """
    _debug(houses)
    result = 0
    i = 0

    # up to first can
    for i in range(len(houses)):
        has_can = int(houses[i])
        if has_can:
            break
        
    last_can = i
    result += sum_series(last_can)
    _debug(result)

    while i < len(houses) - 1:
        i += 1
        has_can = int(houses[i])
        if has_can:
            dist = i - last_can  - 1
            result += sum_series(dist // 2)
            if dist % 2 == 0:
                result += sum_series(dist // 2)
            else:
                result += sum_series(dist // 2 + 1)
            last_can = i
            _debug(result)

    result += sum_series(len(houses) - last_can - 1)
    _debug(result)
 
    return result
            

def main():
    for i, test_case in enumerate(parse_input()):
        print("Case #{}: {}".format(i+1, solution2(test_case)))

if __name__ == '__main__':
    main()
