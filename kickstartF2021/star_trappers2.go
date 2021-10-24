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

func iPow(a, b int) int {
  var result int = 1;

  for 0 != b {
    if 0 != (b & 1) {
      result *= a;

    }
    b >>= 1;
    a *= a;
  }

  return result;
}

func distance2(p1 []int, p2 []int) int {
    dx := p1[0] - p2[0]
    dy := p1[1] - p2[1]

    return iPow(dx, 2) + iPow(dy, 2)
}

func cosine(p1 []int, p2 []int) int {
    return p1[0]*p2[0] + p1[1]*p2[1]
}

func ccw(p1, p2, p3 []int) int {
    // signed area is positive for counter clockwise
    // by right hand rule
    result := (p2[0]-p1[0]) * (p3[1]-p1[1]) - (p3[0]-p1[0]) * (p2[1]-p1[1])
    return result
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

    referencePoint := points[p]
    sort.Slice(points, func(i, j int) bool {
        ci := ccw(referencePoint, points[i], points[j])
        cj := ccw(referencePoint, points[j], points[i])

        if ci == cj {
            di := distance2(points[i], referencePoint)
            dj := distance2(points[j], referencePoint)
            return di > dj
        }

        return ci > cj
    })


    /*
    this funny looking part handles the fact that the furthest most-ccw point will be considered before closer
    ones.  this means that the closer ones will get excluded from consideration.  If we didn't care about 
    colinear points, we could get rid of those
    */
    i := 0
    for i < len(points)-1 && ccw(referencePoint,  points[0], points[i]) == 0 {
        i++
    }
    var tmp []int
    l := 0
    h := i-1
    for l < h {
        tmp = points[l]
        points[l] = points[h]
        points[h] = tmp
        l++
        h--
    }

    stack := make([][]int, 0)

    for _, p := range points {
        for len(stack) > 1 && ccw(stack[len(stack)-2], stack[len(stack)-1], p) < 0 {
            stack = stack[:len(stack)-1]
        }
        stack = append(stack, p)
    }
    return stack
}

// func pointInConvexPolygon(point []int, polygon [][]int) bool {
//     x := float64(point[0])
//     y := float64(point[1])
//     n := len(polygon)
//     inside := false
//
//     var p2x, p2y float64
//     xints := 0.0
//     p1x := float64(polygon[0][0])
//     p1y := float64(polygon[0][1])
//
//     for i := 0; i <= n; i++ {
//         p2x = float64(polygon[i % n][0])
//         p2y = float64(polygon[i % n][1])
//         if y > math.Min(p1y, p2y) {
//             if y <= math.Max(p1y, p2y) {
//                 if x <= math.Max(p1x, p2x) {
//                     if p1y != p2y {
//                         xints = (y-p1y) * (p2x-p1x) / (p2y-p1y) + p1x
//                     }
//                     if p1x == p2x || x < xints {
//                         inside = !inside
//                     }
//                 }
//             }
//         }
//         p1x, p1y = p2x, p2y
//
//     }
//     return inside
// }

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

func pointOnPerimeter(point []int, polygon [][]int) bool {
    for i := range polygon {
        a := polygon[i]
        b := polygon[(i+1) % len(polygon)]
        if isOnSegment(point, a, b) {
            return true
        }
    }
    return false
}

func getPerimeter(polygon [][]int) float64 {
    result := 0.0
    for i := range polygon {
        a := polygon[i]
        b := polygon[(i+1) % len(polygon)]
        result += math.Sqrt(float64(distance2(a, b)))
    }

    return result
}

func solution(points [][]int) string {
    blueStar := points[len(points)-1]
    points = points[:len(points)-1]
    n := len(points)

    result := math.Inf(1)

    // for i := 0; i < n; i++ {
    //     for j := i+1; j < n; j++ {
    //         for k := j+1; k < n; k++ {
    //             vertices := [][]int{points[i], points[j], points[k]}
    //             hull := convexHull(vertices)
    //
    //             if !pointInConvexPolygon(blueStar, hull) {
    //                 continue
    //             } else if pointOnPerimeter(blueStar, hull) {
    //                 continue
    //             }
    //             perimeter := getPerimeter(hull)
    //             result = math.Min(perimeter, result)
    //
    //             for l := k+1; l < n; l++ {
    //                 vertices = append(vertices, points[l])
    //                 hull := convexHull(vertices)
    //
    //                 if !pointInConvexPolygon(blueStar, hull) {
    //                     continue
    //                 } else if pointOnPerimeter(blueStar, hull) {
    //                     continue
    //                 }
    //                 perimeter := getPerimeter(hull)
    //                 result = math.Min(perimeter, result)
    //
    //                 vertices = vertices[:len(vertices)-1]
    //             }
    //         }
    //     }
    // }
    //
    for k := 3; k < 5; k++ {
        combos := combinations(n, k)
        for _, combo := range combos {
            vertices := make([][]int, 0)
            for _, idx := range combo {
                vertices = append(vertices, points[idx])
            }
            hull := convexHull(vertices)

            if !pointInConvexPolygon(blueStar, hull) {
                continue
            } else if pointOnPerimeter(blueStar, hull) {
                continue
            }
            perimeter := getPerimeter(hull)
            result = math.Min(perimeter, result)
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
    for i := 1; i <= T; i++ {
        fmt.Fscan(in, &N)
        points := make([][]int, 0)
        for j := 0; j <= N; j++ {
            fmt.Fscan(in, &X, &Y)
            points = append(points, []int{X, Y})
        }

        result := solution(points)
        fmt.Printf("Case #%d: %s\n", i, result)
    }
}
