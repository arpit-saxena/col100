def partition(a, left, right):
	x = a[left]
	i = left + 1
	j = right
	#INV: a[left..i-1] <= x < a[j+1..right], left + 1 <= i, i <= j + 1, j <= right
	while(i <= j):
		if a[i] <= x:
			i += 1
		else:
			a[i], a[j] = a[j], a[i]
			j -= 1

	#assert: a[left..i-1] <= x < a[i..right], left + 1 <= i <= right
	a[left], a[i - 1] = a[i-1], a[left] #assert: a[i-1] = x
	p = i-1

	#assert: a[left..p-1] <= x < a[p+1..right], left <= p <= right
	return p

def qsort(a, left, right):
	if left < right:
		p = partition(a, left, right)
		qsort(a, left, p - 1)
		qsort(a, p + 1, right)

	#assert: a[left..right] is sorted up

def eligible(b, c):
    # assert: there are no int arrays of roll nums of people who attended (and passed)
    # courses B and C resp. and there are no duplicates in b and c
    qsort(b, 0, len(b) - 1)
    qsort(c, 0, len(c) - 1)

    # assert: b and c are sorted

    i, j = 0, 0
    a = []
    m, n = len(b), len(c)
    # INV: a = b[0..i-1] intersection c[0..j-1], 0 <= i <= m, 0 <= j <= n
    while i < m and j < n:
        if b[i] == c[j]:
            a.append(b[i])
            i += 1
            j += 1
        elif b[i] > c[j]:
            j += 1 # If c[j] < b[i], then there can be no match for c[j] in b[i..m-1]
        else:
            i += 1

    # assert: a = b[0..m-1] intersection c[0..n-1]
    return a

# Time complexity of eligible(b, c) = O(mlogm + nlogn), where m = len(b), n = len(c)
# qsort(arr) on average takes O(n logn) time, where n = len(arr)
# So, qsort(b, 0, len(b) - 1) and qsort(c, 0, len(c) - 1) take mlogm and nlogn time resp.
# 
# Moving further, we observe that in the while loop i + j decreases by atleast 1 in each
# iteration. So, in the worst case, it runs (m + n) times, i.e. it has time complexity 
# O(m + n)
#
# Adding all these, we get the total time complexity O(mlogm + nlogn)
# 
# NOTE: If we were to assume that sorted arrays are passed to the eligible function, then
# it's time complexity would be O(m + n) 