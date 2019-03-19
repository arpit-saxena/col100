def add(a, b):
	if len(a) > len(b):
		b.extend([0] * (len(a) - len(b)))
	elif len(b) > len(a):
		a.extend([0] * (len(b) - len(a)))
	#assert: len(a) = len(b)

	i = 0
	carry = 0
	res = [0] * len(a)
	#INV: VAL(res) + carry * 10^i = VAL(a[0..i-1]) + VAL(b[0..i-1]), 0 <= i <= len(a)
	while(i < len(a)):
		s = a[i] + b[i] + carry
		res[i] = s % 10
		carry = s // 10
		i += 1

	if carry != 0:
		res.append(carry)

	#assert: VAL(res) = VAL(a) + VAL(b)
	return res

def multdigit(a, d):
	i = 0
	carry = 0
	res = [0] * len(a)
	#INV: VAL(res) + carry * 10 ^ i = VAL(a[0..i-1]) * d, 0 <= i <= len(a)
	while i < len(a):
		s = a[i] * d + carry
		res[i] = s % 10
		carry = s // 10
		i += 1

	if carry != 0:
		res.append(carry)

	#assert: VAL(res) = VAL(a) * d
	return res

def addshift(res, c, k):
	if len(res) > len(c) + k:
		c.extend([0] * (len(res) - len(c) - k))
	elif len(c) + k > len(res):
		res.extend([0] * (len(c) + k - len(res)))
	#assert: len(c) + k = len(res)

	i = k
	carry = 0
	#INV: VAL(res) + carry * 10^i = VAL(res0[0..i-1]) + VAL(c[0..i-k-1]) * 10^k; k <= i <= len(res)
	while i < len(res):
		s = res[i] + c[i-k] + carry
		res[i] = s % 10
		carry = s // 10
		i += 1

	if carry != 0:
		res.append(carry)

	#assert: VAL(res) = VAL(res0) + VAL(c) * 10^k
	return res

def mult(a, b):
	i = 0
	res = []
	#INV: VAL(res) = VAL(a) * VAL(b[0..i-1]), 0 <= i <= len(b)
	while i < len(b):
		c = multdigit(a, b[i])
		#assert: VAL(c) = VAL(a) * b[i]
		addshift(res, c, i)
		#assert: VAL(res) = VAL(res0) + VAL(c) * 10 ^ i
		i += 1

	#assert: VAL(res) = VAL(a) * VAL(b)
	return res

def subtract(a, b):
	#assert: VAL(a) >= VAL(b)

	if len(b) < len(a):
		b.extend([0] * (len(a) - len(b)))
	#assert: len(a) = len(b)

	res = [0] * len(a)
	carry = 0
	i = 0
	#INV: VAL(res[0..i-1]) = carry * 10^i + VAL(a[0..i-1]) - VAL(b[0..i-1]), 0 <= i <= len(a)
	while i < len(a):
		s = a[i] - carry - b[i]
		if s < 0:
			s += 10
			carry = 1
		else:
			carry = 0
		res[i] = s
		i += 1

	#assert: VAL(res) = VAL(a) - VAL(b)
	return res

def stripzeroes(a):
	
	while len(a) > 0 and a[len(a) - 1] == 0:
		a.pop()

	#assert: len(a) = 0 or a[len(a) - 1] != 0 and VAL(a) = VAL(a0)

def comp(a, b):
	stripzeroes(a) #assert: a[len(a) - 1] != 0 and VAL(a) = VAL(a0)
	stripzeroes(b) #assert: b[len(b) - 1] != 0 and VAL(b) = VAL(b0)
	
	if len(a) > len(b):
		ret = 1
	elif len(a) < len(b):
		ret = -1
	else:
		#assert: len(a) == len(b)
		i = 0
		#INV: a[len(a)-i..len(a)-1] = b[len(b)-i..len(b)-1], 0 <= i <= len(a)
		while i < len(a) and a[len(a)-i-1] == b[len(b)-i-1]:
			i = i + 1

		if i < len(a):
			if a[len(a)-i-1] < b[len(a)-i-1]:
				ret = -1
			else:
				ret = 1
		else:
			ret = 0

	#assert: a < b => ret = -1
	#	a > b => ret = 1
	#	a == b => ret = 0
	return ret

def div_help(a, b):
	i = 0
	q = []
	r = []
	#INV: VAL(a[len(a)-i..len(a)-1]) = VAL(b) * VAL(q) + VAL(r), VAL(q) >= 0, 0 <= VAL(r) < VAL(b), 0 <= i <= len(a)
	while i < len(a):
		r.insert(0,a[len(a)-i-1])

		j = 0
		#INV: VAL(r0) = VAL(b) * VAL(j) + VAL(r)
		while comp(b, r) <= 0: #assert: comp(b, r) <= 0 <=> VAL(b) <= VAL(r)
			r = subtract(r,b)
			#assert: VAL(r) = VAL(r0) - VAL(b)
			j = j + 1

		#assert: VAL(r0) = VAL(b) * VAL(j) + VAL(r) and VAL(r) < VAL(b)

		q.insert(0,j)
		i = i + 1

	#assert: VAL(a) = VAL(b) * VAL(q) + VAL(r), VAL(q) >= 0, 0 <= VAL(r) < VAL(b)
	stripzeroes(q) #assert: q[len(q)-1] != 0 and VAL(q) = VAL(q0)
	stripzeroes(r) #assert: r[len(r)-1] != 0 and VAL(r) = VAL(r0)
	return q,r

def div(a, b):
	q, r = div_help(a,b)
	#assert: VAL(a) = VAL(b) * VAL(q) + VAL(r), VAL(q) >= 0, 0 <= VAL(r) < VAL(b)
	return q

def mod(a, b):
	q, r = div_help(a,b)
	#assert: VAL(a) = VAL(b) * VAL(q) + VAL(r), VAL(q) >= 0, 0 <= VAL(r) < VAL(b)
	return r
