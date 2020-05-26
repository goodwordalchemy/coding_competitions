DEBUG = False
test_data = """2
5 4
1 3 9 8 2
Q 2 4
Q 5 5
U 2 10
Q 1 2
3 3
4 5 5
U 1 2
U 1 7
Q 1 2"""

if DEBUG:
    from unittest.mock import MagicMock

    input = MagicMock(side_effect=test_data.split("\n"))

def parse_input():
    cases = []
    n_cases = int(input())
    for _ in range(n_cases):
        n, q = list(map(int, input().split()))
        candies = list(map(int, input().split()))
        queries = []
        for _ in range(q):
            queries.append(list(input().split()))
            queries[-1][1] = int(queries[-1][1])
            queries[-1][2] = int(queries[-1][2])
        cases.append((candies, queries))

    return cases


def update(candies, idx, val):
    candies[idx-1] = val


def query(candies, start, end):
    result = 0
    for i, elt in enumerate(candies[start-1:end]):
        parity = -1 if (i&1) else 1
        result += (i+1)*parity*candies[start+i-1]
    
    return result


def query_candies(candies, queries):
    result = 0
    for type_, a, b in queries:
        if type_ == 'U':
            update(candies, a, b)
        else:
            qr = query(candies, a, b)
            result += qr
    

    return result

def main():
    cases = parse_input()
    for i, (candies, queries) in enumerate(cases):
        print("Case #{}: {}".format(i+1, query_candies(candies, queries)))



if __name__ == '__main__':
    main()

