fun add(a, b) = 
	let
		fun add_help(res, [], [], carry) = 
			if carry > 0 then carry::res
			else res
		  | add_help(res, a::x, b::y, carry) =
		  	add_help(((a + b + carry) mod 10)::res, x, y, (a + b + carry) div 10)
	in
		add_help([], a, b, 0)
	end;
