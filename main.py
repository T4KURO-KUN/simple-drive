import os
import json
import shutil
import subprocess
from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, url_for, session, send_from_directory
from werkzeug.utils import secure_filename
load_dotenv()

app = Flask(__name__, template_folder='web', static_folder='web')
app.secret_key = os.urandom(24)
PASSWORD = os.getenv('PASSWORD')

DRIVE_ROOT = os.path.join(os.getcwd(), 'drive')
os.makedirs(DRIVE_ROOT, exist_ok=True)


def is_termux():
    return bool(os.getenv('TERMUX_VERSION')) or os.path.isdir('/data/data/com.termux')


def format_size(size):
    return f'{size / (1024 ** 3):.2f}'.rstrip('0').rstrip('.')


def get_device_status():
    usage = shutil.disk_usage(DRIVE_ROOT)
    storage = f'{format_size(usage.used)}/{format_size(usage.total)} Go'
    battery = 'N/A'

    if is_termux():
        try:
            result = subprocess.run(
                ['termux-battery-status'],
                capture_output=True,
                text=True,
                timeout=2,
                check=True
            )
            battery = f"{json.loads(result.stdout)['percentage']}%"
        except (FileNotFoundError, subprocess.SubprocessError, json.JSONDecodeError, KeyError):
            pass
    else:
        battery_file = '/sys/class/power_supply/BAT0/capacity'
        try:
            with open(battery_file, encoding='utf-8') as file:
                battery = f'{file.read().strip()}%'
        except (FileNotFoundError, OSError):
            pass

    return storage, battery

@app.route('/', defaults={'subpath': ''})
@app.route('/browse/<path:subpath>')
def main(subpath=''):
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    current_dir = os.path.join(DRIVE_ROOT, subpath)
    if not os.path.commonpath([DRIVE_ROOT, current_dir]) == DRIVE_ROOT or not os.path.exists(current_dir):
        return redirect(url_for('main'))

    items = []
    try:
        for entry in os.listdir(current_dir):
            entry_path = os.path.join(current_dir, entry)
            rel_path = os.path.join(subpath, entry) if subpath else entry
            
            items.append({
                'name': entry,
                'is_dir': os.path.isdir(entry_path),
                'path': rel_path
            })
    except FileNotFoundError:
        pass

    parent_path = os.path.dirname(subpath) if subpath else None
    storage, battery = get_device_status()

    return render_template(
        'main.html',
        items=items,
        current_subpath=subpath,
        parent_path=parent_path,
        storage=storage,
        battery=battery
    )

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

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))

@app.route('/import', methods=['POST'])
def import_files():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    subpath = request.form.get('subpath', '')
    current_dir = os.path.abspath(os.path.join(DRIVE_ROOT, subpath))
    if os.path.commonpath([DRIVE_ROOT, current_dir]) != DRIVE_ROOT or not os.path.isdir(current_dir):
        return redirect(url_for('main'))

    for uploaded_file in request.files.getlist('files'):
        filename = secure_filename(uploaded_file.filename or '')
        if filename:
            uploaded_file.save(os.path.join(current_dir, filename))

    return redirect(url_for('main', subpath=subpath) if subpath else url_for('main'))

@app.route('/drive/<path:filename>')
def download_file(filename):
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return send_from_directory(DRIVE_ROOT, filename, as_attachment=False)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)