import os
import subprocess
import argparse
from datetime import datetime

def parse_args():
    parser = argparse.ArgumentParser(description="Визуализатор графа зависимостей для git-репозитория.")
    parser.add_argument("--visualizer", required=True, help="Путь к программе для визуализации графов (PlantUML jar).")
    parser.add_argument("--repo", required=True, help="Путь к анализируемому git-репозиторию.")
    parser.add_argument("--output", required=True, help="Путь к файлу для сохранения изображения графа зависимостей.")
    parser.add_argument("--date", required=True, help="Дата коммитов (в формате YYYY-MM-DD).")
    return parser.parse_args()

def get_commits(repo_path, cutoff_date):
    os.chdir(repo_path)
    result = subprocess.run(
        ["git", "log", "--since", cutoff_date, "--pretty=format:%H"],
        stdout=subprocess.PIPE, text=True
    )
    return result.stdout.splitlines()

def get_commit_files(repo_path, commit_hash):
    os.chdir(repo_path)
    result = subprocess.run(
        ["git", "show", "--name-only", "--pretty=format:", commit_hash],
        stdout=subprocess.PIPE, text=True
    )
    return result.stdout.splitlines()

def build_plantuml_graph(repo_path, commits):
    graph_lines = ["@startuml", "left to right direction", "skinparam ArrowColor Black"]
    nodes = {}
    
    for commit in commits:
        files = get_commit_files(repo_path, commit)
        node_label = "\\n".join(files) if files else "No changes"
        nodes[commit] = f'"{commit}" : {node_label}'
    
    for i in range(len(commits) - 1):
        graph_lines.append(f'{commits[i]} --> {commits[i+1]}')
    
    graph_lines.extend(nodes.values())
    graph_lines.append("@enduml")
    return "\n".join(graph_lines)

def save_plantuml_diagram(plantuml_path, plantuml_content, output_path):
    temp_puml_file = "temp_graph.puml"
    try:
        # Записываем данные PlantUML во временный файл
        with open(temp_puml_file, "w") as f:
            f.write(plantuml_content)

        # Выполняем генерацию PNG
        result = subprocess.run(
            ["java", "-jar", plantuml_path, temp_puml_file, "-o", os.path.dirname(output_path)],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
        )

        # Проверяем, завершилась ли команда успешно
        if result.returncode != 0:
            print("Ошибка при выполнении PlantUML:")
            print(result.stderr)
            return

        # Проверяем, создался ли временный файл
        temp_output_file = os.path.join(os.path.dirname(output_path), "temp_graph.png")
        if not os.path.exists(temp_output_file):
            print("PlantUML не создал файл изображения.")
            return

        # Перемещаем файл в выходной путь
        os.rename(temp_output_file, output_path)
        print(f"Граф успешно сохранён в {output_path}")
    finally:
        # Удаляем временные файлы
        if os.path.exists(temp_puml_file):
            os.remove(temp_puml_file)


def main():
    args = parse_args()
    
    cutoff_date = args.date
    try:
        datetime.strptime(cutoff_date, "%Y-%m-%d")
    except ValueError:
        print("Некорректный формат даты. Используйте формат YYYY-MM-DD.")
        return
    
    commits = get_commits(args.repo, cutoff_date)
    if not commits:
        print("Нет подходящих коммитов для заданной даты.")
        return
    
    plantuml_content = build_plantuml_graph(args.repo, commits)
    save_plantuml_diagram(args.visualizer, plantuml_content, args.output)
    print(f"Граф зависимостей успешно сохранён в файл: {args.output}")

if __name__ == "__main__":
    main()
