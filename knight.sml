use "my_dfs.sml";

fun depthfirst next pred x =
	let
		fun dfs [] = []
		  | dfs (top::stack) =
			if pred(top) then top
			else   dfs(next(top)@stack)
	in
		dfs [x]
	end;

fun belongs(x, []) = false
  | belongs(x, q::qs) = if (x = q) then true else belongs(x, qs);

fun gen_next (a, b) = [
    (a + 2, b + 1),
    (a + 2, b - 1),
    (a + 1, b + 2),
    (a + 1, b - 2),
    (a - 1, b + 2),
    (a - 1, b - 2),
    (a - 2, b + 1),
    (a - 2, b - 1)
]

fun allowed n soln (a, b) = 
    a >= 1 andalso a <= n andalso b >= 1 andalso b <= n andalso not(belongs((a,b), soln));

fun finished n soln = (n * n = length(soln))

fun part_app f x y = f(x,y);

fun cartesian_product [] q = []
  | cartesian_product (a::qs) q = (map (fn b => [(a, b)]) q)@(cartesian_product qs q);

fun next_valid_pos n [] = cartesian_product (upto(1,n)) (upto(1,n))
  | next_valid_pos n (top::soln) = map (secr op:: (top::soln)) (filter (allowed n soln) (gen_next top))

fun knight n = depthfirst (next_valid_pos n) (finished n) [];