fun depthfirst next pred x =
	let
		fun dfs [] = []
		  | dfs (top::stack) =
			if pred(top) then top::(dfs stack)
			else   dfs(next(top)@stack)
	in
		dfs [x]
	end;

(*OKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKK*)
fun secr f y x = f(x,y); (*Reverse application*)

fun map f [] = []
  | map f (x::ls) = f(x)::(map f ls);


fun filter pred [] = []
  | filter pred (x::ls) =
		if pred(x) then x::(filter pred ls)
		else (filter pred ls);

fun upto(m, n) =
	if m > n then []
	else m::upto(m+1,n);

fun isfull n soln = (n = length(soln));

(*OKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKK*)

fun safe soln newq = 
	let
		fun belongs(x, []) = false
		  | belongs(x, q::qs) = if (x = q) then true else belongs(x, qs);
		
		fun nodiag(i, []) = true
		  | nodiag(i, q::soln) = (Int.abs(q - newq) <> i) andalso nodiag(i+1,soln)
	in
		not(belongs(newq, soln)) andalso nodiag(1, soln)
	end;

fun nextqueen n soln = map (secr op:: soln) (filter (safe soln) (upto(1,n)));

fun queen n = depthfirst (nextqueen n) (isfull n) [];

