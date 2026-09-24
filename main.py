import os
from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, url_for, session
load_dotenv()

app = Flask(__name__, template_folder='web', static_folder='web')
app.secret_key = os.urandom(24)
PASSWORD = os.getenv('PASSWORD')

@app.route('/')
def main():
    if session.get('logged_in'):
        return render_template('main.html')
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if session.get('logged_in'):
        return redirect(url_for('main'))

    error = None
    if request.method == 'POST':
        if PASSWORD and request.form.get('password') == PASSWORD:
            session['logged_in'] = True
            return redirect(url_for('main'))
        else:
            error = "Wrong password"

    return render_template('login.html', error=error)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)