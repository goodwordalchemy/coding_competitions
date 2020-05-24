DEV = True

sample_text = """6
0 0 2 0 0 1 0 0 0
0 0 0 0 0 0 0 0 12
0 0 0 0 2 0 1 1 0
3 1 1 1 0 0 0 0 0
3 0 0 0 0 0 3 0 2
0 0 0 0 0 0 0 1 0"""

samples = [
    ("0 0 2 0 0 1 0 0 0", "YES"),
    ("0 0 0 0 0 0 0 0 12", "YES"),
    ("0 0 0 0 2 0 1 1 0", "NO"),
    ("3 1 1 1 0 0 0 0 0", "YES"),
    ("3 0 0 0 0 0 3 0 2", "YES"),
    ("0 0 0 0 0 0 0 1 0", "NO"),
    ("0 0 0 0 0 0 0 0 0", "YES"),
    ("2 0 0 0 0 0 0 0 0", "YES"),
    ("3 0 0 0 0 0 0 0 0", "NO"),
    ("0 0 0 0 0 0 0 1 1", "NO"),
    ("0 1 0 0 0 0 0 0 0", "NO"),
    ("0 0 0 1 0 0 0 0 1", "NO"),
    ("2 1 0 0 0 0 0 0 0", "YES"),
    ("0 0 0 0 0 0 1 0 2", "YES"),
]
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
        tc = list(map(int, input().split()))
        test_cases.append(tc)

    return test_cases

def can_return_early(A):
    gte10 = gte6 = 0
    for elt in A:
        if elt >= 10:
            gte10 += 1
        if elt >= 6:
            gte6 += 1

    return gte10 >= 2 or gte6 >= 3


def can_elevenagram(A):
    if can_return_early(A):
        return "YES"

    mem = {}
    def dp(i, j, k):
        if (i, j, k) in mem:
            return mem[i,j,k]
        if j < 0:
            return False
        if i == 0 and j > A[0]:
            return False

        if i == 0:
            mem[i,j,k] = (k - (2*j - A[0])) % 11 == 0
            return mem[i,j,k]

        for p in range(A[i]+1):
            sum_ = k - (i+1) * (2*p-A[i])
            if dp(i-1, j-p, sum_ % 11):
                mem[i,j,k] =  True
                return mem[i,j,k]

        mem[i,j,k] = False
        return mem[i,j,k]

    result = dp(8, sum(A)//2, 0)

    return "YES" if result else "NO"

def main():
    for i, test_case in enumerate(parse_input()):
        print("Case #{}: {}".format(i+1, can_elevenagram(test_case)))

if __name__ == '__main__':
    main()
