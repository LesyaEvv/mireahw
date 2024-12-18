import sys
import re
import yaml

# Регулярные выражения для различных элементов конфигурации
comment_pattern = re.compile(r'\*>.*')
name_pattern = re.compile(r'[_A-Z][_a-zA-Z0-9]*')
value_pattern = re.compile(r"'.*?'|[0-9]+|<<.*?>>")
define_pattern = re.compile(r'\(define (\w+) (.*)\)')

# Функция для обработки входного конфигурационного файла
def parse_config_file(file_path):
    constants = {}
    result = {}
    
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    for line in lines:
        line = line.strip()
        
        # Пропуск комментариев
        if comment_pattern.match(line):
            continue
        
        # Обработка объявления константы
        define_match = define_pattern.match(line)
        if define_match:
            name, value = define_match.groups()
            constants[name] = parse_value(value.strip(), constants)
            continue
        
        # Обработка строк, значений и массивов
        parts = line.split('=')
        if len(parts) == 2:
            name = parts[0].strip()
            value = parts[1].strip()
            if name_pattern.match(name):
                result[name] = parse_value(value, constants)
            else:
                print(f"Ошибка: Неверное имя {name}")
                sys.exit(1)
    
    return result

# Функция для обработки значений (числа, строки, массивы)
def parse_value(value, constants):
    # Замена ссылок на константы
    if value.startswith('.[') and value.endswith('].'):
        const_name = value[2:-2]
        return constants.get(const_name, f"Ошибка: Неизвестная константа {const_name}")
    
    # Проверка на число
    if value.isdigit():
        return int(value)
    
    # Проверка на строку
    if value.startswith("'") and value.endswith("'"):
        return value[1:-1]
    
    # Проверка на массив
    if value.startswith('<<') and value.endswith('>>'):
        elements = value[2:-2].split(',')
        return [parse_value(e.strip(), constants) for e in elements]
    
    return value

# Функция для конвертации в YAML
def convert_to_yaml(data):
    return yaml.dump(data, allow_unicode=True)

# Основная функция обработки командной строки
def main():
    if len(sys.argv) != 2:
        print("Использование: py hw3.py <путь_к_файлу>")
        sys.exit(1)
    
    file_path = sys.argv[1]
    try:
        parsed_data = parse_config_file(file_path)
        yaml_data = convert_to_yaml(parsed_data)
        print(yaml_data)
    except Exception as e:
        print(f"Ошибка: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
