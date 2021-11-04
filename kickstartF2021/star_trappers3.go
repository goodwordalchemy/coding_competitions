package main

import (
    "bufio"
    "fmt"
	"os"
    "sort"
    // "strings"
	// "io"
    "math"
	// "strconv"
)

// func min(i, j int) int {
// 	if i < j {
// 		return i
// 	} else {
// 		return j
// 	}
// }
//
// func max(i, j int) int {
// 	if i > j {
// 		return i
// 	} else {
// 		return j
// 	}
// }

type CombosCacheType map[int][][]int

func combinations(n int, k int) [][]int {
    result := make([][]int, 0)

    var backtrack func(int, []int)
    backtrack = func(i int, cur []int){
        if len(cur) == k {
            toAppend := make([]int, k)
            copy(toAppend, cur)
            result = append(result, toAppend)
            return
        }
        for j := i; j < n; j++ {
            cur = append(cur, j)
            backtrack(j+1, cur)
            cur = cur[:len(cur)-1]
        }
    }

    backtrack(0, make([]int, 0))

    return result
}


// func iPow(a, b int) int {
//   var result int = 1;
//
//   for 0 != b {
//     if 0 != (b & 1) {
//       result *= a;
//
//     }
//     b >>= 1;
//     a *= a;
//   }
//
//   return result;
// }

func GCDEuclidean(a, b int) int {
    var t int
	for b != 0 {
        t = b
        b = a % b
        a = t
	}
    return a
}

type Fraction struct {
    Numerator, Denominator int
}

func (f Fraction) String() string {
	return fmt.Sprintf("%d/%d", f.Numerator, f.Denominator)
}

func (f Fraction) Compliment() Fraction {
    return Fraction{-f.Numerator, -f.Denominator}.Reduce()
}

func iAbs(a int) int {
    if a < 0 {
        return -a
    }
    return a
}

// Reduce makes given fraction reduced.
func (f Fraction) Reduce() Fraction {
    gcd := GCDEuclidean(iAbs(f.Numerator), iAbs(f.Denominator))
	f.Numerator /= gcd
	f.Denominator /= gcd

	return f
}

// MultiplyByNumber multiplies fraction by given number.
func (f Fraction) MultiplyByNumber(m int) Fraction {
	f.Numerator *= m

	return f
}

// MultiplyByFraction multiplies fraction by given fraction.
func (f Fraction) MultiplyByFraction(m Fraction) Fraction {
	f.Numerator *= m.Numerator
	f.Denominator *= m.Denominator

	return f
}

func getSlope(a, b []int) Fraction {
    fraction := Fraction{
        Numerator:b[1]-a[1],
        Denominator:b[0]-a[0],
    }
    fraction = fraction.Reduce()
    return fraction
}

func distance2(p1 []int, p2 []int) int {
    dx := p1[0] - p2[0]
    dy := p1[1] - p2[1]

    return (dx*dx) + (dy*dy)
}


func ccw(p1, p2, p3 []int) int {
    // signed area is positive for counter clockwise
    // by right hand rule
    result := (p2[0]-p1[0]) * (p3[1]-p1[1]) - (p3[0]-p1[0]) * (p2[1]-p1[1])
    return result
}

type ByReferencePoint struct {
    ReferencePoint []int
    Points [][]int
}

func (b ByReferencePoint) Len()  int { return len(b.Points) }
func (b ByReferencePoint) Swap(i, j int) {
    b.Points[i], b.Points[j] = b.Points[j], b.Points[i]
}
func (b ByReferencePoint) Less(i, j int) bool {
    ci := ccw(b.ReferencePoint, b.Points[i], b.Points[j])
    cj := ccw(b.ReferencePoint, b.Points[j], b.Points[i])

    if ci == cj {
        di := distance2(b.Points[i], b.ReferencePoint)
        dj := distance2(b.Points[j], b.ReferencePoint)
        return di > dj
    }

    return ci > cj
}

func convexHull(points [][]int) [][]int {
    p := 0

    for i := range points {
        if points[i][1] < points[p][1] {
            p = i
        } else if points[i][1] == points[p][1] && points[i][0] < points[p][0] {
            p = i
        }
    }

    toSort := ByReferencePoint{ReferencePoint: points[p], Points:points}
    sort.Sort(toSort)



    /*
    this funny looking part handles the fact that the furthest most-ccw point will be considered before closer
    ones.  this means that the closer ones will get excluded from consideration.  If we didn't care about 
    colinear points, we could get rid of those
    */
    // i := 0
    // for i < len(points)-1 && ccw(referencePoint,  points[0], points[i]) == 0 {
    //     i++
    // }
    // var tmp []int
    // l := 0
    // h := i-1
    // for l < h {
    //     tmp = points[l]
    //     points[l] = points[h]
    //     points[h] = tmp
    //     l++
    //     h--
    // }

    stack := make([][]int, 0)

    for _, p := range points {
        for len(stack) > 1 && ccw(stack[len(stack)-2], stack[len(stack)-1], p) < 0 {
            stack = stack[:len(stack)-1]
        }
        stack = append(stack, p)
    }
    return stack
}


