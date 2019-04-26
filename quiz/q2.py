# Given an array of ints [a0, a1, ..., an]
# Evaluate F(x) = a0 + a1*x + a2*x^2 + ... + an*x^n
# at a point x = m

def evaluate(a, m):
    #assert: a is an array of ints, m is an int
    n = len(a)
    i = 0
    val = 0

    #INV: val = a[n - i] + a[n - i + 1] * m^1 + .. + a[n-1] * m^i, 0 <= i <= n
    while i < n:
        val = val * m + a[n - i - 1]
        i = i + 1

    #assert: val = a[0] + a[1] * m + a[2] * m^2 + .. + a[n-1] * m^(n-1)
    return val

# Time complexity = O(n), where n = length of array of coefficients
# We see that the while loop runs n times and the other statements work in constant
# time, so time complexity is O(n)