import os
import subprocess
import sys

# Automatically detect Desktop path (OneDrive-aware)
def get_desktop_path():
    potential_paths = [
        os.path.join(os.path.expanduser("~"), "Desktop"),
        os.path.join(os.path.expanduser("~"), "OneDrive", "Desktop")
    ]
    for path in potential_paths:
        if os.path.exists(path):
            return path
    return os.path.expanduser("~")  # Fallback to user home

DESKTOP_PATH = get_desktop_path()
HISTORY_FILE = os.path.join(DESKTOP_PATH, "command_history.txt")

def save_to_history(command):
    try:
        with open(HISTORY_FILE, "a") as file:
            file.write(command + "\n")
    except Exception as e:
        print(f"[History error] {e}")

def show_history():
    try:
        with open(HISTORY_FILE, "r") as file:
            for i, line in enumerate(file, start=1):
                print(f"{i}: {line.strip()}")
    except FileNotFoundError:
        print("No history found.")

def change_directory(command):
    parts = command.split(maxsplit=1)
    if len(parts) < 2:
        print("Usage: cd <directory>")
        return
    try:
        os.chdir(parts[1])
    except Exception as e:
        print(f"[cd error] {e}")

def open_desktop_folder():
    try:
        if os.name == 'nt':
            subprocess.Popen(['explorer', DESKTOP_PATH])
        elif sys.platform == 'darwin':
            subprocess.Popen(['open', DESKTOP_PATH])
        else:
            subprocess.Popen(['xdg-open', DESKTOP_PATH])
    except Exception as e:
        print(f"[Open error] {e}")

def make_directory(foldername):
    try:
        path = os.path.join(DESKTOP_PATH, foldername)
        os.mkdir(path)
        print(f"Folder '{foldername}' created on Desktop.")
        open_desktop_folder()
    except FileExistsError:
        print(f"[mkdir error] Folder already exists.")
    except Exception as e:
        print(f"[mkdir error] {e}")

def make_file(filename):
    try:
        path = os.path.join(DESKTOP_PATH, filename)
        with open(path, "x") as f:
            pass
        print(f"File '{filename}' created on Desktop.")
        open_desktop_folder()
    except FileExistsError:
        print(f"[mkfile error] File already exists.")
    except Exception as e:
        print(f"[mkfile error] {e}")

def write_file(filename):
    try:
        path = os.path.join(DESKTOP_PATH, filename)
        with open(path, "w") as f:
            print("Enter content below (type '::end' to finish):")
            while True:
                line = input()
                if line == "::end":
                    break
                f.write(line + "\n")
        print(f"Text written to '{filename}' on Desktop.")
        open_desktop_folder()
    except Exception as e:
        print(f"[write error] {e}")

def execute_command(command):
    background = False
    stdin = None
    stdout = None

    try:
        if command.endswith("&"):
            background = True
            command = command[:-1].strip()

        if ">" in command:
            parts = command.split(">")
            command = parts[0].strip()
            output_file = parts[1].strip()
            stdout = open(output_file, "w")

        if "<" in command:
            parts = command.split("<")
            command = parts[0].strip()
            input_file = parts[1].strip()
            stdin = open(input_file, "r")

        if background:
            subprocess.Popen(command, shell=True, stdin=stdin, stdout=stdout, stderr=subprocess.STDOUT)
        else:
            subprocess.run(command, shell=True, stdin=stdin, stdout=stdout, stderr=subprocess.STDOUT)

    except FileNotFoundError:
        print(f"[Command not found] '{command}'")
    except Exception as e:
        print(f"[Execution error] {e}")
    finally:
        if stdout:
            stdout.close()
        if stdin:
            stdin.close()

def main():
    os.chdir(DESKTOP_PATH)

    while True:
        try:
            command = input("DevMiniShell> ").strip()
            if not command:
                continue

            save_to_history(command)

            if command == "exit":
                print("Exiting DevMiniShell.")
                break
            elif command == "pwd":
                print(os.getcwd())
            elif command.startswith("cd "):
                change_directory(command)
            elif command.startswith("mkdir "):
                foldername = command.split(maxsplit=1)[1]
                make_directory(foldername)
            elif command.startswith("mkfile "):
                filename = command.split(maxsplit=1)[1]
                make_file(filename)
            elif command.startswith("write "):
                filename = command.split(maxsplit=1)[1]
                write_file(filename)
            elif command == "history":
                show_history()
            else:
                execute_command(command)

        except KeyboardInterrupt:
            print("\n[Interrupted] Type 'exit' to quit.")
        except EOFError:
            print("\nExiting DevMiniShell.")
            break
        except Exception as e:
            print(f"[Unexpected error] {e}")

if __name__ == "__main__":
    main()
