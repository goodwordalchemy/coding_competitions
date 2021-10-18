DEV = True

sample_text = """2
3
0 0 1 1
2 3 4 6
0 3 5 9
1
0 0 1 1
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

def distance_to_object(x, y, o):
    dx = 0 if x > o[0] and x < o[2] else min(abs(x-o[0]), abs(x-o[2]))
    dy = 0 if y > o[1] and y < o[3] else min(abs(y-o[1]), abs(y-o[3]))

    return dx + dy

def solution(objects):
    shortest_distance = float('inf')
    cur_x = 101
    cur_y = 101
    for i in range(-100, 101):
        for j in range(-100, 101):
            distance = sum(distance_to_object(i, j, o) for o in objects)
            should_update = distance < shortest_distance
            should_update |= distance == shortest_distance and i < cur_x
            should_update |= (distance == shortest_distance and 
                              i == cur_x and
                              j < cur_y
                             )
            if should_update:
                cur_x = i
                cur_y = j
                shortest_distance = distance

    return "{} {}".format(cur_x, cur_y)
            


def main():
    for i, test_case in enumerate(parse_input()):
        print("Case #{}: {}".format(i+1, solution(test_case)))

if __name__ == '__main__':
    main()
