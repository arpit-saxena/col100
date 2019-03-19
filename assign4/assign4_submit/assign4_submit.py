###########################################################################################################
# Q1

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
############################################################################################################

############################################################################################################
# Q2

#Finds number of ways to give a change for 'total' amount using denominations given in 'denom' list
def coin(total, denom):
	#assert: total >= 0 and denom is an array with positive integer values
	n = len(denom)

	ways = [0] * (total + 1)
	j = 0
	ways[0] = 1
	#INV: for i in [0..total] ways[i] is the number of ways to generate change i using j types of coins
	#	0 <= j <= n
	while j < n:
		k = 0
		#INV: for i in [0..k - 1], ways[i] is the number of ways to generate
		#change i using j + 1 types of coins; 0 <= k <= total + 1
		while k <= total:
			if k >= denom[j]:
				ways[k] = ways[k - denom[j]] + ways[k]
			k = k + 1		

		#assert: for i in [0..total], ways[i] is the number of ways to generate
		#change i using j + 1 types of coins
		j = j + 1

	#assert: for i in [0..total] ways[i] is the number of ways to generate change i
	return ways[total]

############################ end ##########################################################################
