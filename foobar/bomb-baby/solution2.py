from functools import lru_cache

@lru_cache()
def pulverize(x, y, depth=0):
    print(x, y)
    if depth == 10:
        assert False, "too de3p"
    if x < y:
        return pulverize(y, x, depth)
    if x < 0 or y < 0:
        return float('inf')
    if x == 0 and y == 0:
        return 0

    return 1 + min(pulverize(x, y-x, depth+1), pulverize(y, x-y, depth+1))

def solution(x, y):
    result = pulverize(int(x), int(y))

    if result == float('inf'):
        return 'impossible'
    else:
        return str(result)


test_cases = [
    (
        solution('4', '7'),
        4
    # ), (
    #     solution('2', '1'), 
    #     1
    # ), (
    #     solution('2', '1'), 
    #     1
    # ), (
    #     solution('3', '3'),
    #     'impossible'
    # ), (
    #     solution('10000', '10000'),
    #     'idk'
    )
]

for a, e in test_cases:
    print("{} == {}".format(a, e))
