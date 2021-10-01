import math

DEV = True

sample_text = """2
10 4 2
800 2 8
1500 6 9
200 4 7
400 3 5
5 3 3
400 1 3
500 5 5
300 2 3
"""


if DEV:
	from collections import deque
	from unittest.mock import MagicMock
	sample_lines = deque(sample_text.split("\n"))

	input = MagicMock(side_effect=lambda : sample_lines.popleft())



def parse_input():
	n_test_cases = int(input())
	for t in range(n_test_cases):
		D, N, K = list(map(int, input().split()))
		rides = []
		for _ in range(N):
			h, s, e = list(map(int, input().split()))
			rides.append((h, s, e))
		yield (D, K, rides)

class SegmentTree(object):
	def __init__(self, N,
				 query_fn=lambda x, y: x + y,
				 update_fn=lambda x, y: y,
				 default_val=0):

		self.original_N = N
		intended_length = 2**(math.ceil(math.log2(N))+1)
		self.N = intended_length
		self.H = (self.N-1).bit_length()
		self.query_fn = query_fn
		self.update_fn = update_fn
		self.default_val = default_val
		self.tree = [default_val] * (2 * self.N)
		self.lazy = [None] * self.N

	def __apply(self, x, val):
		self.tree[x] = self.update_fn(self.tree[x], val)
		if x < self.N:
			self.lazy[x] = self.update_fn(self.lazy[x], val)

	def bulk_update(self, I, hs):
		for i, h in enumerate(hs):
			self.update(I+i, I+i, h)

	def update(self, L, R, h):
		def pull(x):
			while x > 1:
				x //= 2
				self.tree[x] = self.query_fn(self.tree[x*2], self.tree[x*2 + 1])
				if self.lazy[x] is not None:
					self.tree[x] = self.update_fn(self.tree[x], self.lazy[x])
		L += self.N
		R += self.N
		L0, R0 = L, R
		while L <= R:
			if L & 1:
				self.__apply(L, h)
				L += 1
			if R & 1 == 0:
				self.__apply(R, h)
				R -= 1
			L //= 2
			R //= 2
		pull(L0)
		pull(R0)

	def query(self, L, R):
		def push(x):
			n = 2**self.H
			while n != 1:
				y = x // n
				if self.lazy[y] is not None:
					self.__apply(y*2, self.lazy[y])
					self.__apply(y*2 + 1, self.lazy[y])
					self.lazy[y] = None
				n //= 2

		result = self.default_val
		if L > R:
			return result

		L += self.N
		R += self.N
		push(L)
		push(R)
		while L <= R:
			if L & 1:
				result = self.query_fn(result, self.tree[L])
				L += 1
			if R & 1 == 0:
				result = self.query_fn(result, self.tree[R])
				R -= 1
			L //= 2
			R //= 2
		return result

	def idx_at_or_below(self, k):
		v = 1
		tl = 0
		tr = self.N-1

		while tl != tr:
			if k > self.tree[v]:
				return self.original_N 
			tm = (tl + tr) // 2
			if self.tree[v*2] > k:
				v *= 2
				tr = tm
			else:
				k -= self.tree[v*2]
				v = v * 2 + 1
				tl = tm + 1

		return tl - 1
	
	def data(self):
		showList = []
		for i in xrange(self.N):
			showList.append(self.query(i, i))
		return showList

def test_segment_tree():
	arrays = [
		[1,2,3,4],
		[1,2,3,4,5],
		[1,2,3,4,5,6],
	]

	for a in arrays:
		tree = SegmentTree(len(a))
		tree.bulk_update(0, a)
		idx = tree.idx_at_or_below(-1000)
		assert idx == -1, idx

		idx = tree.idx_at_or_below(1)
		assert idx == 0, idx

		idx = tree.idx_at_or_below(2)
		assert idx == 0, idx

		idx = tree.idx_at_or_below(3)
		assert idx == 1, idx

		idx = tree.idx_at_or_below(5)
		assert idx == 1, idx

		idx = tree.idx_at_or_below(6)
		assert idx == 2, idx

		idx = tree.idx_at_or_below(1000)
		assert idx == len(a), idx

		s = tree.query(2, 2)
		assert s == 3, s

		s = tree.query(0, 1)
		assert s == 3, s

		s = tree.query(1, 3)
		assert s == 9, s


if DEV:
	test_segment_tree()

def solution(D, K, rides):
	line_sweep = []
	hs = []
	for i, (h, s, e) in enumerate(rides):
		line_sweep.append((s, 1, h, i))
		line_sweep.append((e+1, -1, h, i))
		hs.append((h, i))

	hs.sort(reverse=True)
	line_sweep.sort()

	idx_to_rank = {i: rank for rank, (_, i) in enumerate(hs)}

	enabled = SegmentTree(len(rides))
	scores = SegmentTree(len(rides))

	result = 0
	for _, type_, h, i in line_sweep:
		if type_ == 1:
			enabled.update(idx_to_rank[i], idx_to_rank[i], 1)
			scores.update(idx_to_rank[i], idx_to_rank[i], h)
			idx = enabled.idx_at_or_below(K)
			if idx == -1:
				idx = len(rides) 
			
			result = max(result, scores.query(0, idx))
		else:
			enabled.update(idx_to_rank[i], idx_to_rank[i], 0)
			scores.update(idx_to_rank[i], idx_to_rank[i], 0)

	return result



def main():
	for i, test_case in enumerate(parse_input()):
		print("Case #{}: {}".format(i+1, solution(*test_case)))

if __name__ == '__main__':
	main()
