fun acc(a,b,f,succ,oper,iden,comp) = 
	if comp(a,b) then iden
	else oper(f(a),acc(succ(a),b,f,succ,oper,iden,comp));

fun compose (f,g) x = f(g(x));

fun repeat f n =
	if n = 0 then fn x => x
	else compose f (repeat f (n-1));

fun repeat2 f n = acc(1,n,fn a => f, fn a=>a+1, compose, fn x => x, op>);

fun mult x y = x*y;

fun map f [] = []
  | map f (x::ls) = (f x) :: (map f ls);

fun reduce f [] = []
  | reduce f (x::ls) = 
  	if f(x) then x::(reduce f ls)
	else reduce f ls;
  
