import math
 
# A utility function that returns true if x is perfect square
def isPerfectSquare(x):
    s = int(math.sqrt(x))
    return s*s == x
 
# Returns true if n is a Fibinacci Number, else false
def isFibonacci(n):
 
    # n is Fibinacci if one of 5*n*n + 4 or 5*n*n - 4 or both
    # is a perferct square
    return isPerfectSquare(5*n*n + 4) or isPerfectSquare(5*n*n - 4)
    
# A utility function to test above functions
for i in range(1,11):
     if (isFibonacci(i) == True):
         print i,"is a Fibonacci Number"
     else:
         print i,"is a not Fibonacci Number "

print("okay real thing now...")

n = 487067745
print("is {} fib? {}".format(n, isFibonacci(n)))
