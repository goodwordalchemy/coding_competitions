DEV = True

samples = [(
"""2 3
1 2
3 3""", 3
), (
"""2 5
2 2
10 30""", 0
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
        N, H = map(int, input().split())
        A = list(map(int, input().split()))
        B = list(map(int, input().split()))
        yield (H, A, B)


def shifts(H, A, B):
    N = len(A)
    def dp(i, ha, hb):
        if i == N:
            return ha >= H and hb >= H
        return sum([
            dp(i+1, ha+A[i], hb),
            dp(i+1, ha, hb+B[i]),
            dp(i+1, ha+A[i], hb+B[i]),
        ])

    return dp(0, 0, 0)



def main():
    for i, test_case in enumerate(parse_input()):
        print("Case #{}: {}".format(i+1, shifts(*test_case)))

if __name__ == '__main__':
    main()
