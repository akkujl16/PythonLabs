import os
from typing import List, Union, Dict, Any

def convert_value(value: str) -> Union[str, int, float]:
    
    # Проверка на пустую строку
    if not value or value.strip() == '':
        return ''
    
    # Удаление пробелов в начале и конце
    value = value.strip()
    
    # Проверка на int
    # Строка может начинаться с минуса и состоять только из цифр
    if value.startswith('-'):
        # Проверка, что после минуса только цифры
        if value[1:].isdigit():
            return int(value)
    elif value.isdigit():
        return int(value)
    
    # Проверка на float
    # Может содержать одну точку и состоять из цифр с учетом минуса
    if value.count('.') == 1:
        # Разделение на целую и дробную части
        if value.startswith('-'):
            parts = value[1:].split('.')
            # Проверка, что обе части состоят из цифр
            if len(parts) == 2 and parts[0].isdigit() and parts[1].isdigit():
                return float(value)
        else:
            parts = value.split('.')
            if len(parts) == 2 and parts[0].isdigit() and parts[1].isdigit():
                return float(value)
    
    # Если не удалось преобразовать в int или float, возвращение строки
    return value


def read_table_file(filepath: str, delimiter: str = ',', has_header: bool = True) -> Dict[str, Any]:
 
    result = {
        'header': [],
        'data': [],
        'types': []
    }
    
    # Проверка существование файла
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Файл {filepath} не найден")
    
    # Чтение файла
    with open(filepath, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    
    if not lines:
        return result
    
    # Удаление пустых строк
    lines = [line.strip() for line in lines if line.strip()]
    
    if not lines:
        return result
    
    # Определение, нужно ли удалять кавычки
    def clean_value(val: str) -> str:
        val = val.strip()
        if val.startswith('"') and val.endswith('"'):
            val = val[1:-1]
        return val
    
    # Обработка первой строки
    first_line = lines[0]
    if has_header:
        # Разбиваем заголовок
        headers = [clean_value(col) for col in first_line.split(delimiter)]
        result['header'] = headers
        start_index = 1
    else:
        # Если заголовка нет, создаybt автоматически[ заголовкjd
        first_row = [clean_value(col) for col in first_line.split(delimiter)]
        result['header'] = [f"Column_{i+1}" for i in range(len(first_row))]
        start_index = 0
    
    # Определение типов по первой строке данных
    if start_index < len(lines):
        first_data_row = [clean_value(col) for col in lines[start_index].split(delimiter)]
        types = []
        for value in first_data_row:
            converted = convert_value(value)
            if type(converted) == int:
                types.append(int)
            elif type(converted) == float:
                types.append(float)
            else:
                types.append(str)
        result['types'] = types
    
    # Обработка всех строк данных
    for line in lines[start_index:]:
        # Разбиение строки на столбцы
        values = [clean_value(col) for col in line.split(delimiter)]
        
        # Преобразование значений согласно определенным типам
        converted_row = []
        for i in range(len(values)):
            value = values[i]
            #Проверка, есть ли тип для этого столбца
            if i < len(result['types']):
                # Преобразуем согласно типу
                converted = convert_value(value)
            # Приведение к нужному типу, если необходимо
            if result['types'][i] == int and type(converted) == float:
                converted = int(converted)
            elif result['types'][i] == float and type(converted) == int:
                converted = float(converted)
                converted_row.append(converted)
            else:
                # Если столбцов больше, чем типов, просто преобразование
                converted_row.append(convert_value(value))

        result['data'].append(converted_row)
    
    return result


# Пример использования для всех файлов
def demonstrate_reading():
    
    files = [
        ('csv_20260206_08a514.txt', ',', True),
        ('tsv_20260206_ecdd0d.txt', '\t', True),
        ('txt_20260206_2b2f78.txt', '|', True),
        ('txt_20260206_268046.txt', ';', False)
    ]
    
    for filename, delimiter, has_header in files:
        print(f"Файл: {filename}")
        print(f"Разделитель: '{delimiter}'")
        print(f"Наличие заголовка: {has_header}")
        
        try:
            data = read_table_file(filename, delimiter, has_header)
            
            print(f"\nЗаголовки: {data['header']}")
            print(f"Типы столбцов: {[t.__name__ for t in data['types']]}")
            print(f"\nДанные:")
            for row in data['data']:
                print(f"  {row}")
                
        except Exception as e:
            print(f"Ошибка при чтении файла: {e}")

demonstrate_reading()
