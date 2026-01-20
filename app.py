from flask import Flask, render_template_string, request, redirect, url_for
import sqlite3
import socket

app = Flask(__name__)
DB_NAME = "data/votes.db"

# Initialize Database
def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    # Create table if it doesn't exist
    c.execute('''CREATE TABLE IF NOT EXISTS votes 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                  choice TEXT, 
                  ip_address TEXT)''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return """
    <html>
        <head>
            <title>The Tech Poll</title>
            <style>
                body { font-family: sans-serif; text-align: center; padding: 50px; }
                button { padding: 15px 30px; font-size: 18px; margin: 10px; cursor: pointer; }
                .python { background-color: #3776ab; color: white; border: none; }
                .rust { background-color: #000000; color: white; border: none; }
                .go { background-color: #00add8; color: white; border: none; }
            </style>
        </head>
        <body>
            <h1>Which language is the future?</h1>
            <form action="/vote" method="post">
                <button class="python" name="choice" value="Python">Python</button>
                <button class="rust" name="choice" value="Rust">Rust</button>
                <button class="go" name="choice" value="Go">Go</button>
            </form>
        </body>
    </html>
    """

@app.route('/vote', methods=['POST'])
def vote():
    choice = request.form['choice']
    user_ip = request.remote_addr
    
    # Save to Database
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("INSERT INTO votes (choice, ip_address) VALUES (?, ?)", (choice, user_ip))
    conn.commit()
    conn.close()
    
    return redirect(url_for('results'))

@app.route('/results')
def results():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    
    # Get counts
    c.execute("SELECT choice, COUNT(*) FROM votes GROUP BY choice")
    data = c.fetchall()
    conn.close()
    
    # Simple HTML table for results
    rows = "".join([f"<tr><td>{row[0]}</td><td>{row[1]}</td></tr>" for row in data])
    
    return f"""
    <html>
        <body style="font-family: sans-serif; text-align: center; padding: 50px;">
            <h1>Poll Results</h1>
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
    # Ensure database exists before starting
    import os
    if not os.path.exists('data'):
        os.makedirs('data')
    init_db()
    app.run(host='0.0.0.0', port=80)