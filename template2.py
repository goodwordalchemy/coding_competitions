DEV = True

samples = [(
"""5 2
10 13 15 16 17""", 2), (
"""5 6
9 10 20 26 30""", 3), (
"""8 3
1 2 3 4 5 6 7 10""", 1), (
"""3 1
100 200 230""", 50)
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
        N, K = map(int, input().split())
        M = list(map(int, input().split()))
        test_cases.append((K, M))

    return test_cases


def workout(k, sessions):
    pass


def main():
    for i, test_case in enumerate(parse_input()):
        print("Case #{}: {}".format(i+1, workout(*test_case)))

if __name__ == '__main__':
    main()
