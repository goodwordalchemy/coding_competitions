from collections import Counter

DEV = True

sample_text = """7
3
012
4
0145
5
00000
11
98765432101
2
01
1
1
2
10
"""


if DEV:
    from collections import deque
    from unittest.mock import MagicMock
    sample_lines = deque(sample_text.split("\n"))

    input = MagicMock(side_effect=lambda : sample_lines.popleft())


CACHE_TO_LENGTH = 4

substitutions = [
    ("01", "2"),
    ("12", "3"),
    ("23", "4"),
    ("34", "5"),
    ("45", "6"),
    ("56", "7"),
    ("67", "8"),
    ("78", "9"),
    ("89", "0"),
    ("90", "1"),
]

def parse_input():
    n_test_cases = int(input())
    for t in range(n_test_cases):
        _ = input()
        N = input()
        yield (N,)


def do_substitutions(N):
    cur = list(N)

    for to_sub, sub_to in substitutions:
        i = 0
        result = []
        while i < len(cur):
            if i == len(cur) - 1:
                result.append(cur[-1])
                break

            two = "".join(cur[i:i+2])
            if two == to_sub:
                result.append(sub_to)
                i += 1
            else:
                result.append(cur[i])
            i += 1
        cur = result


    # print("N", "".join(N))
    # print("cur", "".join(cur))
    return cur


def solution1(N):
    prev = list(N)
    cur = do_substitutions(prev)

    while prev != cur:
        prev = cur
        cur = do_substitutions(prev)

    return "".join(cur)


"""
the idea is to get a 10x speedup by precomputing substitutions of all strings
up to length 10

how do I precompute substitutions?
one idea is recursion with memoization, but if a string goes N steps deep,
python will raise.  I've got to do it iteratively

start with 3.  For each substitution of size two, and for each digit, append
the digit to the result of the substitution and the "reduce"

then scan the string and start substituting in groups of 10


What happened is that there are edges that may have to be substituted first.

I proposed to solve this issue by setting one ahead and one behind and then 
voting.

The other issue was how to precompute  the substitutions.  I think this can be
done by iterating over each size up to the max size you desire.  For each
size you can use the substitutions from 2 sizes down (so you get a quorum for
voting.  But I have no idea).
"""

subs_cache = dict(substitutions)
for i in range(10):
    subs_cache[str(i)] = str(i)

def precompute_substitutions(max_size, cur_size):
    votes = [Counter() for _ in range(len(N))]

    for i in range(max_size):

        sub = N[i:i+cur_size]
        for j in range(CACHE_TO_LENGTH):
            votes[i+j][N[i+j]] += 1

    result = [v.most_common(1)[0] for v in votes]



precompute_substitutions(9, 2)

def precompute_substitutions_garbage(max_size=CACHE_TO_LENGTH):
    result = dict(substitutions)
    for i in range(10):
        result[str(i)] = str(i)

    for j in range(3, max_size+1):
        for prev in range(10**j):
            for i in range(10):
                cur = str(prev).zfill(j) + str(i)
                result[str(i)] = solution1(cur)

    return result



"""
one way to do this is to make a counter for every index in the string

then use the highest voted
"""
def do_subs_big(N, length):
    if len(N) <= CACHE_TO_LENGTH:
        return subs_cache[N]

    votes = [Counter() for _ in range(len(N))]

    for i in range(len(N)-CACHE_TO_LENGTH):
        sub = N[i:i+CACHE_TO_LENGTH]
        for j in range(CACHE_TO_LENGTH):
            votes[i+j][N[i+j]] += 1

    result = [v.most_common(1)[0] for v in votes]


def solution(N):
    prev = list(N)
    cur = do_subs_big(prev)

    while prev != cur:
        prev = cur
        cur = do_subs_big(prev)

    return "".join(cur)



def main():
    for i, test_case in enumerate(parse_input()):
        print("Case #{}: {}".format(i+1, solution(*test_case)))

if __name__ == '__main__':
    main()
