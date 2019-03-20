def partition(a, left, right):
	elem = a[right]
	i = left
	j = right
	#INV: a[left..i-1] < elem <= a[j+1..right], left <= pos <= right
	while i <= j:
		if a[j] >= elem:
			j -= 1
		else:
			a[i], a[j] = a[j], a[i]
			i += 1

	a[j + 1], a[right] = a[right], a[j + 1]
	pos = j + 1

	#assert: a[left..pos-1] < a[pos] <= a[pos+1..right], 
	# left <= pos <= right
	return pos

def qsort(a, left, right):
	#assert: a is an array

	if left < right:
		pos = partition(a, left, right) 
			#assert: partitioned with right element as pivot.
			#pos indicates the position of pivot in partitioned array
			#   a[left..pos-1] < a[pos] <= a[pos+1..right], 
			# left <= pos <= right
		qsort(a, left, pos - 1)
		qsort(a, pos + 1, right)
	
	#assert: a[left..right] is sorted

def quicksort(a):
	qsort(a, 0, len(a) - 1)
	#assert: a[0..len(a)-1] is sorted
	return a

def merge(a, b):
	i = 0
	j = 0
	arr = []
	#INV: arr = a[0..i-1] + b[0..j-1] and sorted up, 0 <= i <= len(a), 0 <= j <= len(b)
	while i < len(a) and j < len(b):
		if a[i] <= b[j]:
			arr.append(a[i])
			i = i + 1
		else:
			arr.append(b[j])
			j = j + 1

	if i < len(a): #assert: j = len(b)
		while i < len(a):
			arr.append(a[i])
			i += 1
	elif j < len(b): #assert: i = len(a)
		while j < len(b):
			arr.append(b[j])
			j += 1

	#assert: arr = a + b and arr is sorted up
	return arr

def mergeSort(a):
	#assert: a is an array

	arr = a
	if len(a) > 1:
		mid = len(a) // 2
		left = mergeSort(a[:mid]) #assert: left is sorted up
		right = mergeSort(a[mid:]) #assert: right is sorted up
		arr = merge(left, right) #assert: arr = left + right and sorted up
	#assert: arr is sorted up
	return arr
