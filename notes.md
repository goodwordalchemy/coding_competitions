# NOTES

## Solving Questions I Missed

### 2020C
- [ ] Perfect Subarray (part 2)
- [x] Candies (part 2)

* "Candies I" was just a take on summing across a matrix and prefix sums.
* "Candies II" was just awful to debug.  I kept getting TLE even for the first test set.  Then, Ii realized that prefix sum queries are constant time, so they are much faster when you have a small amount of updates.  I knew my prefix sum worked on the first test set, so I tried using prefix sum when the number of queries is small and segment tree for when it is larger, and it passed.

### 2020B
- [x] Bus Routes
- [x] Wandering Robot

### 2020A
- [x] Workout (2nd set)
- [x] Bundling

* second set of workout required deep intuition about the problem itself.  Was not hard to program at all.  The intution was that you could binary search for the global answer, and use each guess to check that amount of sessions that would have to be inserted.
* key thing with bundling was realizing that each prefix could contribute
Pi // K to the total.  Basically greedy algorithm where you group and count
as many as possible.

### 2019H
- [x] H-index
- [x] Diagonal Puzzle (3 hours with analysis in front of me)
- [x] Elevanagram

* h_index was greedy with a priority queue, and very hard for me.  How do you prove 
greedy algorithms sufficiently?  I might have come up with that algorithm, but 
questioned it.
* diagonal.  gotta be good at matrix diagonals.

### 2019G
- [x] Book Reading (part 2)
- [ ] The equation (part 2)
- [ ] shifts (part 2)

* Book Reading Part II - the key insight is that you can cache queries from the same reader.  This is a common paradigm in these kinds of problems, in my opinion.  I guess it's just simple memoization, but it's hard to see because it's outside of a dynamic programming context.
