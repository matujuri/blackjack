
base_template = '''
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Blackjack Game</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            min-height: 100vh;
            background-color: #f3f3f3;
        }
        .container {
            width: 90%;
            max-width: 600px;
            margin: auto;
            text-align: center;
        }
        img {
            max-width: 100%;
            height: auto;
        }
        a, button {
            display: inline-block;
            margin: 10px;
            padding: 10px 20px;
            background-color: #007bff;
            color: white;
            text-decoration: none;
            border: none;
            border-radius: 5px;
            cursor: pointer;
        }
        a:hover, button:hover {
            background-color: #0056b3;
        }
        .logo {
            font-size: 10px; /* ロゴのフォントサイズを小さくする */
            line-height: 1; /* 行間隔を詰める */
            white-space: pre; /* フォーマットを保持する */
            overflow-x: auto; /* 必要に応じてスクロール可能にする */
        }
        .background-image {
            background-image: url('/static/images/background.jpeg');
            background-size: contain;
            # background-repeat: no-repeat;
        }
    </style>
</head>
<body class="background-image">
    <select id="languageSelect" onchange="changeLanguage()">
    <option value="en" {{ 'selected' if selected_language == 'en' else '' }}>English</option>
    <option value="ja" {{ 'selected' if selected_language == 'ja' else '' }}>日本語</option>
    <option value="zh" {{ 'selected' if selected_language == 'zh' else '' }}>中文</option>
    </select>

    <div class="container">
        <pre>{{ logo }}</pre>
        <!-- コンテンツはここに入れる -->
        {{ content }}
    </div>
    <script>
    function changeLanguage() {
        var selectedLanguage = document.getElementById('languageSelect').value;
        window.location.href = '/change_language?lang=' + selectedLanguage;
    }
    </script>
</body>
</html>
'''
