package main

import (
    "bufio"
    "fmt"
    "os"
	"sort"
)

func Max(x, y int) int {
    if x < y {
        return y
    }
    return x
}

func Min(x, y int) int {
    if x > y {
        return y
    }
    return x
}

type SegmentTree struct {
    nodes []int
    size int
    oSize int
}

func calcTreeSize(originalSize int) int {
    return 4 * originalSize
}

func NewSegmentTree(s int) *SegmentTree{
    size := calcTreeSize(s)
    nodes := make([]int, size)

    t := &SegmentTree{nodes, size, s}
    return t
}

func (t *SegmentTree) buildUtil(a []int, v, tl, tr int) {
    if (tl == tr) {
        t.nodes[v] = a[tl]
    } else {
        tm := (tl + tr) / 2
        t.buildUtil(a, v*2, tl, tm)
        t.buildUtil(a, v*2+1, tm+1, tr)
        t.nodes[v] = t.nodes[v*2] + t.nodes[v*2+1]
    }
}

func (t *SegmentTree) build(a []int) {
    t.buildUtil(a, 1, 0, t.oSize-1)
}

func NewSegmentTreeFromSlice(from []int) *SegmentTree{
    t := NewSegmentTree(len(from))
    t.build(from)
    return t
}

func (t *SegmentTree) queryUtil(v, tl, tr, l, r int) int {
    if l > r {
        return 0
    }
    if l == tl && r == tr {
        return t.nodes[v]
    }
    tm := (tl + tr) / 2
    result := t.queryUtil(v*2, tl, tm, l, Min(r, tm))
    result += t.queryUtil(v*2+1, tm+1, tr, Max(l, tm+1), r)

    return result
}

func (t *SegmentTree) query(left, right int) int {
    return t.queryUtil(1, 0, t.oSize-1, left, right)

}

func (t *SegmentTree) updateUtil(v, tl, tr, pos, newVal int) {
    if tl == tr {
        t.nodes[v] = newVal
    } else {
        tm := (tl + tr) / 2
        if pos <= tm {
            t.updateUtil(v*2, tl, tm, pos, newVal)
        } else {
            t.updateUtil(v*2+1, tm+1, tr, pos, newVal)
        }
        t.nodes[v] = t.nodes[v*2] + t.nodes[v*2+1]
    }
}

func (t *SegmentTree) update(idx, value int) {
    t.updateUtil(1, 0, t.oSize-1, idx, value)
}

func (t *SegmentTree) idxAtOrBelowUtil(v, tl, tr, k int) int {
    if tl == tr {
        return tl
    }
    if k >= t.nodes[v] {
        return t.oSize  // gets decremented in parent func
    }

    tm := (tl + tr) / 2
    if t.nodes[v*2] > k {
        return t.idxAtOrBelowUtil(v*2, tl, tm, k)
    } else {
        return t.idxAtOrBelowUtil(v*2+1, tm+1, tr, k - t.nodes[v*2])
    }

}

func (t *SegmentTree) idxAtOrBelow(k int) int {
    return t.idxAtOrBelowUtil(1, 0, t.oSize-1, k) - 1

}

func testSegmentTree() {
	for _, arr := range [][]int{[]int{1,2,3,4}, []int{1,2,3,4,5}, []int{1,2,3,4,5,6}} {
		tree := NewSegmentTreeFromSlice(arr)
		var s int
        fmt.Println("sums")
		s = tree.query(0, 2)
		fmt.Println(6, s)

		s = tree.query(0, 3)
		fmt.Println(10, s)

		s = tree.query(1, 2)
		fmt.Println(5, s)

		tree.update(1, 0)
		s = tree.query(1, 2)
		fmt.Println(3, s)

		tree.update(1, 2)
		fmt.Println(tree.nodes)

		s = tree.query(1, 2)
		fmt.Println(5, s)

        s = tree.query(0, len(arr)-1)
        s2 := 0
        for _, e := range arr {
            s2 += e
        }
        fmt.Println(s2, s)

        fmt.Println("idxs")
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

        s = tree.idxAtOrBelow(s2+1)
        fmt.Println(len(arr)-1, s)

        s = tree.idxAtOrBelow(s2)
        fmt.Println(len(arr)-1, s)

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
			if idx == -1 || idx == len(attractions) {
				idx = len(attractions) - 1
			}
			result = Max(result, scores.query(0, idx))
		} else {
			enabled.update(idxToRank[i], 0)
			scores.update(idxToRank[i], 0)
		}
	}


    return result
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
        // if i == 67 {
        //     fmt.Printf("%v %v %v\n", D, N, K)
        //     s := 0
        //     for _, a := range attractions {
        //         fmt.Printf("%v\n", a)
        //         s += a.h
        //     }
        //     fmt.Printf("should be %v\n", s)
        // }
        result := solution(D, K, attractions)
        fmt.Printf("Case #%d: %d\n", i, result)
    }
}
