DEV = True

sample_text = """3
4 100
20 90 40 90
4 50
30 30 10 10
3 300
999 999 999"""


if DEV:
    from collections import deque
    from unittest.mock import MagicMock
    sample_lines = deque(sample_text.split("\n"))

    input = MagicMock(side_effect=lambda : sample_lines.popleft())



def parse_input():
    n_test_cases = int(input())
    test_cases = []
    for t in range(n_test_cases):
        _, money = map(int, input().split())
        tc = list(map(int, input().split()))
        test_cases.append((money, tc))

    return test_cases

def allocation(money, houses):
    houses.sort()
    result = 0

    for price in houses:
        if price <= money:
            result += 1
            money -= price

    return result


def main():
    for i, test_case in enumerate(parse_input()):
        print("Case #{}: {}".format(i+1, allocation(*test_case)))

if __name__ == '__main__':
    main()
