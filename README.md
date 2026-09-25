
# 📂 Simple Drive

A lightweight, self-hosted local cloud storage solution built with Python (Flask). It features a clean web interface and is designed to run seamlessly on standard **Linux** distributions as well as **Termux (Android)**.


## ✨ Features

* **File Explorer:** Navigate through directories and subdirectories effortlessly.
* **Upload & Download:** Import new files via the web UI or download them directly.
* **Secure Authentication:** Protected by a password managed via a `.env` file.
* **Cross-Platform:** Works natively on standard Linux and Android via Termux.
* **Live Status:** Real-time monitoring of disk space and battery level.


## 🛠️ Requirements & Dependencies

The project relies on the following Python packages (`requirements.txt`):

* **Flask**: Micro web framework for the server and routing.
* **python-dotenv**: Loads environment variables securely from a `.env` file.
* **Werkzeug**: Secures uploaded filenames against path traversal attacks.

### Extra requirement for Termux (Android):

If you are running this on Termux and want the live **battery status** feature to work, you must install the **Termux-API** package and the companion Android app:

1. Install the Termux-API app on your Android device (from F-Droid or Github).
2. Install the package inside Termux:
```bash
pkg install termux-api

```


## 🚀 Installation & Setup

### 1. Configure the Environment File

move the `.env.example` file to `.env` and set your admin password:

```bash
cp .env.example .env
```
```env
PASSWORD=your_secure_password
```

### 2. Install Dependencies

Install all required Python packages using `requirements.txt`:

```bash
pip install -r requirements.txt

```

### 3. Run the Server

Start the Flask application:

```bash
python main.py

```

### 4. Access Simple Drive

Open your web browser and go to:

* **Local access:** `http://127.0.0.1:5000`
* **Network access:** `http://<your_device_ip>:5000`



## 📁 Project Structure

```text
.
├── README.md
├── drive/             # Root storage directory (created automatically)
├── main.py            # Core Flask server script
├── requirements.txt   # Python dependencies list
└── web/               # Web interface assets
    ├── css/
    │   ├── login.css
    │   └── main.css
    ├── js/
    │   ├── cbz-reader.js
    │   └── main.js
    ├── login.html
    └── main.html

```