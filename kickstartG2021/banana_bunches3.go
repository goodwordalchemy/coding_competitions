package main

import (
    "bufio"
    "fmt"
	"os"
	"io"
	"strconv"
)

func min(i, j int) int {
	if i < j {
		return i
	} else {
		return j
	}
}

func solution(N int, K int, B []int) string {
    // fmt.Println(K, B)
    dp := make([]int, K+1)

	inf := N + 10
    for i := 0; i <= K; i++ {
        dp[i] = inf
    }
    dp[0] = 0

	result := inf
    var curSum int

    for jx := 0; jx < N; jx++ {
        // fmt.Println(jx, dp, result)
        curSum = 0
        for y := jx; y < N; y++ {
            curSum += B[y]
            if K - curSum >= 0 {
                result = min(result, y - jx + 1 + dp[K-curSum])
            }
        }

        curSum = 0
        for i := jx-1; i >= 0; i-- {
            curSum += B[i]
            if K - curSum >= 0 {
                dp[curSum] = min(dp[curSum], jx - i)
            }
        }

    }


	if result == inf {
		result = -1
	}

	return strconv.Itoa(result)
}

func FScanIntArray(in io.Reader, n int) ([]int, error) {
  result := make([]int, n)
  for i := range result {
    _, err := fmt.Fscan(in, &result[i])
    if err != nil {
       return nil, err
    }
  }
  return result, nil
}

func main() {
	// testSegmentTree()
    in := bufio.NewReader(os.Stdin)

    var T int
    fmt.Fscan(in, &T)
    for i := 1; i <= T; i++ {
        var N, K int
        fmt.Fscan(in, &N, &K)

		B, err := FScanIntArray(in, N)
		if err != nil {
			fmt.Printf("there was an error scanning: %v", err)
		}

        result := solution(N, K, B)
        fmt.Printf("Case #%d: %s\n", i, result)
    }
}
