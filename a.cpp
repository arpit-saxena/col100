#include <iostream>
#include <utility>
#include <tuple>

std::pair<long long, long long> fib_help(long long n)
{
    if(n == 0)
    {
        return std::make_pair(0, 1);
    }
    else if(n == 1)
    {
        return std::make_pair(1, 1);
    }
    else
    {
        long long f1, f2;
        std::tie(f1, f2) = fib_help(n / 2);
        if(n % 2 == 0)
        {
            return std::make_pair(f1 * (2 * f2 - f1), f1 * f1 + f2 * f2);
        }
        else
        {
            return std::make_pair(f1 * f1 + f2 * f2, f2 * (2 * f1 + f2));
        }
    }
    return std::make_pair(0, 0);
}

long long fib(long long n)
{
    return fib_help(n).first;
}

constexpr long long fib_bad(long long n)
{
    if(n == 0) return 0;
    else if(n == 1) return 1;
    else return fib_bad(n - 1) + fib_bad(n - 2);
}

long long fib_bad2(long long n)
{
    if(n == 0) return 0;
    else if(n == 1) return 1;

    long long a = 0, b = 1, i = 2;
    while(i <= n)
    {
        long long temp = a;
        a = b;
        b = temp + a;
        i++;
    }

    return a;
}

int main()
{
	const long long ans = fib_bad(40);
    std::cout << ans << std::endl;
}
