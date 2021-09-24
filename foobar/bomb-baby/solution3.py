def pulverize(x, y):
    print('{} {}'.format(x, y))
    if x > y:
        return pulverize(y, x)
    if x == 1:
        return y - 1
    if x < 1 or y < 1:
        return float('inf')

    return (y / x) + pulverize(x, y % x)


def solution(x, y):
    print('')
    result = pulverize(int(x), int(y))

    if result == float('inf'):
        return 'impossible'
    else:
        return str(result)


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
        solution('4', '3'),
        3
    ), (
        solution('100', '100001'),
        'idk'
    )
]

for a, e in test_cases:
    print("{} == {}".format(a, e))
    print()
