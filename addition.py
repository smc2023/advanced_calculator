def add(a: float, b: float) -> float:
    """Return the sum of a and b."""
    return a + b


if __name__ == "__main__":
    import sys
    if len(sys.argv) != 3:
        sys.exit(1)
    try:
        x, y = float(sys.argv[1]), float(sys.argv[2])
        print(add(x, y))
    except ValueError:
        sys.exit(1)