func rayIntersectsSegment(p, a, b []int) bool {
    if a[1] > b[1] {
        return rayIntersectsSegment(p, b, a)
    }
    var px, py, ax, ay, bx, by float64

    px = float64(p[0])
    ax = float64(a[0])
    bx = float64(b[0])
    py = float64(p[1])
    ay = float64(a[1])
    by = float64(b[1])


   if py == ay || py == by {
       py = math.Nextafter(py, math.Inf(1))
   }

   if py < ay || py > by {
       return false
   } else if px >= math.Max(ax, bx) {
       return false
   } else if px < math.Min(ax, bx) {
       return true
   }

   var slopeAB, slopeAP float64

   slopeAB = math.Inf(1)
   slopeAP = math.Inf(1)

   if ax != bx {
       slopeAB = (by - ay) / (bx - ax)
   }

   if ax != px {
       slopeAP = (py - ay) / (px - ax)
   }
   return slopeAP >= slopeAB
}

func pointInConvexPolygon(point []int, polygon [][]int) bool {
    // based on https://rosettacode.org/wiki/Ray-casting_algorithm
    count := 0
    for i := range polygon {
        a := polygon[i]
        b := polygon[(i+1) % len(polygon)]
        if rayIntersectsSegment(point, a, b) {
            count++
        }
    }

    return count % 2 == 1
}

func within(p, q, r int) bool {
    a := p <= q
    a = a && (q <= r)

    b := r <= q
    b = b && (q <= p)

    return a || b
}

func isOnSegment(point, a, b []int) bool {
    result := ccw(point, a, b) == 0
    if a[0] != b[0] {
        return result && within(a[0], point[0], b[0])
    } else {
        return result && within(a[1], point[1], b[1])
    }
}

// func pointOnPerimeter(point []int, polygon [][]int) bool {
//     for i := range polygon {
//         a := polygon[i]
//         b := polygon[(i+1) % len(polygon)]
//         if isOnSegment(point, a, b) {
//             return true
//         }
//     }
//     return false
// }
//
// func getPerimeter(polygon [][]int) float64 {
//     result := 0.0
//     for i := range polygon {
//         a := polygon[i]
//         b := polygon[(i+1) % len(polygon)]
//         result += math.Sqrt(float64(distance2(a, b)))
//     }
//
//     return result
// }

func pairEqual(a, b []int) bool {
    return a[0] == b[0] && a[1] == b[1]
}

func solution(points [][]int, combosCache CombosCacheType) string {
    // fmt.Println(len(points))
    blueStar := points[len(points)-1]
    points = points[:len(points)-1]
    n := len(points)

    result := math.Inf(1)
    var hull, vertices [][]int

    slopeGroups := make(map[Fraction][]int)
    var slopeKey Fraction
    // parallelograms:
    // group points by polar angle with blueStar
    for i := 0; i < n; i++ {
        slopeKey = getSlope(blueStar, points[i])
        if _, ok := slopeGroups[slopeKey]; !ok {
            slopeGroups[slopeKey] = points[i]
        }
        if distance2(points[i], blueStar) < distance2(slopeGroups[slopeKey], blueStar) {
            slopeGroups[slopeKey] = points[i]
        }
    }

    for slopeKey, group := range slopeGroups {
        complimentKey := slopeKey.Compliment()
        compliment, ok := slopeGroups[complimentKey]
        if !ok {
            continue
        }

        for key1, point1 := range slopeGroups {
            if key1 == complimentKey || key1 == slopeKey {
                continue
            }
            for key2, point2 := range slopeGroups {
                if key2 == complimentKey || key2 == slopeKey || key1 == key2 {
                    continue
                }

                vertices = [][]int{
                    group, compliment,
                    point1, point2,
                }
                hull = convexHull(vertices)
                perimeter := 0.0
                onPerimeter := false
                for i := range hull {
                    a := hull[i]
                    b := hull[(i+1) % len(hull)]
                    perimeter += math.Sqrt(float64(distance2(a, b)))
                    if perimeter > result {
                        break
                    }
                    if isOnSegment(blueStar, a, b) {
                        onPerimeter = true
                        break
                    }
                }

                if onPerimeter {
                    continue
                }

                if !pointInConvexPolygon(blueStar, hull) {
                    continue
                }

                result = math.Min(perimeter, result)
            }
        }
    }

    for i := 0; i < len(points); i++{
        for j := i+1; j < len(points); j++ {
            for k := j+1; k < len(points); k++ {
                vertices = [][]int{points[i], points[j], points[k]}
                hull = convexHull(vertices)
                perimeter := 0.0
                onPerimeter := false
                for i := range hull {
                    a := hull[i]
                    b := hull[(i+1) % len(hull)]
                    perimeter += math.Sqrt(float64(distance2(a, b)))
                    if perimeter > result {
                        break
                    }
                    if isOnSegment(blueStar, a, b) {
                        onPerimeter = true
                        break
                    }
                }
                if onPerimeter {
                    continue
                }

                if !pointInConvexPolygon(blueStar, hull) {
                    continue
                }

                result = math.Min(perimeter, result)
            }

        }

    }
    if result ==  math.Inf(1) {
        return "IMPOSSIBLE"
    }
    return fmt.Sprintf("%0.9f", result)
}

// func FScanIntArray(in io.Reader, n int) ([]int, error) {
//   result := make([]int, n)
//   for i := range result {
//     _, err := fmt.Fscan(in, &result[i])
//     if err != nil {
//        return nil, err
//     }
//   }
//   return result, nil
// }

func main() {
    in := bufio.NewReader(os.Stdin)

    var T, N, X, Y int
    fmt.Fscan(in, &T)
    combosCache := make(CombosCacheType)

    for i := 1; i <= T; i++ {
        fmt.Fscan(in, &N)
        points := make([][]int, 0)
        for j := 0; j <= N; j++ {
            fmt.Fscan(in, &X, &Y)
            points = append(points, []int{X, Y})
        }

        result := solution(points, combosCache)
        fmt.Printf("Case #%d: %s\n", i, result)
    }
}
