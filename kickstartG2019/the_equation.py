import math

DEV = True


samples = [(
"""3 27
8 2 4""", 12
), (
"""4 45
30 0 4 11""", 14
), (
"""1 0
100""", 100
), (
"""0 0
100""", 100
), (
"""6 2
5 5 1 5 1 0""", -1
)]

sample_inputs, sample_outputs = zip(*samples)

sample_text  = str(len(samples))+'\n'+"\n".join(sample_inputs)
if DEV:
    print("expected output:\n")
    print("\n".join("EXPECT Case {}: {}".format(i+1, o) for i, o in enumerate(sample_outputs)))
    print()



if DEV:
    from collections import deque
    from unittest.mock import MagicMock
    sample_lines = deque(sample_text.split("\n"))

    input = MagicMock(side_effect=lambda : sample_lines.popleft())



def parse_input():
    n_test_cases = int(input())
    test_cases = []
    for t in range(n_test_cases):
        N, M = map(int, input().split())
        A = list(map(int, input().split()))
        yield (M, A)

def count_bits(n):
    if n == 0:
        return 1
    return int(math.log2(n)) + 1

def the_equation_slow(M, A):
    top = max(M, max(A))
    for i in reversed(range(top+1)):
        total = 0
        for a in A:
            total += i ^ a
        if total <= M:
            return i
    return -1

def the_equation(M, A):
    nbits = count_bits(M)
    assert nbits == len(bin(M)[2:])

    result = 0
    for i in reversed(range(nbits)):
        cur = 0
        for a in A:
            if (1 << i) ^ a:
                cur += 1
        if result + cur*(1<<i) <= M:
            result += cur*(1<<i)
            print("good i={}, result={}".format(i, result))
    return result


def main():
    for i, test_case in enumerate(parse_input()):
        print("Case #{}: {}".format(i+1, the_equation(*test_case)))

if __name__ == '__main__':
    main()
