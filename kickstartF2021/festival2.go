package main

import (
    "math"
    "bufio"
    "fmt"
    "os"
	"sort"
)


type SegmentTree struct {
    nodes []int
    size int
    oSize int
}


func calcTreeSize(originalSize int) int {
    return 1<<uint(math.Ceil(math.Log2(float64(originalSize)))+1)
}

func NewSegmentTree(s int) *SegmentTree{
    size := calcTreeSize(s)
    nodes := make([]int, size*2)

    t := &SegmentTree{nodes, size, s}
    return t
}

func NewSegmentTreeFromSlice(from []int) *SegmentTree{
    size := calcTreeSize(len(from))
    nodes := make([]int, size*4)

    t := &SegmentTree{nodes, size, len(from)}
    for i := 0; i < len(from); i += 1 {
        nodes[i+size] = from[i]
    }
    for i := size - 1; i > 0; i -= 1 {
        t.nodes[i] = t.nodes[i<<1] + t.nodes[i<<1|1];
    }
    return t
}

func (t *SegmentTree) query(left, right int) int {
    res := 0
    left += t.size
    right += t.size;
    for left < right  {
        if left&1 == 1 {
            res += t.nodes[left]
            left += 1
        }
        if right&1 == 1 {
            right -= 1
            res += t.nodes[right]
        }
        left >>= 1
        right >>= 1
    }
    return res
}

func (t *SegmentTree) update(idx, value int) {
    idx += t.size
    t.nodes[idx] = value
    for idx > 1 {
        t.nodes[idx>>1] = t.nodes[idx] + t.nodes[idx^1]
        idx -= 1
    }
}

func (t *SegmentTree) idxAtOrBelow(k int) int {
	v := 1
	tl := 0
	tr := t.size - 1

    var tm int
	for tl != tr {
		if k > t.nodes[v] {
            return t.oSize
        }
        tm = (tl + tr) / 2
        if t.nodes[v*2] > k {
            v *= 2
            tr = tm
        } else {
            k -= t.nodes[v*2]
            v = v * 2 + 1
            tl = tm + 1
        }
	}

    return tl - 1
}


	// def idx_at_or_below(self, k):
	// 	v = 1
	// 	tl = 0
	// 	tr = self.N-1
    //
	// 	while tl != tr:
	// 		if k > self.tree[v]:
	// 			return self.original_N 
	// 		tm = (tl + tr) // 2
	// 		if self.tree[v*2] > k:
	// 			v *= 2
	// 			tr = tm
	// 		else:
	// 			k -= self.tree[v*2]
	// 			v = v * 2 + 1
	// 			tl = tm + 1
    //
	// 	return tl - 1

func testSegmentTree() {
	for _, arr := range [][]int{[]int{1,2,3,4}, []int{1,2,3,4,5}, []int{1,2,3,4,5,6}} {
		tree := NewSegmentTreeFromSlice(arr)
		var s int
		s = tree.query(0, 3)
		fmt.Println(6, s)

		s = tree.query(1, 3)
		fmt.Println(5, s)

		tree.update(1, 0)
		s = tree.query(1, 3)
		fmt.Println(3, s)

		tree.update(1, 2)
		fmt.Println(tree.nodes)

		s = tree.query(1, 3)
		fmt.Println(5, s)

		s = tree.idxAtOrBelow(1)
		fmt.Println(0, s)

		s = tree.idxAtOrBelow(2)
		fmt.Println(0, s)

		s = tree.idxAtOrBelow(3)
		fmt.Println(1, s)

		s = tree.idxAtOrBelow(5)
		fmt.Println(1, s)

		s = tree.idxAtOrBelow(6)
		fmt.Println(2, s)

		s = tree.idxAtOrBelow(1000)
		fmt.Println(len(arr), s)

		s = tree.idxAtOrBelow(-1000)
		fmt.Println(-1, s)
	}
	fmt.Println("test done")
}

type Attraction struct {
    h int
    s int
    e int
}


func solution(D int, K int, attractions []Attraction) int {
    hs := make([][]int,  0)
    lineSweep := make([][]int, 0)
    for i, ride := range attractions {
        lineSweep = append(lineSweep, []int{ride.s, 1, ride.h, i})
        lineSweep = append(lineSweep, []int{ride.e+1, -1, ride.h, i})
        hs = append(hs, []int{ride.h, i})
    }
    sort.Slice(hs[:],func(i, j int) bool {
		for x := range hs[i] {
			if hs[i][x] == hs[j][x] {
				continue
			}
			return hs[i][x] > hs[j][x]
		}
		return false
	})
    sort.Slice(lineSweep[:],func(i, j int) bool {
		for x := range lineSweep[i] {
			if lineSweep[i][x] == lineSweep[j][x] {
				continue
			}
			return lineSweep[i][x] < lineSweep[j][x]
		}
		return false
	})

	idxToRank := make(map[int]int)
	for i, elt := range hs {
		idxToRank[elt[1]] = i
	}


	enabled := NewSegmentTree(len(attractions))
	scores := NewSegmentTree(len(attractions))

	result := 0
	for _, elt := range lineSweep {
		type_ := elt[1]
		h := elt[2]
		i := elt[3]
		if type_ == 1 {
			enabled.update(idxToRank[i], 1)
			scores.update(idxToRank[i], h)
			idx := enabled.idxAtOrBelow(K)
			if idx == -1 {
				idx = len(attractions)
			}
			idx += 1
			result = Max(result, scores.query(0, idx))
		} else {
			enabled.update(idxToRank[i], 0)
			scores.update(idxToRank[i], 0)
		}
	}


    return result
}

func Max(x, y int) int {
    if x < y {
        return y
    }
    return x
}

func main() {
	// testSegmentTree()
    in := bufio.NewReader(os.Stdin)

    var T int
    fmt.Fscan(in, &T)
    for i := 1; i <= T; i++ {
        var D, N, K int
        fmt.Fscan(in, &D, &N, &K)

        attractions := make([]Attraction, N)
        var h, s, e int
        for j := 0; j < N; j++ {
            fmt.Fscan(in, &h, &s, &e)
            attractions[j] = Attraction{h, s, e}
        }
        result := solution(D, K, attractions)
        fmt.Printf("Case #%d: %d\n", i, result)
    }
}
