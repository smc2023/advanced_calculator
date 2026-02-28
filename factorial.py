def factorial(n: int) -> int:
    """Return n! for non-negative integer n. Raises ValueError if n < 0 or not integer."""
    if n < 0:
        raise ValueError("Factorial not defined for negative numbers")
    if n != int(n):
        raise ValueError("Factorial requires an integer")
    n = int(n)
    if n == 0 or n == 1:
        return 1
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result


if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        sys.exit(1)
    try:
        x = int(sys.argv[1])
        if x < 0:
            sys.exit(1)
        print(factorial(x))
    except (ValueError, TypeError):
        sys.exit(1)
