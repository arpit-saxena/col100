# Consider a sequence S = {1,2,3,4,5,6,8,10,12,..} which includes
# 1 and all numbers divisible by no primes other than 2, 3
# or 5.
# Returns an array which has first n terms of the sequence S
def generate(n = 1000):
    #assert: n is a positive integer.
    arr = [0] * n
    i = 1
    arr[0] = 1
    #INV: arr[0..i-1] has first i terms of the sequence S, 0 <= i <= n
    while i < n:
        t = arr[i-1] * 2
        j = i - 2
        exhausted_all_possibilities = False
        multiply_by = 2
        # INV: t is of the form 2^a * 3^b * 5^c; a, b, c >= 0; t > arr[i-1]
        # t is the smallest multiple of all elements in arr[j..n-1] of that form
        # 0 <= j <= n; 
        # not exhausted_all_possibilities <=> There can multiples of
        # elements in arr[0..j-1] that satisfy conditions for t;
        # multiply_by = number in {2,3,5} by which multiplying the element of array
        # can possibly generate t
        while j >= 0 and not exhausted_all_possibilities:
            if arr[j] * multiply_by <= arr[i - 1]:
                if multiply_by == 5:
                    exhausted_all_possibilities = True
                elif multiply_by == 3:
                    multiply_by = 5
                else:
                    multiply_by = 3
            else:
                if arr[j] * multiply_by < t:
                    t = arr[j] * multiply_by
                j -= 1

        #assert: t is the (i + 1)th term of the sequence S.
        arr[i] = t
        i += 1

    #assert: arr has first n terms of the sequence S
    return arr

print(generate(10000))

###########################################################################################################
#
# Proof follows from the fact that the next term of the sequence after finding
# its first i terms (say) can be generated by multiplying each of the i terms by 2,3 and 5
# and then the smallest of those numbers which is greater than the ith term will be the 
# (i+1)th term.
# 
# This can be easily proven. Suppose the next term is 2^a * 3^b * 5^c. If i >= 1, then one
# of a, b, c has to be non-zero (If all were zero, then the next term would be 1, which is not possible)
# Without loss of generality, let a != 0. Then, we observe that 2^(a-1) * 3^b * 5^c is also
# part of the sequence, and since it's less than the (i + 1)th term, it must be one of the already
# found out terms. Thus we have shown that the (i + 1)th term is a multiple of one of the first
# i terms.
#
# Time complexity:
#       We start at the innermost while loop. Worst case time for it would be j counted down
#       to 0. Since the inner statements of the loop run in time bounded by a constant,
#       Time for inner while loop = c * i, where c is a constant (as j counts down from i-2 to 0)
#       
#       For the ith iteration of outer loop, it runs c2 + i times, where c2 is a constant
#       Therefore, since i runs from 0 to n, the time complexity of the loop is O(n^2)
#       
#       Since all other statements run in constant time, the time complexity of generate(n) is
#       O(n^2)
# 
############################################################################################################ 