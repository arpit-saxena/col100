#Quick Sort

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

from random import randint
a = [randint(0, 1000000) for i in range(1000000)]
qsort(a, 0, len(a) - 1)
