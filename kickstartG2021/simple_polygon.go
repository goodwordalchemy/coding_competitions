package main

import (
    "bufio"
    "fmt"
	"os"
    "strings"
	// "io"
	// "strconv"
)

func min(i, j int) int {
	if i < j {
		return i
	} else {
		return j
	}
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

func solution(N int, A2 int) string {
    smallestA2 := (2 * N) / 2 - 2
    if A2 < smallestA2 {
        return "IMPOSSIBLE"
    }

    vertices := make([][]int, 0)

    if N == 3 {
        vertices = append(vertices, []int{0,0})
        vertices = append(vertices, []int{1,0})
        vertices = append(vertices, []int{0,A2})
    } else {
        //  bottom vertices
        x := 0
        var y int
        for x < N / 2 {
            if x % 2 == 1 {
                y = 0
            } else {
                y = 1
            }
            vertices = append(vertices, []int{x, y})
            x++
        }

        // outer vertex
        if N % 2 ==  1 {
            vertices = append(vertices, []int{x, 1})
        }


        // top vertices
        for x > 1 {
            x--
            if x % 2 == 1 {
                y = 1
            } else {
                y = 2
            }
            vertices = append(vertices, []int{x, y})
        }

        // fix top left
        smallestA2 := (2 * (N-1)) / 2 - 2
        outerY := A2 - smallestA2 + 1
        if outerY > 1000000000 {
            fmt.Println(N, A2)
            fmt.Printf("outer Y too big: %v\n", outerY)
            panic("peace")
        }
        vertices = append(vertices, []int{0, outerY})
    }


    resultArray := []string{"POSSIBLE"}

    for _, v := range vertices {
        resultArray = append(resultArray, fmt.Sprintf("%v %v", v[0], v[1]))
    }

    return strings.Join(resultArray, "\n")



}


func main() {
    in := bufio.NewReader(os.Stdin)

    var T int
    fmt.Fscan(in, &T)
    for i := 1; i <= T; i++ {
        var N, A int
        fmt.Fscan(in, &N, &A)

        result := solution(N, A)
        fmt.Printf("Case #%d: %s\n", i, result)
    }
}
