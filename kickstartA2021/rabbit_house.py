"""
For this one, I'm thinking a priority queue is a good idea.

Start with the tallest block.  check each of it's neighbors.

Add as many blocks as necessary to get to size of current block - 1

Update those neighbors

Never visit cur block again.

Loop until heap is empty
"""

DEV = True

from heapq import heappush, heappop
import itertools

sample_text = """3
1 3
3 4 3
1 3
3 0 0
3 3
0 0 0
0 2 0
0 0 0"""


if DEV:
    from collections import deque
    from unittest.mock import MagicMock
    sample_lines = deque(sample_text.split("\n"))

    input = MagicMock(side_effect=lambda : sample_lines.popleft())


def parse_input():
    n_test_cases = int(input())
    test_cases = []
    for t in range(n_test_cases):
        r, _ = list(map(int, input().split()))
        grid = []
        for _ in range(r):
            grid.append(list(map(int, input().split())))

        test_cases.append(grid)

    return test_cases


class PriorityQueue:
    REMOVED = '<removed-task>'      # placeholder for a removed task

    def __init__(self):
        self.pq = []                         # list of entries arranged in a heap
        self.entry_finder = {}               # mapping of tasks to entries
        self.counter = itertools.count()     # unique sequence count

    def add_task(self, task, priority=0):
        'Add a new task or update the priority of an existing task'
        if task in self.entry_finder:
            self.remove_task(task)
        count = next(self.counter)
        entry = [priority, count, task]
        self.entry_finder[task] = entry
        heappush(self.pq, entry)

    def get_priority(self, task):
        entry = self.entry_finder.get(task)
        if entry is None:
            return None
        return entry[0]

    def remove_task(self, task):
        'Mark an existing task as REMOVED.  Raise KeyError if not found.'
        entry = self.entry_finder.pop(task)
        entry[-1] = self.REMOVED

    def pop_task(self):
        'Remove and return the lowest priority task. Raise KeyError if empty.'
        while self.pq:
            priority, count, task = heappop(self.pq)
            if task is not self.REMOVED:
                del self.entry_finder[task]
                return task, priority
        raise KeyError('pop from an empty priority queue')


def rabbit_house(grid):
    pq = PriorityQueue()


    for i in range(len(grid)):
        for j in range(len(grid[0])):
            pq.add_task((i, j), priority=-grid[i][j])

    result = 0

    while True:
        try:
            (i, j), neg_cur_height = pq.pop_task()
        except KeyError:
            break
        cur_height = -neg_cur_height
        

        for di, dj in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            ni = i+di
            nj = j+dj
            if not (0 <= ni < len(grid) and 0 <= nj < len(grid[0])):
                continue
            
            neg_neighbor_height = pq.get_priority((ni, nj))
            if neg_neighbor_height is None:
                continue
            neighbor_height = -neg_neighbor_height

            if cur_height - neighbor_height > 1:
                diff = cur_height - neighbor_height
                # print((i, j), (ni, nj), diff)

                result += diff - 1

                pq.remove_task((ni, nj))
                pq.add_task(
                    (ni, nj),
                    priority=-(neighbor_height + diff - 1)
                )

    return result


def main():
    for i, test_case in enumerate(parse_input()):
        print("Case #{}: {}".format(i+1, rabbit_house(test_case)))

if __name__ == '__main__':
    main()
