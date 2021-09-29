from bisect import insort

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


class SegmentTree:
	def __init__(self, values, zero_val=0, comb=lambda a, b: a + b):
		"""
		values: List[T] an array of values to query
		comb: Function[[T, T], U]
		"""
		import math
		intended_length = 2**(math.ceil(math.log2(len(values)))+1)
		for _ in range(intended_length - len(values) - 1):
			values.append(zero_val)


		self.zero_val = zero_val
		self.N = len(values)
		self.tree = [self.zero_val]*self.N*4
		self.tree[self.N+1:2*self.N+1] = values
		self.comb = comb
		for i in reversed(range(1, self.N+1)):
			self.tree[i] = self.comb(self.tree[i<<1], self.tree[i<<1|1])

	def update(self, idx, val):
		idx += self.N
		self.tree[idx] = val
		while idx > 1:
			self.tree[idx>>1] = self.comb(self.tree[idx], self.tree[idx^1])
			idx >>= 1

	def query(self, l, r):
		result = self.zero_val 
		l += self.N
		r += self.N
		while l < r:
			if l&1:
				result = self.comb(result, self.tree[l])
				l += 1
			if r&1:
			   r -= 1
			   result = self.comb(result, self.tree[r])

			l >>= 1
			r >>= 1

		return result

	def idx_at_or_below(self, k):
		v = 1
		tl = 0
		tr = self.N

		while tl != tr:
			if k > self.tree[v]:
				return -1
			tm = (tl + tr) // 2
			if self.tree[v*2] > k:
				v *= 2
				tr = tm
			else:
				k -= self.tree[v*2]
				v = v * 2 + 1
				tl = tm + 1

		return tl
			

def test_segment_tree():
	arrays = [
		[1,2,3,4],
		[1,2,3,4,5],
		[1,2,3,4,5,6],
	]

	for a in arrays:
		tree = SegmentTree(a)
		idx = tree.idx_at_or_below(-1000)
		assert idx == 0, idx

		idx = tree.idx_at_or_below(1)
		assert idx == 1, idx

		idx = tree.idx_at_or_below(2)
		assert idx == 1, idx

		idx = tree.idx_at_or_below(3)
		assert idx == 2, idx

		idx = tree.idx_at_or_below(5)
		assert idx == 2, idx

		idx = tree.idx_at_or_below(6)
		assert idx == 3, idx

		idx = tree.idx_at_or_below(1000)
		assert idx == -1, idx

		s = tree.query(1, 3)
		assert s == 3

		s = tree.query(1, 4)
		assert s == 6

		s = tree.query(2, 4)
		assert s == 5

if DEV:
	test_segment_tree()

class BIT(object):	# 0-indexed.
	def __init__(self, n):
		self.__bit = [0]*(n+1)	# Extra one for dummy node.

	def add(self, i, val):
		i += 1	# Extra one for dummy node.
		while i < len(self.__bit):
			self.__bit[i] += val
			i += (i & -i)

	def query(self, i):
		i += 1	# Extra one for dummy node.
		ret = 0
		while i > 0:
			ret += self.__bit[i]
			i -= (i & -i)
		return ret

	def kth_element(self, k):
		floor_log2_n = (len(self.__bit)-1).bit_length()-1
		pow_i = 2**floor_log2_n
		total = pos = 0  # 1-indexed
		for _ in reversed(range(floor_log2_n+1)):	# O(logN)
			if pos+pow_i < len(self.__bit) and total+self.__bit[pos+pow_i] < k:  # find max pos s.t. total < k
				total += self.__bit[pos+pow_i]
				pos += pow_i
			pow_i >>= 1
		return (pos+1)-1  # 0-indexed, return min pos s.t. total >= k if pos exists else n

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

	enabled = BIT(len(rides))
	scores = BIT(len(rides))
	# enabled = SegmentTree([0]*len(rides))
	# scores = SegmentTree([0]*len(rides))

	result = 0
	for _, type_, h, i in line_sweep:
		if type_ == 1:
			enabled.add(idx_to_rank[i], 1)
			scores.add(idx_to_rank[i], h)
			idx = enabled.kth_element(K)
			idx = min(idx, len(rides) - 1)
		   
			result = max(result, scores.query(idx))
		else:
			enabled.add(idx_to_rank[i], -1)
			scores.add(idx_to_rank[i], -h)

	return result



def main():
	for i, test_case in enumerate(parse_input()):
		print("Case #{}: {}".format(i+1, solution(*test_case)))

if __name__ == '__main__':
	main()
