"""
2 key insights.

1. use a set of "interesting locations" organized with substitution order.
This way it saves you a lot of iterating through the list.


2. use a linked list so you can add and remove in constant time.
"""
DEV = False

sample_text = """7
3
012
4
0145
5
00000
11
98765432101
2
01
1
1
2
10
"""

sample_text = """1
{}
523682305021737909598451707498860955107428866940862351771569298500297852990189896277685441775
""".format(len("523682305021737909598451707498860955107428866940862351771569298500297852990189896277685441775"))


if DEV:
    from collections import deque
    from unittest.mock import MagicMock

    sample_lines = deque(sample_text.split("\n"))

    input = MagicMock(side_effect=lambda: sample_lines.popleft())


substitutions = [
    ("01", "2"),
    ("12", "3"),
    ("23", "4"),
    ("34", "5"),
    ("45", "6"),
    ("56", "7"),
    ("67", "8"),
    ("78", "9"),
    ("89", "0"),
    ("90", "1"),
]

substitutions_mapping = dict(substitutions)
substitutables = list(zip(*substitutions))[0]

substitutable_idx = {s: i for i, s in enumerate(substitutables)}


def parse_input():
    n_test_cases = int(input())
    for t in range(n_test_cases):
        _ = input()
        N = input()
        yield (N,)


class ListNode:
    def __init__(self, val, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

    @property
    def val2(self):
        if self.right.val is None:
            return
        elif self.val is None:
            return 
        return self.val + self.right.val


class DLList:
    def __init__(self):
        leader = ListNode(None)
        leader.right = leader
        leader.left = leader

        self.leader = leader

    def insert_right(self, before, node):
        after = before.right

        node.left = before
        before.right = node

        after.left = node
        node.right = after

    def append(self, node):
        self.insert_right(self.leader.left, node)

    def remove(self, node):
        before = node.left
        after = node.right

        node.left = node.right = None
        before.right = after
        after.left = before

    @property
    def last(self):
        return self.leader.left

    def __iter__(self):
        cur = self.leader.right

        while cur != self.leader:
            yield cur
            cur = cur.right


def solution(N):
    # print(N)
    interesting = {}
    for pattern in substitutables:
        interesting[pattern] = set()

    dl_list = DLList()
    dl_list.append(ListNode(N[0]))

    for elt in N[1:]:
        dl_list.append(ListNode(elt))

        val2 = dl_list.last.left.val2
        if val2 in substitutables:
            interesting[val2].add(dl_list.last.left)

    while sum(len(v) for v in interesting.values()):
        # print(interesting)
        for pattern in substitutables:
            while interesting[pattern]:
                node = interesting[pattern].pop()
                # filter out nodes that have been subject to replaement
                if not node.right and not node.left:
                    continue
                assert node.right and node.left

                val2 = node.val2
                if val2 not in substitutions_mapping:
                    continue


                before = node.left
                after = node.right

                dl_list.remove(node)
                dl_list.remove(after)

                if val2 is None:
                    continue

                new_node = ListNode(substitutions_mapping[val2])
                dl_list.insert_right(before, new_node)

                if new_node.val2 in substitutions_mapping:
                    interesting[new_node.val2].add(new_node)
                if new_node.left.val2 in substitutions_mapping:
                    interesting[new_node.left.val2].add(new_node.left)


    result = "".join(elt.val for elt in dl_list)
    return result


def do_substitutions(N):
    cur = list(N)

    for to_sub, sub_to in substitutions:
        i = 0
        result = []
        while i < len(cur):
            if i == len(cur) - 1:
                result.append(cur[-1])
                break

            two = "".join(cur[i : i + 2])
            if two == to_sub:
                result.append(sub_to)
                i += 1
            else:
                result.append(cur[i])
            i += 1
        cur = result

    return cur


def solution2(N):
    prev = list(N)
    cur = do_substitutions(prev)

    while prev != cur:
        prev = cur
        cur = do_substitutions(prev)

    return "".join(cur)


def main():
    for i, test_case in enumerate(parse_input()):
        print("Case #{}: {}".format(i + 1, solution(*test_case)))


if __name__ == "__main__":
    main()
