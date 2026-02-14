# Function to check if a number is prime
is_prime = lambda n: n > 1 and all(n % i != 0 for i in range(2, int(n**0.5) + 1))

# Input
numbers = list(map(int, input().split()))

# Filter primes
primes = list(filter(is_prime, numbers))

# Output
if primes:
    print(*primes)
else:
    print("No primes")
