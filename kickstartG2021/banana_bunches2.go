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
	prefix := make([]int, N+1)
    prefix[0] = 0
	for i, elt := range B {
        if elt == K {
            return "1"
        }
		prefix[i+1] = prefix[i] + elt
	}

	inf := N + 10
	result := inf
    var curSum, diff int

	for i := 0; i < N; i++ {
        if prefix[N] - prefix[i] < K {
            break
        }
		for y := i+1; y < N; y++ {
			curSum = prefix[y+1] - prefix[i]
			if curSum == K {
				result = min(result, y - i + 1)
			}
            if curSum < K {
                continue
            }
			j := i+1
            for x := j; x < y; x++ {
				diff = prefix[x+1] - prefix[j]
				if curSum - diff == K {
					result = min(result, y - i + 1  - (x - j + 1))
				}
				for (j < x) && (curSum - diff <= K) {
					if B[x] == 0 && B[j] == 0 {
						break
					}
					j++
					diff = prefix[x+1] - prefix[j]
					if curSum - diff == K {
						result = min(result, y - i + 1  - (x - j + 1))
					}
				}
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
