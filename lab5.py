import time
from datetime import datetime
from functools import wraps

def log_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Время начала выполнения
        start_time = time.time()
        start_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Запись о вызове функции
        with open('log.txt', 'a', encoding='utf-8') as log_file:
            log_file.write(f"[{start_datetime}] Функция '{func.__name__}' вызвана с аргументами: {args}\n")
        
        # Вызов исходной функции
        result = func(*args, **kwargs)
        
        # Время завершения и выполнения
        end_time = time.time()
        end_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        execution_time = end_time - start_time
        
        # Запись о завершении функции
        with open('log.txt', 'a', encoding='utf-8') as log_file:
            log_file.write(f"[{end_datetime}] Функция '{func.__name__}' завершена. Время выполнения: {execution_time:.4f} сек.\n")
        
        return result
    return wrapper

@log_decorator
def calculate(a, b, operation):
    if operation == '+':
        return a + b
    elif operation == '-':
        return a - b
    elif operation == '*':
        return a * b
    elif operation == '/':
        return a / b
    else:
        raise ValueError("Неподдерживаемая операция")

print(calculate(10, 5, '+'))
print(calculate(10, 5, '-'))
print(calculate(10, 5, '*'))
print(calculate(10, 5, '/'))
