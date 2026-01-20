from flask import Flask, request, redirect, url_for
import os
import datetime
from collections import Counter

app = Flask(__name__)
DATA_FILE = "data/votes.txt"

# Ensure the data file exists
if not os.path.exists('data'):
    os.makedirs('data')

@app.route('/')
def index():
    return """
    <html>
        <head>
            <title>The Tech Poll v2</title>
            <style>
                body { font-family: sans-serif; text-align: center; padding: 50px; }
                button { padding: 15px 30px; font-size: 18px; margin: 10px; cursor: pointer; }
                .python { background-color: #3776ab; color: white; border: none; }
                .rust { background-color: #000000; color: white; border: none; }
                .go { background-color: #00add8; color: white; border: none; }
                .js { background-color: #f7df1e; color: black; border: none; } /* NEW BUTTON STYLE */
            </style>
        </head>
        <body>
            <h1>Which language is the future?</h1>
            <form action="/vote" method="post">
                <button class="python" name="choice" value="Python">Python</button>
                <button class="rust" name="choice" value="Rust">Rust</button>
                <button class="go" name="choice" value="Go">Go</button>
                <button class="js" name="choice" value="JavaScript">JavaScript</button>
            </form>
        </body>
    </html>
    """

@app.route('/vote', methods=['POST'])
def vote():
    choice = request.form['choice']
    user_ip = request.remote_addr
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # NEW: Write to a human-readable text file
    # "a" means Append (add to the end without deleting old stuff)
    with open(DATA_FILE, "a") as f:
        f.write(f"{timestamp} | {choice} | {user_ip}\n")
    
    return redirect(url_for('results'))

@app.route('/results')
def results():
    # Read the text file to count votes
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            lines = f.readlines()
        
        # Extract just the choices (the middle part of the line)
        # Line format: "2024-01-20 10:00:00 | Python | 127.0.0.1"
        votes = []
        for line in lines:
            parts = line.split(" | ")
            if len(parts) >= 2:
                votes.append(parts[1])
        
        # Count them
        counts = Counter(votes)
        
        # Create HTML Rows
        rows = ""
        for language, count in counts.items():
            rows += f"<tr><td>{language}</td><td>{count}</td></tr>"
            
    else:
        rows = "<tr><td colspan='2'>No votes yet</td></tr>"
    
    return f"""
    <html>
        <body style="font-family: sans-serif; text-align: center; padding: 50px;">
            <h1>Poll Results (Text File Backend)</h1>
            <table border="1" style="margin: 0 auto; width: 50%;">
                <tr><th>Language</th><th>Votes</th></tr>
                {rows}
            </table>
            <br>
            <a href="/">Back to Vote</a>
        </body>
    </html>
    """

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)