def add_help(res, a, b, i, carry):
	# INV: If s = sum of numbers represented by the first i digits of a and b, 
	# res = s div 10^i and carry = s div 10^i
	if i == len(a):
		if carry != 0:
			res.append(carry)
		return res
	else:
		res.append( (a[i] + b[i] + carry) % 10 )
		return add_help(res, a, b, i + 1, (a[i] + b[i] + carry) // 10)
def add(a, b):
	if len(a) < len(b):
		a.extend([0] * ( len(b) - len(a) ) )
	elif len(a) > len(b):
		b.extend([0] * (len(a) - len(b)) )
	#assert: len(a) = len(b)
	return add_help([], a, b, 0, 0)
