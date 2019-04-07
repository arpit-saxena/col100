fun factorial(n) = if n = 0 then 1 else n * factorial(n - 1);
fun power(x, n) = if n = 0 then 1 else x * power(x, n - 1);
fun gcd(a, b) = 
    if a = b then a
    else if a > b then gcd(a - b, b)
    else gcd(a, b - a);

fun fibonacci(n) = 
    if n = 0 then 1
    else if n = 1 then 1
    else fibonacci(n - 1) + fibonacci(n - 2);

print(Int.toString (factorial(12)) ^ "\n");
