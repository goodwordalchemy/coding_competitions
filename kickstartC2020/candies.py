DEBUG = True
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


def query_candies_slow(candies, queries):
    def update(candies, idx, val):
        candies[idx-1] = val


    def query(candies, start, end):
        result = 0
        for i, elt in enumerate(candies[start-1:end]):
            parity = -1 if (i&1) else 1
            result += (i+1)*parity*candies[start+i-1]

        return result

    result = 0
    for type_, a, b in queries:
        if type_ == 'U':
            update(candies, a, b)
        else:
            qr = query(candies, a, b)
            result += qr

    return result

def query(prefix, start, end):
    return prefix[end] - prefix[start-1]

def update(prefix, candies, idx, val):
    idx -= 1
    N = len(candies)

    candies[idx] = val
    for i in range(idx, N):
        parity = 1 if i&1 else -1
        prefix[i+1] = prefix[i] + parity*(i+1)*candies[i]

def query_candies(candies, queries):
    prefix = [0]
    for i, c in enumerate(candies):
        parity = 1 if i&1 else -1
        prefix.append(prefix[-1] + parity*(i+1)*c)

    result = 0
    for type_, a, b in queries:
        if type_ == 'U':
            update(prefix, candies, a, b)
        else:
            qr = query(prefix, a, b)
            print("query={} {} {}, result={}".format(type_, a, b, qr))
            result += qr

    return result

def main():
    cases = parse_input()
    for i, (candies, queries) in enumerate(cases):
        print("Case #{}: {}".format(i+1, query_candies(candies, queries)))



if __name__ == '__main__':
    main()

