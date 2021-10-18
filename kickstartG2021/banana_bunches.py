from collections import defaultdict

DEV = True

sample_text = """4
6 8
1 2 3 1 2 3
4 10
6 7 5 2
6 8
3 1 2 1 3 1
4 6
3 1 2 0
"""

# case where all dogs are fed, and not enough cat food.
# case where we run out of cat food and a dog is waiting
# case where run out of cat food and no dogs waiting


if DEV:
    from collections import deque
    from unittest.mock import MagicMock
    sample_lines = deque(sample_text.split("\n"))

    input = MagicMock(side_effect=lambda : sample_lines.popleft())



def parse_input():
    t_test_cases = int(input())
    test_cases = []
    for t in range(t_test_cases):
        N, K = list(map(int, input().split()))
        B = list(map(int, input().split()))
        yield (K, B)


def get_overlap(a, b):
    return max(0, min(a[1], b[1]) - max(a[0], b[0]))

def solution(K, B):
    segments_by_bunches = defaultdict(list)
    N = len(B)

    prefix = [0]
    for b in B:
        prefix.append(prefix[-1] + b)

    for i in range(N):
        for j in range(i+1, N+1):
            bunches = prefix[j] - prefix[i]
            segments_by_bunches[bunches].append((i, j))

    # already should be sorted by i
    for b in segments_by_bunches:
        segments_by_bunches[b].sort(lambda item: item[1]-item[0])

    result = float('inf')

    if K in segments_by_bunches:
        result = min(j-i for i,j in segments_by_bunches[K])

    for k in reversed(range(1, K)):
        if k not in segments_by_bunches:
            continue

        for b1 in segments_by_bunches[k]:
            if K-k not in segments_by_bunches:
                continue



            for b2 in segments_by_bunches[K-k]:
                # if b1[0] < b2[1] or b1[1] > b2[0]:
                #     continue
                if get_overlap(b1, b2) > 0:
                    continue
                # print(b1, b2, (b1[1]-b1[0]) + (b2[1]-b2[0]))
                result = min(result, (b1[1]-b1[0]) + (b2[1]-b2[0]))

    return result if result < float('inf') else -1





def main():
    for i, test_case in enumerate(parse_input()):
        print("Case #{}: {}".format(i+1, solution(*test_case)))

if __name__ == '__main__':
    main()
