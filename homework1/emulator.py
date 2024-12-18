import os
import tarfile
import csv
import sys
import argparse
import datetime

class ShellEmulator:
    def __init__(self, config_file):
        self.current_path = "/"
        self.history = []
        self.username = os.getenv("USER", "user")
        self.computer_name = "localhost"
        self.virtual_fs_path = ""
        self.log_file_path = ""
        self.startup_script_path = ""

        self.virtual_fs_dir = "virtual_fs"

        self.read_config(config_file)
        self.extract_virtual_fs()
        self.log_action("Эмулятор запущен")

    def read_config(self, config_file):
        """Load configuration from the provided CSV file."""
        try:
            with open(config_file, newline='') as csvfile:
                reader = csv.reader(csvfile)
                config = {row[0]: row[1] for row in reader}

            self.computer_name = config.get("computer_name", self.computer_name)
            self.virtual_fs_path = config.get("virtual_fs_path", "")
            self.log_file_path = config.get("log_file_path", "")
            self.startup_script_path = config.get("startup_script_path", "")

            if not self.virtual_fs_path or not os.path.exists(self.virtual_fs_path):
                print("Ошибка: путь к виртуальной файловой системе некорректен.")
                sys.exit(1)

        except Exception as e:
            print(f"Ошибка чтения конфигурационного файла: {str(e)}")
            sys.exit(1)

    def extract_virtual_fs(self):
        """Extract the virtual file system from the tar archive."""
        if not os.path.exists(self.virtual_fs_dir):
            os.mkdir(self.virtual_fs_dir)

        with tarfile.open(self.virtual_fs_path, "r") as tar:
            tar.extractall(self.virtual_fs_dir)

    def log_action(self, action):
        """Log an action with a timestamp."""
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"{timestamp}, {action}"
        if self.log_file_path:
            with open(self.log_file_path, "a") as log_file:
                log_file.write(log_entry + "\n")

    def execute_startup_script(self):
        """Execute commands from the startup script."""
        if self.startup_script_path and os.path.exists(self.startup_script_path):
            with open(self.startup_script_path) as script:
                for line in script:
                    command = line.strip()
                    if command:
                        self.execute_command(command)

    def list_files(self):
        """Simulate the 'ls' command."""
        path = os.path.join(self.virtual_fs_dir, self.current_path.strip("/"))
        try:
            files = os.listdir(path)
            if files:
                print("\n".join(files))
            else:
                print("Пустая директория")
            self.log_action("ls")
        except FileNotFoundError:
            print("Директория не найдена")
            self.log_action("ls (ошибка: директория не найдена)")

    def change_directory(self, path):
        """Simulate the 'cd' command."""
        new_path = os.path.join(self.virtual_fs_dir, self.current_path.strip("/"), path).strip("/")
        if os.path.isdir(new_path):
            self.current_path = os.path.relpath(new_path, self.virtual_fs_dir)
            self.log_action(f"cd {path}")
        else:
            print("Директория не найдена")
            self.log_action(f"cd {path} (ошибка: директория не найдена)")

    def print_users(self):
        """Simulate the 'who' command."""
        print(f"Пользователь: {self.username}")
        self.log_action("who")

    def word_count(self, filename):
        """Simulate the 'wc' command."""
        file_path = os.path.join(self.virtual_fs_dir, self.current_path.strip("/"), filename)
        try:
            with open(file_path, "r") as file:
                lines = file.readlines()
                print(f"{len(lines)} строк, {sum(len(line.split()) for line in lines)} слов")
                self.log_action(f"wc {filename}")
        except FileNotFoundError:
            print("Файл не найден")
            self.log_action(f"wc {filename} (ошибка: файл не найден)")

    def tail_file(self, filename, lines=10):
        """Simulate the 'tail' command."""
        file_path = os.path.join(self.virtual_fs_dir, self.current_path.strip("/"), filename)
        try:
            with open(file_path, "r") as file:
                all_lines = file.readlines()
                print("".join(all_lines[-lines:]))
                self.log_action(f"tail {filename}")
        except FileNotFoundError:
            print("Файл не найден")
            self.log_action(f"tail {filename} (ошибка: файл не найден)")

    def exit_shell(self):
        """Exit the shell emulator."""
        self.log_action("Эмулятор завершен")
        print("Выход из эмулятора.")
        sys.exit(0)

    def execute_command(self, command):
        """Parse and execute commands."""
        self.history.append(command)
        parts = command.split()
        cmd = parts[0]
        args = parts[1:]

        if cmd == "ls":
            self.list_files()
        elif cmd == "cd":
            self.change_directory(args[0]) if args else print("Нужен аргумент для команды cd.")
        elif cmd == "who":
            self.print_users()
        elif cmd == "wc":
            self.word_count(args[0]) if args else print("Нужен аргумент для команды wc.")
        elif cmd == "tail":
            self.tail_file(args[0], int(args[1]) if len(args) > 1 else 10)
        elif cmd == "exit":
            self.exit_shell()
        else:
            print(f"{self.username}: команда не найдена")
            self.log_action(f"{cmd} (неизвестная команда)")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Запуск эмулятора командной строки.")
    parser.add_argument("config", type=str, help="Путь к конфигурационному файлу.")
    args = parser.parse_args()

    emulator = ShellEmulator(args.config)
    emulator.execute_startup_script()

    while True:
        try:
            command = input(f"{emulator.username}@{emulator.computer_name}:{emulator.current_path} $ ")
            emulator.execute_command(command.strip())
        except EOFError:
            emulator.exit_shell()
