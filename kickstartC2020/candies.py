DEV = True
sample_text = """2
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

MAX = 20000
samples = [(
"""5 4
1 3 9 8 2
Q 2 4
Q 5 5
U 2 10
Q 1 2""", -8
), (
"""3 3
4 5 5
U 1 2
U 1 7
Q 1 2""", -3
), (
"""1 3
1
Q 1 1
U 1 3
Q 1 1""", 4
), (
"""2 4
1 2
Q 1 1
U 1 3
U 2 3
Q 1 1""", 4
), (
"""10 3
1 2 3 4 5 6 7 8 9 10
Q 1 4
U 5 8
Q 4 9""", -46
), (
"""{} 8
{}
Q 1 500
U 488 4
Q 400 599
Q 1 1000
U 1 1000
U 1000 1
U 56 56
U 9999 18""".format(20000, " ".join(map(str, range(20000)))), -492183
), (
"""{} {}
{}
Q 1 500
U 488 4
Q 1 1000
U 1 1000
Q 400 599
U 1000 1
Q 400 20000
U 56 56
Q 1 1000
U 9999 18
Q 1 1000
{}""".format(
    MAX,
    MAX,
    " ".join(map(str, range(MAX))),
    "\n".join("Q {} {}".format(i%100+1, MAX) for i in range(MAX-11)))[:-1],
11096018
)
]

sample_inputs, sample_outputs = zip(*samples)

sample_text  = str(len(samples))+'\n'+"\n".join(sample_inputs)
if DEV:
    print("expected output:\n")
    print("\n".join("EXPECT Case {}: {}".format(i+1, o) for i, o in enumerate(sample_outputs)))
    print()


if DEV:
    from unittest.mock import MagicMock

    input = MagicMock(side_effect=sample_text.split("\n"))

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


class SegmentTree:
    def __init__(self, values):
        self.N = len(values)
        self.tree = [0]*self.N*4
        self.tree[self.N+1:2*self.N+1] = values
        for i in reversed(range(1, self.N+1)):
            self.tree[i] = self.tree[i<<1] + self.tree[i<<1|1]

    def update(self, idx, val):
        idx += self.N
        self.tree[idx] = val
        while idx > 1:
            self.tree[idx>>1] = self.tree[idx] + self.tree[idx^1]
            idx >>= 1

    def query(self, l, r):
        result = 0
        l += self.N
        r += self.N
        while l < r:
            if l&1:
                result += self.tree[l]
                l += 1
            if r&1:
               r -= 1
               result += self.tree[r]

            l >>= 1
            r >>= 1

        return result

def get_segment_trees(candies):
    s, m = [], []
    for i, c in enumerate(candies):
        parity = -1 if i&1 else 1
        s.append(parity*c)
        m.append(parity*(i+1)*c)

    s_tree = SegmentTree(s)
    m_tree = SegmentTree(m)

    return s_tree, m_tree

def query(s_tree, m_tree, start, end):
    result = m_tree.query(1, end+1)
    result -= m_tree.query(1, start)
    result -= (start-1)*(s_tree.query(1, end+1) - s_tree.query(1, start))

    parity = -1 if (start-1)&1 else 1
    result *= parity

    return result

def query_candies(candies, queries):
    n_updates = 0
    for type_, _, __ in queries:
        if type_ == 'U':
            n_updates += 1
    if n_updates == len(queries):
        return 0
    elif n_updates <= 6:
        return query_candies_prefix(candies, queries)

    s_tree, m_tree = get_segment_trees(candies)

    result = 0
    for type_, a, b in queries:
        if type_ == 'U':
            parity = -1 if (a-1)&1 else 1

            s_tree.update(a, parity*b)
            m_tree.update(a, a*parity*b)
        else:
            qr = query(s_tree, m_tree, a, b)
            result += qr

    return result


def query_candies_prefix(candies, queries):
    def query(prefix, m_prefix, start, end):
        result = m_prefix[end]
        result -= m_prefix[start-1]
        result -= (start-1)*(prefix[end] - prefix[start-1])

        parity = 1 if (start-1)&1 else -1
        result *= parity

        return result

    def get_prefix_arrays(candies):
        prefix = [0]
        m_prefix = [0]
        for i, c in enumerate(candies):
            parity = 1 if i&1 else -1
            prefix.append(prefix[-1] + parity*c)
            m_prefix.append(m_prefix[-1] + parity*(i+1)*c)

        return prefix, m_prefix
    prefix, m_prefix = get_prefix_arrays(candies)

    result = 0
    for type_, a, b in queries:
        if type_ == 'U':
            candies[a-1] = b
            prefix, m_prefix = get_prefix_arrays(candies)
        else:
            qr = query(prefix, m_prefix, a, b)
            result += qr

    return result

def main():
    cases = parse_input()
    for i, (candies, queries) in enumerate(cases):
        print("Case #{}: {}".format(i+1, query_candies(candies, queries)))

def debug():
    cases = parse_input()
    for i, (candies, queries) in enumerate(cases):
        print("Case #{}: {}".format(i+1, query_candies(candies, queries)))
        print("DEBUG: Case #{}: {}".format(i+1, query_candies_prefix(candies, queries)))
        print()


if __name__ == '__main__':
    main()
    # debug()

