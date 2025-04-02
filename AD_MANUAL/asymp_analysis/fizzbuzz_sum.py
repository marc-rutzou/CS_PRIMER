def quotient(n, d):
    return (n - n % d) // d

def sum_up_to(n):
    return (n * (n + 1)) // 2

def fizz(n, x):
    return x * sum_up_to(quotient(n, x)) 

def fizzbuzz(n):
    return fizz(n, 3) + fizz(n, 5) - fizz(n, 15)

if __name__ == "__main__":
    print(fizzbuzz(20))


