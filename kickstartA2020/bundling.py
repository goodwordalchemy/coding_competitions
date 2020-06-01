from collections import deque
from string import ascii_uppercase

DEV = True

samples = [(
"""2 2
KICK
START""", 0
), (
"""8 2
G
G
GO
GO
GOO
GOO
GOOO
GOOO""", 10
), (
"""3 1
I
LOVE
CATS""", 9
), (
"""3 3
I
LOVE
CATS""", 0
), (
"""6 3
RAINBOW
FIREBALL
RANK
RANDOM
FIREWALL
FIREFIGHTER
""", 6
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
        N, K = map(int, input().split())
        strings = [input() for _ in range(N)]

        test_cases.append((K, strings))

    return test_cases

l2i = {l:i for i, l in enumerate(ascii_uppercase)}

class TrieNode:
    def __init__(self):
        self.count = 0
        self.children = [None for _ in range(26)]


class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):
        cur = self.root

        for l in word:
            i = l2i[l]
            if not cur.children[i]:
                cur.children[i] = TrieNode()
            cur = cur.children[i]
            cur.count += 1


def bfs(node, k):
    if not node:
        return 0

    result = 0
    queue = deque([node])
    while queue:
        for _ in range(len(queue)):
            cur = queue.popleft()
            result += cur.count // k
            for child in cur.children:
                if child:
                    queue.append(child)
    return result

def dfs(node, k):
    result = 0

    for child in node.children:
        if not child:
            continue
        result += dfs(child, k)
    result += node.count // k

    return result

def bundle(k, strings):
    trie = Trie()
    for s in strings:
        trie.insert(s)

    return bfs(trie.root, k)


def main():
    for i, test_case in enumerate(parse_input()):
        print("Case #{}: {}".format(i+1, bundle(*test_case)))

if __name__ == '__main__':
    main()
