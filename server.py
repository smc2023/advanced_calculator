"""
Python-only web server for the calculator. No PHP or Homebrew needed.
Run: python3 server.py
Then open http://localhost:8080 in your browser.
"""
import html
import os
import urllib.parse
from http.server import HTTPServer, BaseHTTPRequestHandler

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(SCRIPT_DIR)


def compute(operation, num1, num2):
    """Run the requested operation using the calculator modules. Returns (result_string, is_error)."""
    valid_ops = ["add", "subtract", "multiply", "divide", "factorial"]
    if operation not in valid_ops:
        return "Invalid operation.", True
    if operation == "factorial":
        if num1 == "" and num1 != "0":
            return "Enter a non-negative integer for factorial.", True
        try:
            n = int(num1)
            if n < 0:
                return "Factorial requires a non-negative integer.", True
        except ValueError:
            return "Factorial requires a non-negative integer.", True
        try:
            from factorial import factorial
            return str(factorial(n)), False
        except Exception:
            return "Error computing factorial.", True
    # Binary operations
    if num1 == "" or num2 == "":
        return "Please enter both numbers.", True
    try:
        a, b = float(num1), float(num2)
    except ValueError:
        return "Please enter valid numbers.", True
    if operation == "divide" and b == 0:
        return "Cannot divide by zero.", True
    try:
        if operation == "add":
            from addition import add
            result = add(a, b)
        elif operation == "subtract":
            from subtraction import subtract
            result = subtract(a, b)
        elif operation == "multiply":
            from multiplication import multiply
            result = multiply(a, b)
        else:  # divide
            from division import divide
            result = divide(a, b)
        return str(result), False
    except Exception:
        return "Error computing result.", True


def render_page(result_text="Result will appear here", result_class="empty", operation="add", num1="", num2=""):
    """Load index.html and fill in the placeholders."""
    path = os.path.join(SCRIPT_DIR, "index.html")
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    selected = {op: " selected" if op == operation else "" for op in ["add", "subtract", "multiply", "divide", "factorial"]}
    content = content.replace("{{RESULT_TEXT}}", html.escape(result_text))
    content = content.replace("{{RESULT_CLASS}}", result_class)
    content = content.replace("{{NUM1}}", html.escape(num1))
    content = content.replace("{{NUM2}}", html.escape(num2))
    for op in selected:
        content = content.replace("{{SELECTED_" + op + "}}", selected[op])
    return content


def serve_file(path, content_type, handler):
    """Serve a static file from SCRIPT_DIR."""
    filepath = os.path.join(SCRIPT_DIR, path.lstrip("/"))
    if not os.path.isfile(filepath) or not os.path.abspath(filepath).startswith(SCRIPT_DIR):
        handler.send_error(404)
        return
    with open(filepath, "rb") as f:
        data = f.read()
    handler.send_response(200)
    handler.send_header("Content-Type", content_type)
    handler.send_header("Content-Length", str(len(data)))
    handler.end_headers()
    handler.wfile.write(data)


class CalculatorHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        path = self.path.split("?")[0] or "/"
        if path == "/" or path == "/index.html":
            body = render_page().encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
        elif path == "/styles.css":
            serve_file("/styles.css", "text/css", self)
        else:
            self.send_error(404)

    def do_POST(self):
        path = self.path.split("?")[0] or "/"
        if path != "/" and path != "/index.html":
            self.send_error(404)
            return
        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length).decode("utf-8")
        data = urllib.parse.parse_qs(body)
        operation = (data.get("operation") or ["add"])[0].strip()
        num1 = (data.get("num1") or [""])[0].strip()
        num2 = (data.get("num2") or [""])[0].strip()
        result_text, is_error = compute(operation, num1, num2)
        result_class = "error" if is_error else "success"
        page = render_page(result_text, result_class, operation, num1, num2)
        out = page.encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(out)))
        self.end_headers()
        self.wfile.write(out)

    def log_message(self, format, *args):
        print(args[0])


def main():
    # Use PORT env var if provided (e.g. by AWS App Runner), otherwise default to 8080.
    port = int(os.environ.get("PORT", "8080"))
    for attempt in range(10):
        try:
            server = HTTPServer(("0.0.0.0", port), CalculatorHandler)
            break
        except OSError as e:
            if e.errno == 48:  # Address already in use
                port += 1
                continue
            raise
    else:
        print("No free port found between 8080 and {}.".format(port - 1))
        return
    print("Calculator running at http://localhost:{}/".format(port))
    print("Press Ctrl+C to stop.")
    server.serve_forever()


if __name__ == "__main__":
    main()
