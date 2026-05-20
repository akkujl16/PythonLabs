from functools import wraps

def cache_decorator(func):
    cache = {}
    
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Ключ из аргументов
        key = (args, tuple(sorted(kwargs.items())))
        
        # ПроверКА, есть ли результат в кэше
        if key in cache:
            print(f"Возвращение закэшированого результат для {func.__name__}{args}")
            return cache[key]
        
        # Вычисление результата и сохранение в кэш
        print(f"Вычисление {func.__name__}{args} ")
        result = func(*args, **kwargs)
        cache[key] = result
        return result
    
    return wrapper

@cache_decorator
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

print("Первый вызов fibonacci(10):")
result1 = fibonacci(10)
print(f"Результат: {result1}\n")

print("Второй вызов fibonacci(10) должен вернуться из кэша:")
result2 = fibonacci(10)
print(f"Результат: {result2}\n")
