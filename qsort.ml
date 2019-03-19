fun append([], []) = []
  | append([], l2) = l2
  | append(x::l1, l2) =
  	(* IH: append(l, r) appends list r to l for all where size(l) <= size(l1) and size(r) < size(l2) *)
	x::append(l1,l2);

fun partition(ls, x) = 
	let
		fun partition_help(left, right, []) = (left, right)
		  | partition_help(left, right, elem::ls) = 
		  	(* INV: for all a in left: a <= ls and for all b in right b > ls *)
		  	if elem <= x then partition_help(elem::left, right, ls)
			else partition_help(left, elem::right, ls);
	in
		partition_help([],[],ls)
	end;

fun qsort([]) = []
  | qsort([x]) = [x]
  | qsort(x::ls) =
  	(* IH: qsort returns sorted list for lists with length less than equal to that of ls  *)
	let
		val (l,r) = partition(ls, x)
	in
		append(qsort(l), x::qsort(r))
	end;
