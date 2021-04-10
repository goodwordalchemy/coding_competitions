from functools import lru_cache
DEV = True

sample_text = """6
5
2 2
3 1
5 2
7 1
11 1
1
17 2
2
2 2
3 1
1
2 7
1
2 1
1
2 2
"""


if DEV:
    from collections import deque
    from unittest.mock import MagicMock
    sample_lines = deque(sample_text.split("\n"))

    input = MagicMock(side_effect=lambda : sample_lines.popleft())



def parse_input():
    n_test_cases = int(input())
    test_cases = []
    for t in range(n_test_cases):
        M = int(input())
        counter = [] 
        for _ in range(M):
            p, n = list(map(int, input().split()))
            counter.append((p, n))
        yield counter

"""
As a first pass here, we will break the counter into a sorted list of all of the 
numbers.  Why? because it will be easier to do dynamic programming on such a 
thing, though it would not be impossible without it.

Then we will call dp(i, sum_so_far, prod_so_far).

One question I have is what to initialize_prod_so_far.  I think I just need a
condition that says if prod_so_far is 0, then just set it to whatever was 
passed in.


ways to improve:
* make it iterative.
"""


def prime_time(counter):
    @lru_cache(None)
    def dp(i, sum_so_far, prod_so_far):
        if i == len(counter):
            # print("counter={}, sum_so_far={}, prod_so_far={}".format(
            #     counter, sum_so_far, prod_so_far)
            # )
            return sum_so_far if sum_so_far == prod_so_far else 0

        if not prod_so_far:
            prod_so_far =  1

        p, n = counter[i]
        result = 0
        for j in range(0, n+1):
            result = max(
                result, 
                dp(i+1, sum_so_far + p*j, prod_so_far * p**(n-j))
            )
        return result

    score = dp(0, 0, 0)
    return str(score)



def main():
    for i, test_case in enumerate(parse_input()):
        print("Case #{}: {}".format(i+1, prime_time(test_case)))

if __name__ == '__main__':
    main()
