(*Assignment 3 COL100*)

(*recursive function for factorial*)
fun fact_recur(n) =
	if n = 0 then 1
	else n * fact_recur(n-1);

(*iterative factorial function*)
fun fact_iter(n) = 
	let
        (* curr_ans = i! *)
		fun fact_help(n, curr_ans, i) =
			if i = n then curr_ans
			else fact_help(n, curr_ans * (i + 1), i + 1);
	in
		fact_help(n, 1, 0)
	end;

(*recursive power function*)
fun pow_recur(x, n) =
	if n = 0 then 1
	else x * pow_recur(x, n - 1);

(* iterative power function*)
fun pow_iter(x, n) =
	let
        (* curr_ans = x^i *)
		fun pow_help(curr_ans, i) =
			if i = n then curr_ans
			else pow_help(curr_ans * x, i + 1);
	in
		pow_help(1, 0)
	end;

(* helper function to square argument*)
fun sqr(x) = x * x;

(*power function in O(log n) recursive*)
fun fpow_recur(x, n) =
	if n = 0 then 1
	else if n mod 2 = 0 then fpow_recur(x * x, n div 2)
	else x * fpow_recur(x * x, n div 2);

(*iterative power function in O(log n)*)
fun fpow_iter(x, n) =
	let
		(*Final answer = curr_ans * x^n *)
		fun fpow_help(curr_ans, x, n) = 
			if n = 0 then curr_ans
			else if n mod 2 = 0 then fpow_help(curr_ans, sqr(x), n div 2)
			else fpow_help(curr_ans * x, sqr(x), n div 2);
	in
		fpow_help(1, x, n)
	end;

(* Naive fibonacci function *)
fun fib(n) = 
	if n = 0 then 0
	else if n = 1 then 1
	else fib(n - 1) + fib(n - 2);

(* Iterative O(n) fibonacci function *)
fun fib_n(n) = 
	let
        (*b is equal to the ith fibonacci number*)
		fun fib_help(a, b, i) = 
			if i = n then b
			else fib_help(b, a + b, i + 1);
	in
		if n = 0 then 0
		else if n = 1 then 1
		else fib_help(0, 1, 1)
	end;

(* Iterative O(log n) fibonacci function
	Using the relation 
	fib(n) = fib(n div 2) * ( 2 * fib(n div 2 + 1) - fib(n div 2) ) if n is even
			 square(fib(n div 2)) + square(fib(n div 2 + 1))        otherwise 
*)
fun fib_logn(n) =
	let
        (* f1 is the (n / pow2)th fibonacci number. f2 is the next fibonacci number *)
		fun fib_help(f1, f2, pow2) =
			if pow2 = 1 then f1
			else
				let val next_n = n div (pow2 div 2);
				in
					if next_n mod 2 = 0 then
						fib_help(f1 * (2 * f2 - f1), sqr(f1) + sqr(f2), pow2 div 2)
					else
						fib_help(sqr(f1) + sqr(f2), f2 * (2 * f1 + f2), pow2 div 2)
				end;

        (* Returns minimum power of 2 greater than n *)
		fun min_pow2(curr) = 
			if curr > n then curr
			else min_pow2(curr * 2);
	in
		fib_help(0, 1, min_pow2(1))
	end;


(*
Recursive integer square root func
fn : int -> int
O(log n)
*)
fun sqrt(n) =
	if n = 0 then 0
	else
		let 
			val ans = sqrt(n div 4);
		in
			if sqr(2 * ans + 1) <= n then 2 * ans + 1
			else 2 * ans
		end;

(* Determines if the argument is a perfect number or not *)
fun is_perfect(n) =
	let
		(*Add all factors of n*)
		fun addfactors(n) =
		let
			fun factor(i) =
				if n mod i = 0 then i
				else 0;

			(*ans = sum of all factors of n less than i *)
			fun sum(f, i, ans) =
				if i = n then ans
				else sum(f, i + 1, ans + f(i));
		in
			sum(factor, 1, 0)
		end;
	in
		n = addfactors(n)
	end;