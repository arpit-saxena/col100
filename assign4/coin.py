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
