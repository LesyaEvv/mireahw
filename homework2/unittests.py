import unittest
from unittest.mock import patch, MagicMock
import os
import subprocess
from datetime import datetime

# Импортируем функции для тестирования
from hw2 import parse_args, get_commits, get_commit_files, build_plantuml_graph, save_plantuml_diagram


class TestGitVisualizer(unittest.TestCase):

    @patch("argparse.ArgumentParser.parse_args")
    def test_parse_args(self, mock_parse_args):
        mock_parse_args.return_value = MagicMock(
            visualizer="C:\\Users\\user\\Desktop\\Otcheti\\var7\\homework2\\path\\to\\plantuml.jar", 
            repo="C:\\Users\\user\\Desktop\\Otcheti\\var7\\homework2\\path\\to\\repo", 
            output="C:\\Users\\user\\Desktop\\Otcheti\\var7\\homework2\\path\\to\\output.png", 
            date="2024-12-08"
        )
        
        args = parse_args()
        self.assertEqual(args.visualizer, "C:\\Users\\user\\Desktop\\Otcheti\\var7\\homework2\\path\\to\\plantuml.jar")
        self.assertEqual(args.repo, "C:\\Users\\user\\Desktop\\Otcheti\\var7\\homework2\\path\\to\\repo")
        self.assertEqual(args.output, "C:\\Users\\user\\Desktop\\Otcheti\\var7\\homework2\\path\\to\\output.png")
        self.assertEqual(args.date, "2024-12-08")

    @patch("subprocess.run")
    @patch("os.chdir")  # Мокируем os.chdir, чтобы избежать реального перехода в директорию
    def test_get_commits(self, mock_chdir, mock_run):
        mock_run.return_value = MagicMock(stdout="commit1\ncommit2\n")
        
        commits = get_commits("C:\\Users\\user\\Desktop\\Otcheti\\var7\\homework2\\path\\to\\repo", "2024-12-08")
        self.assertEqual(commits, ["commit1", "commit2"])

    @patch("subprocess.run")
    @patch("os.chdir")  # Мокируем os.chdir
    def test_get_commit_files(self, mock_chdir, mock_run):
        mock_run.return_value = MagicMock(stdout="file1.py\nfile2.py\n")
        
        files = get_commit_files("C:\\Users\\user\\Desktop\\Otcheti\\var7\\homework2\\path\\to\\repo", "commit1")
        self.assertEqual(files, ["file1.py", "file2.py"])

    def build_plantuml_graph(repo_path, commits):
        graph_lines = [
            "@startuml",
            "    left to right direction",
            "    skinparam ArrowColor Black"
        ]
        nodes = {}
        
        for commit in commits:
            files = get_commit_files(repo_path, commit)
            node_label = "\\n".join(files) if files else "No changes"
            nodes[commit] = f'    "{commit}" : {node_label}'
        
        for i in range(len(commits) - 1):
            graph_lines.append(f'    {commits[i]} --> {commits[i+1]}')
        
        graph_lines.extend(nodes.values())
        graph_lines.append("    @enduml")
        
        return "\n".join(graph_lines)




    @patch("subprocess.run")
    @patch("os.rename")
    @patch("os.path.exists")
    def test_save_plantuml_diagram(self, mock_exists, mock_rename, mock_run):
        # Настроим mock-ы для subprocess и файловой системы
        mock_exists.return_value = True
        mock_run.return_value = MagicMock(returncode=0, stdout="", stderr="")
        
        # Запускаем функцию сохранения диаграммы
        save_plantuml_diagram("C:\\Users\\user\\Desktop\\Otcheti\\var7\\homework2\\path\\to\\plantuml.jar", "@startuml\n@enduml", "C:\\Users\\user\\Desktop\\Otcheti\\var7\\homework2\\path\\to\\output.png")
        
        mock_run.assert_called_with(
            ["java", "-jar", "C:\\Users\\user\\Desktop\\Otcheti\\var7\\homework2\\path\\to\\plantuml.jar", "temp_graph.puml", "-o", "C:\\Users\\user\\Desktop\\Otcheti\\var7\\homework2\\path\\to"],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
        )
        
        # Изменим путь для сравнения с экранированными обратными слешами
        expected_temp_graph_path = "C:\\Users\\user\\Desktop\\Otcheti\\var7\\homework2\\path\\to\\temp_graph.png"
        expected_output_path = "C:\\Users\\user\\Desktop\\Otcheti\\var7\\homework2\\path\\to\\output.png"
        mock_rename.assert_called_with(expected_temp_graph_path, expected_output_path)

if __name__ == "__main__":
    unittest.main()
