# Установка
1. Установка программы и переход в директорию
   ```bash
   git clone <URL репозитория>
   cd <директория проекта>
   ```
2. Создайте и активируйте виртуальное окружение:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # Для Linux/Mac
   venv\Scripts\activate     # Для Windows
   ```
3. Установите необходимые зависимости :
   ```bash
   Зависимости не требуются
   ```

# Запуск скрипта

Скрипт принимает текст конфигурационного файла через файл и выводит yaml в стандартный вывод.

```bash
py hw3.py input.txt
```

# Вывод

```bash
Входные данные:

*> Это комментарий
(define PI 3.14159)
(define COLORS << "red", "green", "blue" >>)
MyValue = .[PI].
Name = 'Konfig'
Numbers = << 1, 2, 3, 4 >>
```

```bash
Вывод: 

MyValue: '3.14159'
Name: Konfig
Numbers:
- 1
- 2
- 3
- 4
```