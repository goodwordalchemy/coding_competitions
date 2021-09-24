import os
from itertools import combinations
from functools import reduce
from scipy.spatial import ConvexHull

DEV = True

def make_sample_text_from_lines():
	sample_text = """1
123 456
789 1011
""","""3
0 0
0 1000000
1000000 0
187055 151277
""","""4
0 0
0 1000000
1000000 0
1000000 1000000
500000 500000
""","""4
500000 0
0 500000
500000 1000000
1000000 500000
500000 500000
"""
	sample_text = "{}\n".format(len(sample_text)) + "".join(sample_text)

	return sample_text

def make_sample_text_from_file(
		dirname="star_trappers_test_data/test_set_1",
		filename="ts2_input.txt"
	):
	with open(os.path.join(dirname, filename)) as handle:
		return handle.read()


FILE, LINES = (0, 1)
def make_sample_text(method=FILE):
	if method == FILE:
		return make_sample_text_from_file()
	elif method == LINES:
		return make_sample_text_from_lines()
	else:
		assert False



if DEV:
	from collections import deque
	from unittest.mock import MagicMock

	sample_text = make_sample_text()
	print( sample_text)
	sample_lines = deque(sample_text.split("\n"))

	input = MagicMock(side_effect=lambda : sample_lines.popleft())


def _debug(*args, enabled=False):
	if DEV and enabled:
		print(*args)



def parse_input():
	t_test_cases = int(input())
	for t in range(t_test_cases):
		N = int(input())
		white_stars = []
		for _ in range(N):
			Xi, Yi = list(map(int, input().split()))
			white_stars.append((Xi, Yi))
		Xs, Ys = list(map(int, input().split()))
		yield (white_stars, (Xs, Ys))

MIN_X = 0
MAX_X = 10**6
IMPOSSIBLE = "IMPOSSIBLE"

"""
for first solution, there are only 10 points.  

I can just try every combination of points, I think.

but then how to calculate the area?

also how to know if the point is bounded by the set of points?
"""

def ccw(A, B, C):
	Ay, Ax = A
	By, Bx = B
	Cy, Cx = C

	return (Cy - Cx) * (Bx - Ax) > (By - Ay) * (Cx - Ax)


def intersects(A1, A2, B1, B2):
	return ccw(A1, B1, B2) != ccw(A2, B1, B2) and ccw(A1, A2, B1) != ccw(A1, A2, B2)
	

def point_in_polygon2(point, poly):
	"""NOTE: polygon must be list of connected points"""
	n = 0
	# p1, p2 = (point[0], MIN_X), (point[0], MAX_X)
	p1, p2 = (point[0], point[1]), (MAX_X, point[1])
	for i in range(len(poly)):
		n += intersects(p1, p2, poly[i], poly[(i+1) % len(poly)])

	return n % 2 == 1

def point_in_polygon(point, poly):
	x, y = point
	n = len(poly)
	inside = False
	p2x = 0.0
	p2y = 0.0
	xints = 0.0
	p1x,p1y = poly[0]
	for i in range(n+1):
		p2x,p2y = poly[i % n]
		if y > min(p1y,p2y):
			if y <= max(p1y,p2y):
				if x <= max(p1x,p2x):
					if p1y != p2y:
						xints = (y-p1y)*(p2x-p1x)/(p2y-p1y)+p1x
					if p1x == p2x or x <= xints:
						inside = not inside
		p1x,p1y = p2x,p2y

	return inside


def distance(A, B):
	Ay, Ax = A
	By, Bx = B

	return ((By - Ay)**2 + (Bx - Ax)**2) ** 0.5
	
def get_perimeter(poly):
	perimeter = 0
	for i in range(len(poly)):
		perimeter += distance(poly[i], poly[(i+1) % len(poly)])

	return perimeter
	

	
def get_convex_hull_points(points):
	TURN_LEFT, TURN_RIGHT, TURN_NONE = (1, -1, 0)

	def cmp(a, b):
		return (a > b) - (a < b)

	def turn(p, q, r):
		return cmp((q[0] - p[0])*(r[1] - p[1]) - (r[0] - p[0])*(q[1] - p[1]), 0)

	def _keep_left(hull, r):
		while len(hull) > 1 and turn(hull[-2], hull[-1], r) != TURN_LEFT:
			hull.pop()
		if not len(hull) or hull[-1] != r:
			hull.append(r)
		return hull

	points = sorted(points)
	l = reduce(_keep_left, points, [])
	u = reduce(_keep_left, reversed(points), [])
	return l.extend(u[i] for i in range(1, len(u) - 1)) or l

def convex_hull_graham(points):
	'''
	Returns points on convex hull in CCW order according to Graham's scan algorithm. 
	By Tom Switzer <thomas.switzer@gmail.com>.
	'''
	TURN_LEFT, TURN_RIGHT, TURN_NONE = (1, -1, 0)

	def cmp(a, b):
		return (a > b) - (a < b)

	def turn(p, q, r):
		return cmp((q[0] - p[0])*(r[1] - p[1]) - (r[0] - p[0])*(q[1] - p[1]), 0)

	def _keep_left(hull, r):
		while len(hull) > 1 and turn(hull[-2], hull[-1], r) != TURN_LEFT:
			hull.pop()
		if not len(hull) or hull[-1] != r:
			hull.append(r)
		return hull

	points = sorted(points)
	l = reduce(_keep_left, points, [])
	u = reduce(_keep_left, reversed(points), [])
	return l.extend(u[i] for i in range(1, len(u) - 1)) or l

def collinear(a, b, c):
	"Return true iff a, b, and c all lie on the same line."
	ax, ay = a
	bx, by = b
	cx, cy = c
	return (bx - ax) * (cy - ay) == (cx - ax) * (by - ay)

def within(p, q, r):
	"Return true iff q is between p and r (inclusive)."
	return p <= q <= r or r <= q <= p

def is_on_line(a, b, c):
	"Return true iff point c intersects the line segment from a to b."
	# (or the degenerate case that all 3 points are coincident)
	ax, ay = a
	bx, by = b
	cx, cy = c
	return (collinear(a, b, c)
			and (within(ax, cx, bx) if ax != bx else 
				 within(ay, cy, by)))

def is_on_perimeter(point, poly):
	for i in range(len(poly)):
		if is_on_line(poly[i], poly[(i+1) % len(poly)], point):
			return True
	return False



def solution(white_stars, blue_star):
	if len(white_stars) < 3:
		return IMPOSSIBLE

	best_perimeter = float('inf')
	for size in range(3, 5):
		for subset in combinations(white_stars, size):
			
			hull = get_convex_hull_points(subset)
			if is_on_perimeter(blue_star, hull):
				continue
			
			_debug("hull:", hull)

			if point_in_polygon(blue_star, hull):
				cur_perimeter = get_perimeter(hull)
				_debug("perimeter: ", cur_perimeter)
				best_perimeter = min(best_perimeter, cur_perimeter)
			else:
				_debug("point not in polygon")
				cur_perimeter = get_perimeter(hull)
				_debug("perimeter: ", cur_perimeter)


	
	if best_perimeter == float('inf'):
		return IMPOSSIBLE
	return best_perimeter
	
def main():
	for i, test_case in enumerate(parse_input()):
		print("Case #{}: {}".format(i+1, solution(*test_case)))
		_debug()

if __name__ == '__main__':
	main()
