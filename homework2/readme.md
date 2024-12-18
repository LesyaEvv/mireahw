# 1. Клонирование репозитория

Склонируйте репозиторий с исходным кодом и тестами:

```
git clone <URL репозитория>
cd <директория проекта>
```

# 2. Установка зависимостей при запуске

```
pip install subprocess

```

# Создайте виртуальное окружение

```bash
# Активируйте виртуальное окружение
python -m venv venv
# Для Windows:
venv\Scripts\activate
# Для MacOS/Linux:
source venv/bin/activate
```


# 3. Структура проекта
Проект содержит следующие файлы и директории:
```bash
unittests.py              # файл для тестирования
hw2.py                  # файл с программой
plantuml.jar           # plantuml
output.png             # файл с выводом программы 
```

# 4. Запуск проекта
```bash
py hw2.py --visualizer C:\Users\user\Desktop\Otcheti\var7\homework2\plantuml.jar --repo C:\Users\user\Desktop\TestRepHw --output C:\Users\user\Desktop\Otcheti\var7\homework2\output.png --date 2024-01-01     

# py hw2.py --visualizer <путь к визуализатору> --repo <путь к репозиторию> --output <путь к выходному png файлу> --date <дата коммитов>
```


# 5. Тестирование с моим репозитеорием 
Вывод программы
```

```



