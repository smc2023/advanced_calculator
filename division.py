def divide(a: float, b: float) -> float:
    """Return a divided by b. Raises ZeroDivisionError if b is 0."""
    if b == 0:
        raise ZeroDivisionError("Cannot divide by zero")
    return a / b


if __name__ == "__main__":
    import sys
    if len(sys.argv) != 3:
        sys.exit(1)
    try:
        x, y = float(sys.argv[1]), float(sys.argv[2])
        print(divide(x, y))
    except (ValueError, ZeroDivisionError):
        sys.exit(1)
