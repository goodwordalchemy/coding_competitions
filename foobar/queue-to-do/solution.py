def xor_to(n):
    if n % 4 == 0:
        return n
    elif n % 4 == 1:
        return 1
    elif n % 4 == 2:
        return n + 1
    elif n % 4 == 3:
        return 0
    
    assert False, "Impossible"


def xor_range(l, r):
    return xor_to(l-1) ^ xor_to(r)


def solution(start, length):
    # print()
    leader = start

    result = 0

    for n_checked in reversed(range(1, length+1)):
        # print("start={}, end={}, row_result={}".format(
        #     leader, leader+n_checked-1,
        #     xor_range(leader, leader + n_checked - 1)
        # ))
        result ^= xor_range(leader, leader + n_checked-1)
        leader += length

    return result


test_cases = [
    (solution(0, 3), 2),
    (solution(17, 4), 14),
]

for a, e in test_cases:
    print("{} == {}".format(a, e))
    print()

