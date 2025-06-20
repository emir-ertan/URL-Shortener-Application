import sqlite3
import secrets
import string
from flask import Flask, request, redirect, render_template, g, url_for

DATABASE = 'urls.db'
SHORT_CODE_LENGTH = 6

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here' # Change this for security

def get_db():
    """Returns the database connection."""
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row # To access columns by name
    return db

@app.teardown_appcontext
def close_db(error):
    """Closes the database connection when the request ends."""
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def generate_short_code(length=SHORT_CODE_LENGTH):
    """Generates a unique short code."""
    characters = string.ascii_letters + string.digits
    while True:
        short_code = ''.join(secrets.choice(characters) for i in range(length))
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT id FROM urls WHERE short_code = ?", (short_code,))
        if cursor.fetchone() is None:
            return short_code

@app.route('/')
def index():
    """Displays the home page."""
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT original_url, short_code FROM urls ORDER BY id DESC")
    urls = cursor.fetchall()
    return render_template('index.html', urls=urls)

@app.route('/shorten', methods=['POST'])
def shorten_url():
    """Handles the URL shortening request."""
    original_url = request.form['original_url']
    if not original_url:
        return render_template('index.html', error="Please enter a URL.")

    db = get_db()
    cursor = db.cursor()

    # Check if the same URL has been shortened before
    cursor.execute("SELECT short_code FROM urls WHERE original_url = ?", (original_url,))
    existing_short_code = cursor.fetchone()

    if existing_short_code:
        short_code = existing_short_code['short_code']
    else:
        short_code = generate_short_code()
        cursor.execute("INSERT INTO urls (original_url, short_code) VALUES (?, ?)", (original_url, short_code))
        db.commit()

    # Query again to display the shortened URL on the home page
    cursor.execute("SELECT original_url, short_code FROM urls ORDER BY id DESC")
    urls = cursor.fetchall()

    return render_template('index.html', short_url=request.host_url + short_code, urls=urls)

@app.route('/<short_code>')
def redirect_to_original(short_code):
    """Redirects from short code to original URL."""
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT original_url FROM urls WHERE short_code = ?", (short_code,))
    url_entry = cursor.fetchone()

    if url_entry:
        return redirect(url_entry['original_url'])
    else:
        return render_template('index.html', error="Invalid short code.")

@app.route('/delete/<short_code>', methods=['POST'])
def delete_url(short_code):
    """Deletes the URL specified by the short code from the database."""
    db = get_db()
    cursor = db.cursor()
    cursor.execute("DELETE FROM urls WHERE short_code = ?", (short_code,))
    db.commit()
    return redirect(url_for('index')) # Redirect to home page after deletion

if __name__ == '__main__':
    from database import init_db
    init_db() # Initialize the database before starting the app
    app.run(debug=True)