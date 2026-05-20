# Задание 1. Банкомат
print("Задание 1. Банкомат")

while True:
    try:
        amount = input("Введите сумму: ")
        amount = int(amount)
        assert amount > 0, "Сумма должна быть положительной"
        assert amount % 100 == 0, "Сумма должна быть кратна 100"
        print(f"Выдано {amount} руб.")
        break
    except ValueError:
        print("Ошибка: Введите числовое значение")
    except AssertionError as e:
        print(f"Ошибка: {e}")
print("\n")

# Задание 2. Калькулятор возраста
print("Задание 2. Калькулятор возраста")

try:
    current_year = input("Введите текущий год: ")
    birth_year = input("Введите год рождения: ")
    
    current_year = int(current_year)
    birth_year = int(birth_year)
    
    assert birth_year <= current_year, "Год рождения не может быть больше текущего года"
    
    age = current_year - birth_year
    assert 0 <= age <= 120, f"Возраст {age} лет находится вне допустимого диапазона 0-120"
    
    print(f"Ваш возраст: {age} лет")
    
except ValueError:
    print("Ошибка: Пожалуйста, введите числовые значения")
except AssertionError as e:
    print(f"Ошибка: {e}")
print("\n")

# Задание 3. Чтение конфигурационного файла
print("Задание 3. Чтение конфигурационного файла")

filename = "settings.txt"

try:
    with open(filename, 'r') as file:
        content = file.read().strip()
        volume = int(content)
    
    try:
        assert 0 <= volume <= 100, "Значение вне диапазона"
    except AssertionError:
        if volume < 0:
            volume = 0
        elif volume > 100:
            volume = 100
        print(f"Значение было скорректировано до {volume}")
    
except FileNotFoundError:
    print(f"Файл {filename} не найден. Создается с значением по умолчанию (50)")
    volume = 50
    with open(filename, 'w') as file:
        file.write(str(volume))
except ValueError:
    print("Ошибка: В файле не число. Устанавливается значение по умолчанию (50)")
    volume = 50
    with open(filename, 'w') as file:
        file.write(str(volume))

print(f"Уровень громкости установлен: {volume}")
print("\n")

# Задание 4. Регистрация пользователя
print("Задание 4. Регистрация пользователя")

login = input("Введите логин: ")
password = input("Введите пароль: ")

try:
    assert len(password) >= 8, "Пароль должен содержать не менее 8 символов"
    assert any(c.isdigit() for c in password), "Пароль должен содержать хотя бы одну цифру"
    assert any(c.isupper() for c in password), "Пароль должен содержать хотя бы одну заглавную букву"
    print("Регистрация успешна")
    
except AssertionError as e:
    print(f"Ошибка регистрации: {e}")
print("\n")

# Задание 5. Загрузка данных из интернета
print("Задание 5. Загрузка данных из интернета")

def get_user_data(user_id):
    import random
    error_type = random.choice(['connection', 'permission', 'value', 'success', 'no_name'])
    
    if error_type == 'connection':
        raise ConnectionError("Нет соединения с сервером")
    elif error_type == 'permission':
        raise PermissionError("Доступ запрещен")
    elif error_type == 'value':
        raise ValueError("Неверный формат ID")
    elif error_type == 'no_name':
        return {"id": user_id, "age": 25}  # Нет ключа 'name'
    else:
        return {"id": user_id, "name": "Иван", "age": 25}

# Основной код
try:
    user_id = input("Введите ID пользователя: ")
    
    try:
        user_id = int(user_id)
    except ValueError:
        raise ValueError("ID должен быть числом")
    
    result = get_user_data(user_id)
    
    # Проверка наличия ключа 'name'
    assert 'name' in result, "В полученных данных отсутствует поле 'name'"
    print(f"Данные пользователя получены: {result}")
    
except ConnectionError:
    print("Проверьте интернет")
except PermissionError:
    print("Нет прав доступа")
except ValueError as e:
    print(f"Ошибка: {e}")
except AssertionError as e:
    print(f"Ошибка в данных: {e}")

print("\n")