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
    print(s_tree.tree)
    import ipdb; ipdb.set_trace()
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
    s_tree, m_tree = get_segment_trees(candies)

    result = 0
    for type_, a, b in queries:
        if type_ == 'U':
            s_tree.update(a, b)
            m_tree.update(a, b)
        else:
            qr = query(s_tree, m_tree, a, b+1)
            print(qr)
            result += qr

    return result

# def query(prefix, m_prefix, start, end):
#     result = m_prefix[end]
#     result -= m_prefix[start-1]
#     result -= (start-1)*(prefix[end] - prefix[start-1])

#     parity = 1 if (start-1)&1 else -1
#     result *= parity

#     return result

# def get_prefix_arrays(candies):
#     prefix = [0]
#     m_prefix = [0]
#     for i, c in enumerate(candies):
#         parity = 1 if i&1 else -1
#         prefix.append(prefix[-1] + parity*c)
#         m_prefix.append(m_prefix[-1] + parity*(i+1)*c)

#     return prefix, m_prefix

# def query_candies(candies, queries):
#     prefix, m_prefix = get_prefix_arrays(candies)

#     result = 0
#     for type_, a, b in queries:
#         if type_ == 'U':
#             candies[a-1] = b
#             prefix, m_prefix = get_prefix_arrays(candies)
#         else:
#             qr = query(prefix, m_prefix, a, b)
#             result += qr

#     return result

def main():
    cases = parse_input()
    for i, (candies, queries) in enumerate(cases):
        print("Case #{}: {}".format(i+1, query_candies(candies, queries)))



if __name__ == '__main__':
    main()

