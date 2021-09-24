from collections import deque


def solution(x, y):
    mx, fx = int(x), int(y)

    start = (1, 1)
    queue = deque([start])
    visited = {start}

    depth = 0
    while queue:
        for _ in range(len(queue)):
            m, f = queue.popleft()

            if m == mx and f == fx:
                return str(depth)

            mff = (m + f, f)
            if m + f <= mx and mff not in visited:
                queue.append(mff)
                visited.add(mff)


            mmf = (m, m + f)
            if m + f <= fx and mmf not in visited:
                queue.append(mmf)
                visited.add(mmf)

        depth += 1

    return 'impossible'
        


test_cases = [
    (
        solution('4', '7'),
        4
    ), (
        solution('2', '1'), 
        1
    ), (
        solution('2', '1'), 
        1
    ), (
        solution('3', '3'),
        'impossible'
    ), (
        solution('10000', '10000'),
        'idk'
    )
]

for a, e in test_cases:
    print("{} == {}".format(a, e))
