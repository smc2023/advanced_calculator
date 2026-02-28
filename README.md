# Advanced Calculator

A small calculator web app with add, subtract, multiply, divide, and factorial. The UI is HTML/CSS; the logic lives in Python modules.

## Run locally (Python only)

No PHP or extra installs needed—just Python 3:

```bash
cd "advanced calculator "
python3 server.py
```

Then open **http://localhost:8080** (or the port printed in the terminal) in your browser.

## Project layout

- **server.py** – Web server (stdlib only); serves the form and runs the calculations.
- **index.html** – Calculator form and UI.
- **styles.css** – Styles for the calculator.
- **addition.py**, **subtraction.py**, **multiplication.py**, **division.py**, **factorial.py** – Operation logic.
- **app.py** – CLI dispatcher: `python3 app.py <operation> [arg1] [arg2]` (e.g. `python3 app.py add 2 3`).
- **index.php** – Same UI for a PHP environment (if you have PHP and want to use it instead of `server.py`).
