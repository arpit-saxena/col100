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

def merge_sort(a):
	#assert: a is an array

	arr = a
	if len(a) > 1:
		mid = len(a) // 2
		left = merge_sort(a[:mid]) #assert: left is sorted up
		right = merge_sort(a[mid:]) #assert: right is sorted up
		arr = merge(left, right) #assert: arr = left + right and sorted up
	#assert: arr is sorted up
	return arr
