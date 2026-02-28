"""
Calculator dispatcher: runs the appropriate Python module from command line.
Usage: python app.py <operation> [arg1] [arg2]
Operations: add, subtract, multiply, divide, factorial
For factorial only one argument is used.
"""
import sys
import os

# Run from this script's directory so imports work
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(SCRIPT_DIR)

def main():
    if len(sys.argv) < 2:
        sys.exit(1)
    op = sys.argv[1].lower()
    if op == "add":
        if len(sys.argv) != 4:
            sys.exit(1)
        from addition import add
        print(add(float(sys.argv[2]), float(sys.argv[3])))
    elif op == "subtract":
        if len(sys.argv) != 4:
            sys.exit(1)
        from subtraction import subtract
        print(subtract(float(sys.argv[2]), float(sys.argv[3])))
    elif op == "multiply":
        if len(sys.argv) != 4:
            sys.exit(1)
        from multiplication import multiply
        print(multiply(float(sys.argv[2]), float(sys.argv[3])))
    elif op == "divide":
        if len(sys.argv) != 4:
            sys.exit(1)
        from division import divide
        try:
            print(divide(float(sys.argv[2]), float(sys.argv[3])))
        except ZeroDivisionError:
            sys.exit(2)  # signal for "divide by zero"
    elif op == "factorial":
        if len(sys.argv) != 3:
            sys.exit(1)
        from factorial import factorial
        n = int(sys.argv[2])
        if n < 0:
            sys.exit(1)
        print(factorial(n))
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
