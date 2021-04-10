from sys import exit, stderr, stdin, stdout
import heapq

def get_median(a, b, c):
    message = "{} {} {}".format(a.val, b.val, c.val)
    print(message, flush=True)
    stdout.flush()
    median = int(input())
    stderr.write(message + ", median: " + str(median) + "\n")
    if median == -1:
        exit(1)
    return median

def get_direction(a, b, target):
    if b is None or a is None:
        return 0

    median = get_median(a, b, target)
    if median == target.val:
        return 0
    elif median == b.val:
        return 1
    else:
        return -1

class Node:
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None

    def insert_between(self, a, b):
        if a is not None:
            a.right = self
        self.left = a

        if b is not None:
            b.left = self
        self.right = b
    

def insert(a, b, c):
    d = get_direction(a, b, c)

    if d == 0:
        while get_direction(a, a.right, c) != 0:
            a = a.right
        c.insert_between(a, a.right)
    elif d == 1:
        while get_direction(b, b.right, c) != 0:
            b = b.right
        c.insert_between(b, b.right)
    else:
        while get_direction(a.left, a, c) != 0:
            a = a.left
        c.insert_between(a.left, a)

def main():
    T, N, Q = map(int, input().split())

    for t in range(T):
        # stderr.write("t: " + str(t) + "\n")
        a = Node(1)
        b = Node(2)
        a.right = b
        b.left = a

        for i in range(3, N+1):
            insert(a, b, Node(i))

        right_of_a = []
        cur = a.right
        while cur:
            right_of_a.append(cur.val)
            cur = cur.right

        left_of_a = []
        cur = a.left
        while cur:
            left_of_a.append(cur.val)
            cur = cur.left

        result = " ".join(map(str, list(reversed(left_of_a)) + [a.val] + right_of_a))
        stderr.write("result: " + result + "\n")
        print(result, flush=True)
        stdout.flush()
        if int(input()) != 1:
            stderr.write("wrong answer maybe")
            exit(1)

if __name__ == '__main__':
    main()
