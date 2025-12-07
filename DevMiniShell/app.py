import os
import subprocess
import sys
from flask import Flask, render_template, request, jsonify

app = Flask(__name__, template_folder='templates', static_folder='static')

def get_desktop_path():
    potential_paths = [
        os.path.join(os.path.expanduser("~"), "Desktop"),
        os.path.join(os.path.expanduser("~"), "OneDrive", "Desktop")
    ]
    for path in potential_paths:
        if os.path.exists(path):
            return path
    return os.path.expanduser("~")

DESKTOP_PATH = get_desktop_path()
HISTORY_FILE = os.path.join(DESKTOP_PATH, "command_history.txt")

def save_to_history(command):
    try:
        with open(HISTORY_FILE, "a") as file:
            file.write(command + "\n")
    except Exception as e:
        return f"[History error] {e}"

def show_history():
    try:
        with open(HISTORY_FILE, "r") as file:
            return "".join(f"{i}: {line.strip()}\n" for i, line in enumerate(file, start=1))
    except FileNotFoundError:
        return "No history found."

def change_directory(command):
    parts = command.split(maxsplit=1)
    if len(parts) < 2:
        return "Usage: cd <directory>"
    try:
        os.chdir(parts[1])
        return f"Changed directory to {os.getcwd()}"
    except Exception as e:
        return f"[cd error] {e}"

def make_directory(foldername):
    try:
        path = os.path.join(DESKTOP_PATH, foldername)
        os.mkdir(path)
        return f"Folder '{foldername}' created on Desktop."
    except FileExistsError:
        return f"[mkdir error] Folder already exists."
    except Exception as e:
        return f"[mkdir error] {e}"

def make_file(filename):
    try:
        path = os.path.join(DESKTOP_PATH, filename)
        with open(path, "x") as f:
            pass
        return f"File '{filename}' created on Desktop."
    except FileExistsError:
        return f"[mkfile error] File already exists."
    except Exception as e:
        return f"[mkfile error] {e}"

def execute_command(command):
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, cwd=os.getcwd())
        return result.stdout + result.stderr
    except Exception as e:
        return f"[Execution error] {e}"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/command', methods=['POST'])
def handle_command():
    data = request.json
    command = data.get('command', '').strip()
    output = ""

    if not command:
        return jsonify({'output': output})

    save_to_history(command)

    if command == "exit":
        output = "Exiting DevMiniShell is not supported in the web version."
    elif command == "pwd":
        output = os.getcwd()
    elif command.startswith("cd "):
        output = change_directory(command)
    elif command.startswith("mkdir "):
        foldername = command.split(maxsplit=1)[1]
        output = make_directory(foldername)
    elif command.startswith("mkfile "):
        filename = command.split(maxsplit=1)[1]
        output = make_file(filename)
    elif command == "history":
        output = show_history()
    else:
        output = execute_command(command)

    return jsonify({'output': output})

if __name__ == "__main__":
    app.run(debug=True)
