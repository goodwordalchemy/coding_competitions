from itertools import combinations, permutations
"""

intuitively, you want to start with permutations of 
combinations that are sorted in descending order.

"""

# thank you leetcode
# def nextPermutation(nums):
#         """
#         Do not return anything, modify nums in-place instead.
#         """
#         n = len(nums)
#         i = n - 1
#         while i and nums[i-1] <= nums[i]:
#             i -= 1
        
#         j = n - 1
#         while j > i and i and nums[j] >= nums[i-1]:
#             j -= 1
        
#         nums[i-1], nums[j] = nums[j], nums[i-1]
        
#         j = n - 1
#         while i < j:
#             nums[i], nums[j] = nums[j], nums[i]
#             i += 1
#             j -= 1
        
def make(nums):
    return int("".join(nums))

def check(num):
    return num % 3 == 0
    
def solution(l):
    # Your code here
    l = list(map(str, l))
    for length in reversed(range(1, len(l)+1)):
        for perm in sorted(permutations(l, length), reverse=True):
            n = make(perm)
            if check(n):
                return n
    return 0
            

test_cases = [
    (solution([3, 1, 4, 1]), 4311),
    (solution([3, 1, 4, 1, 5, 9]), 94311),
    (solution([7, 7, 7 ,7]), 777),
    (solution([1]), 0)
]

for actual, expected in test_cases:
    print("{} == {}".format(actual, expected))
