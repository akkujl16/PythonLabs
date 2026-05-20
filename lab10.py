import numpy as np
import matplotlib.pyplot as plt

# ЗАГРУЗКА ДАННЫХ
print("1. Загрузка данных")
filename = "data.csv"

try:
    data = np.loadtxt(filename, delimiter=';', skiprows=1)
    x = data[:, 0]  # первый столбец - аргумент (время)
    y = data[:, 1]  # второй столбец - исходный ряд
    print(f"Файл '{filename}' загружен.")
except FileNotFoundError:
    print(f"ОШИБКА: файл '{filename}' не найден.")
    exit()

# ОСНОВНЫЕ ПАРАМЕТРЫ
N = len(y)  # длина временного ряда
print(f"2. Длина наблюдений N = {N}")

# ГРАФИК ИСХОДНОГО ПРОЦЕССА
plt.figure(figsize=(12, 7))
plt.plot(x, y, 'b-', linewidth=1, label='Исходные данные y(x)', alpha=0.7)
plt.title('Исходный временной ряд')
plt.xlabel('x')
plt.ylabel('y')
plt.grid(True, linestyle=':', alpha=0.6)
plt.legend()
plt.show()

# СКОЛЬЗЯЩЕЕ СРЕДНЕЕ
print("3. Метод скользящего среднего")
def moving_average(data, L):
    smoothed = np.zeros_like(data, dtype=float)
    n = len(data)
    
    for i in range(n):
        left = max(0, i - L)
        right = min(n, i + L + 1)
        smoothed[i] = np.mean(data[left:right])
    return smoothed

# Сглаживание с разными L
L_values = [3, 5, 10]  # полуплечи (по заданию L=3, а также больше)
z_dict = {}  # словарь для хранения сглаженных рядов

for L in L_values:
    z = moving_average(y, L)
    z_dict[L] = z
    print(f"L = {L:2d} окно = {2*L+1:2d} точек, сглаживание выполнено")

# Все сглаженные ряды на одном графике с исходным
plt.figure(figsize=(14, 8))
plt.plot(x, y, 'b-', linewidth=1, label='Исходные данные', alpha=0.5)

colors = ['r', 'g', 'm']
for idx, L in enumerate(L_values):
    plt.plot(x, z_dict[L], colors[idx], linewidth=1.5, 
             label=f'Скользящее среднее, L={L} (окно {2*L+1})')

plt.title('Сглаживание методом скользящего среднего при разных L')
plt.xlabel('x')
plt.ylabel('y')
plt.grid(True, linestyle=':', alpha=0.6)
plt.legend()
plt.show()

# ЭКСПОНЕНЦИАЛЬНОЕ СГЛАЖИВАНИЕ
print("4. Метод экспоненциального сглаживания")

def exponential_smoothing(data, alpha, beta=None):
    n = len(data)
    smoothed = np.zeros(n)
    smoothed[0] = data[0]
    
    if beta is None:
        # Простое экспоненциальное сглаживание
        for t in range(1, n):
            smoothed[t] = alpha * data[t] + (1 - alpha) * smoothed[t-1]
    else:
        # Двойное экспоненциальное сглаживание
        trend = np.zeros(n)
        trend[0] = data[1] - data[0] if n > 1 else 0
        
        for t in range(1, n):
            if t == 1:
                smoothed[t] = alpha * data[t] + (1 - alpha) * (smoothed[t-1] + trend[t-1])
            else:
                smoothed[t] = alpha * data[t] + (1 - alpha) * (smoothed[t-1] + trend[t-1])
            trend[t] = beta * (smoothed[t] - smoothed[t-1]) + (1 - beta) * trend[t-1]
    
    return smoothed

# Параметры сглаживания (α и β)
alpha_values = [0.1, 0.3, 0.7]  # разные степени сглаживания
# Для двойного сглаживания фиксируется alpha и beta
alpha_double = 0.3
beta_double = 0.2

print("Простое экспоненциальное сглаживание (только α):")
s_exp_simple = {}
for alpha in alpha_values:
    s = exponential_smoothing(y, alpha)
    s_exp_simple[alpha] = s
    print(f"α = {alpha} выполнено")

print("Двойное экспоненциальное сглаживание (α и β):")
s_exp_double = exponential_smoothing(y, alpha_double, beta_double)
print(f"α = {alpha_double}, β = {beta_double} выполнено")

# ПОСТРОЕНИЕ ГРАФИКОВ ЭКСПОНЕНЦИАЛЬНОГО СГЛАЖИВАНИЯ

# График для простого экспоненциального сглаживания
plt.figure(figsize=(14, 8))
plt.plot(x, y, 'b-', linewidth=1, label='Исходные данные', alpha=0.5)

colors_simple = ['orange', 'purple', 'brown']
for idx, alpha in enumerate(alpha_values):
    plt.plot(x, s_exp_simple[alpha], colors_simple[idx], linewidth=1.5,
             label=f'Простое эксп. сглаживание, α={alpha}')

plt.title('Простое экспоненциальное сглаживание при разных α')
plt.xlabel('x')
plt.ylabel('y')
plt.grid(True, linestyle=':', alpha=0.6)
plt.legend()
plt.show()

# График для двойного экспоненциального сглаживания
plt.figure(figsize=(14, 8))
plt.plot(x, y, 'b-', linewidth=1, label='Исходные данные', alpha=0.5)
plt.plot(x, s_exp_double, 'r-', linewidth=1.8, 
         label=f'Двойное эксп. сглаживание, α={alpha_double}, β={beta_double}')

plt.title('Двойное экспоненциальное сглаживание')
plt.xlabel('x')
plt.ylabel('y')
plt.grid(True, linestyle=':', alpha=0.6)
plt.legend()
plt.show()

# ИТОГОВЫЙ СВОДНЫЙ ГРАФИК
# На одном графике: исходные, лучшее скользящее среднее, лучшее эксп. сглаживание

plt.figure(figsize=(14, 8))
plt.plot(x, y, 'b-', linewidth=1, label='Исходные данные', alpha=0.4)

# L=5 как норм скользящее среднее
plt.plot(x, z_dict[5], 'g-', linewidth=1.5, label='Скользящее среднее, L=5 (окно 11)')

# α=0.3 как норм экспоненциальное сглаживание
plt.plot(x, s_exp_simple[0.3], 'r-', linewidth=1.5, label='Эксп. сглаживание, α=0.3')

# Двойное сглаживание
plt.plot(x, s_exp_double, 'm-', linewidth=1.5, label=f'Двойное эксп., α={alpha_double}, β={beta_double}')

plt.title('Сравнение методов сглаживания')
plt.xlabel('x')
plt.ylabel('y')
plt.grid(True, linestyle=':', alpha=0.6)
plt.legend()
plt.show()