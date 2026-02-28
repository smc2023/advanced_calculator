<?php
$result = null;
$isError = false;
$operation = '';
$num1 = '';
$num2 = '';

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $operation = isset($_POST['operation']) ? trim($_POST['operation']) : '';
    $num1 = isset($_POST['num1']) ? trim($_POST['num1']) : '';
    $num2 = isset($_POST['num2']) ? trim($_POST['num2']) : '';

    $validOps = ['add', 'subtract', 'multiply', 'divide', 'factorial'];
    if (!in_array($operation, $validOps)) {
        $result = 'Invalid operation.';
        $isError = true;
    } elseif ($operation === 'factorial') {
        if ($num1 === '' && $num1 !== '0') {
            $result = 'Enter a non-negative integer for factorial.';
            $isError = true;
        } else {
            $n = (int) $num1;
            if ($n < 0 || (string) $n !== $num1) {
                $result = 'Factorial requires a non-negative integer.';
                $isError = true;
            } else {
                $dir = __DIR__;
                $cmd = sprintf(
                    'python3 %s/app.py factorial %s 2>/dev/null',
                    escapeshellarg($dir),
                    escapeshellarg((string) $n)
                );
                $output = @shell_exec($cmd);
                if ($output === null || $output === '') {
                    $result = 'Error computing factorial.';
                    $isError = true;
                } else {
                    $result = trim($output);
                }
            }
        }
    } else {
        if ($num1 === '' || $num2 === '') {
            $result = 'Please enter both numbers.';
            $isError = true;
        } elseif (!is_numeric($num1) || !is_numeric($num2)) {
            $result = 'Please enter valid numbers.';
            $isError = true;
        } elseif ($operation === 'divide' && (float) $num2 === 0.0) {
            $result = 'Cannot divide by zero.';
            $isError = true;
        } else {
            $dir = __DIR__;
            $cmd = sprintf(
                'python3 %s/app.py %s %s %s 2>/dev/null',
                escapeshellarg($dir),
                escapeshellarg($operation),
                escapeshellarg($num1),
                escapeshellarg($num2)
            );
            $output = @shell_exec($cmd);
            if ($output === null || $output === '') {
                $result = 'Error computing result.';
                $isError = true;
            } else {
                $result = trim($output);
            }
        }
    }
}
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Advanced Calculator</title>
    <link rel="stylesheet" href="styles.css">
</head>
<body>
    <div class="calculator" id="calc">
        <h1>Advanced Calculator</h1>
        <form method="post" action="">
            <div class="form-row">
                <label for="operation">Operation</label>
                <select name="operation" id="operation" required>
                    <option value="add" <?php echo $operation === 'add' ? 'selected' : ''; ?>>Add (+)</option>
                    <option value="subtract" <?php echo $operation === 'subtract' ? 'selected' : ''; ?>>Subtract (−)</option>
                    <option value="multiply" <?php echo $operation === 'multiply' ? 'selected' : ''; ?>>Multiply (×)</option>
                    <option value="divide" <?php echo $operation === 'divide' ? 'selected' : ''; ?>>Divide (÷)</option>
                    <option value="factorial" <?php echo $operation === 'factorial' ? 'selected' : ''; ?>>Factorial (!)</option>
                </select>
            </div>
            <div class="form-row">
                <label for="num1" id="label-num1">First number</label>
                <input type="text" name="num1" id="num1" value="<?php echo htmlspecialchars($num1); ?>" placeholder="e.g. 12" inputmode="decimal" autocomplete="off">
            </div>
            <div class="form-row" id="row-num2">
                <label for="num2">Second number</label>
                <input type="text" name="num2" id="num2" value="<?php echo htmlspecialchars($num2); ?>" placeholder="e.g. 5" inputmode="decimal" autocomplete="off">
            </div>
            <div class="submit-row">
                <button type="submit">Calculate</button>
            </div>
        </form>
        <?php if ($result !== null): ?>
        <div class="result-box <?php echo $isError ? 'error' : 'success'; ?>">
            <?php echo htmlspecialchars($result); ?>
        </div>
        <?php else: ?>
        <div class="result-box empty">Result will appear here</div>
        <?php endif; ?>
    </div>
    <script>
        (function() {
            var op = document.getElementById('operation');
            var rowNum2 = document.getElementById('row-num2');
            var labelNum1 = document.getElementById('label-num1');
            var num1 = document.getElementById('num1');
            function toggleFactorial() {
                var isFactorial = op.value === 'factorial';
                rowNum2.style.display = isFactorial ? 'none' : 'block';
                labelNum1.textContent = isFactorial ? 'Number (non-negative integer)' : 'First number';
                num1.placeholder = isFactorial ? 'e.g. 5' : 'e.g. 12';
            }
            op.addEventListener('change', toggleFactorial);
            toggleFactorial();
        })();
    </script>
</body>
</html>
