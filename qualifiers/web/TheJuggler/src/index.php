<?php
// Set content type based on request method
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    header('Content-Type: application/json');

    // Read raw input
    $input = file_get_contents('php://input');
    $data = json_decode($input, true);

    if (!isset($data['guess'])) {
        echo json_encode(['result' => 'invalid input']);
        exit;
    }

    $original = 'thejuggler';

    $juggled = str_shuffle($original);

    if ($data['guess'] == $juggled) {
        $flag = getenv('FLAG');
        echo json_encode(['result' => $flag]);
    } else {
        echo json_encode(['result' => 'wrong answer!']);
    }

    exit;
}
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>The Juggler</title>
    <style>
        body {
            background: #1a1a1a;
            color: #f0f0f0;
            font-family: monospace;
            text-align: center;
            margin-top: 10%;
        }
        h1 {
            color: #f9a825;
        }
        form {
            margin-top: 20px;
        }
        input[type="text"] {
            padding: 8px;
            width: 300px;
            font-size: 16px;
            border-radius: 5px;
            border: none;
        }
        input[type="submit"] {
            padding: 8px 16px;
            margin-left: 10px;
            font-size: 16px;
            border-radius: 5px;
            border: none;
            background-color: #f9a825;
            color: #000;
            cursor: pointer;
        }
    </style>
</head>
<body>
    <h1>Welcome to The Juggler!</h1>
    <p>I have juggled the characters in the string "<strong>thejuggler</strong>".<br>
       Can you guess the new string?<br>
       Every time you make a guess, I will juggle the characters again!</p>

    <form id="jugglerForm">
        <input type="text" id="guess" name="guess" required />
        <input type="submit" value="Submit Guess" />
    </form>

    <p id="result"></p>

    <script>
        const form = document.getElementById('jugglerForm');
        const result = document.getElementById('result');

        form.addEventListener('submit', async (e) => {
            e.preventDefault();
            const guess = document.getElementById('guess').value;

            const response = await fetch('', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ guess: guess })
            });

            const data = await response.json();
            result.textContent = data.result;
        });
    </script>
</body>
</html>
