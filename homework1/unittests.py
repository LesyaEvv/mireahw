import unittest
import os
import shutil
from unittest.mock import patch, mock_open
from emulator import ShellEmulator  
import tarfile

class TestShellEmulator(unittest.TestCase):

    def setUp(self):
        """Настройка окружения перед каждым тестом."""
        self.config_file = "test_config.csv"
        self.virtual_fs_path = "test_virtual_fs.tar"
        self.log_file_path = "test_log.txt"

        # Создаем тестовый конфигурационный файл
        with open(self.config_file, "w") as config:
            config.write("computer_name,TestComputer\n")
            config.write(f"virtual_fs_path,{self.virtual_fs_path}\n")
            config.write(f"log_file_path,{self.log_file_path}\n")
            config.write("startup_script_path,\n")

        # Создаем тестовую файловую систему
        os.mkdir("test_virtual_fs")
        with open("test_virtual_fs/file1.txt", "w") as file1:
            file1.write("Hello\nWorld\n")
        with tarfile.open(self.virtual_fs_path, "w") as tar:
            tar.add("test_virtual_fs", arcname=".")

        self.emulator = ShellEmulator(self.config_file)

    def tearDown(self):
        """Очистка окружения после каждого теста."""
        if os.path.exists(self.config_file):
            os.remove(self.config_file)
        if os.path.exists(self.virtual_fs_path):
            os.remove(self.virtual_fs_path)
        if os.path.exists(self.log_file_path):
            os.remove(self.log_file_path)
        if os.path.exists("test_virtual_fs"):
            shutil.rmtree("test_virtual_fs")
        if os.path.exists(self.emulator.virtual_fs_dir):
            shutil.rmtree(self.emulator.virtual_fs_dir)

    def test_ls_command(self):
        """Тест команды 'ls'."""
        with patch("builtins.print") as mocked_print:
            self.emulator.list_files()
            mocked_print.assert_called_with("file1.txt")

    def test_cd_command(self):
        """Тест команды 'cd'."""
        self.emulator.change_directory(".")
        self.assertEqual(self.emulator.current_path, ".")

    def test_wc_command(self):
        """Тест команды 'wc'."""
        with patch("builtins.print") as mocked_print:
            self.emulator.word_count("file1.txt")
            mocked_print.assert_called_with("2 строк, 2 слов")

    def test_unknown_command(self):
        """Тест на неизвестную команду."""
        with patch("builtins.print") as mocked_print:
            self.emulator.execute_command("unknown")
            mocked_print.assert_called_with(f"{self.emulator.username}: команда не найдена")

    def test_log_action(self):
        """Тест функции логирования."""
        self.emulator.log_action("test action")
        with open(self.log_file_path, "r") as log_file:
            log_content = log_file.read()
        self.assertIn("test action", log_content)

if __name__ == "__main__":
    unittest.main()
