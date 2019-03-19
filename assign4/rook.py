def choose(n, m):
	a = [1]
	i = 0
		
	#INV: For all 0 <= r <= i, a[r] = (i)choose(r); 0 <= i <= n
	while i < n:
		new_a = [0] * (i + 2)
		j = 1
		new_a[0] = 1
		new_a[i + 1] = 1
		
		#INV: for k in [0..j-1] new_a[k] = (i + 1)choose(k); 1 <= j <= i + 1
		while(j <= i):
			new_a[j] = a[j] + a[j - 1]
			#(i + 1)Cj = iCj + iC(j - 1)
			j += 1

		#assert: for k in [0..i+1] new_a[k] = (i + 1)choose(k)   
		i += 1

		a = new_a

	#assert: For all 0 <= r <= n, a[r] = (n)choose(r)
	return a[m]

def rook(p, q):
	#To find: (p + q - 2) C (q - 1)
	return choose(p + q - 2, q - 1)
