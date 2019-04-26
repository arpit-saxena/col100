def sum_digits(num):
    # assert: num is a positive integer

    i = 0
    sum = 0
    temp = num
    # INV: sum = a0 + a1 + .. + a(i-1), where num = sum_{j = 0}^{n-1}{aj * 10^j}, 0 <= i <= n,
    # temp = sum_{j = i}^{n-1}{aj * 10^j}
    while temp > 0: #temp > 0 => i < n
        sum += temp % 10
        temp //= 10
        i += 1

    # assert: sum = a0 + a1 + .. + a(n-1), where num = sum_{i = 0}^{n-1}{ai * 10^i}
    return sum

# TIME COMPLEXITY:
# IN each iteration of the while loop, temp is divided by 10.
# Therefore, after the ith iteration, temp = num // 10 ^ i
# Suppose that k be the smallest number such that num // 10^k = 0
# Then, firstly k = O(log n) and after k iteration, the loop terminates
# n // 10^(k-1) > 0 => 10^(k-1) < n => k < 1 + log(n) => k = O(logn)
# 
# Therefore, the time complexity of sum_digits(n) is O(log n) 