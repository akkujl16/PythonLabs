import numpy as np
import matplotlib.pyplot as plt

# Поиск определителя
def determinant_3x3(A):
    a11, a12, a13 = A[0,0], A[0,1], A[0,2]
    a21, a22, a23 = A[1,0], A[1,1], A[1,2]
    a31, a32, a33 = A[2,0], A[2,1], A[2,2]
    
    # Главные диагонали
    main = (a11 * a22 * a33 + 
            a12 * a23 * a31 + 
            a13 * a21 * a32)
    
    # Побочные диагонали
    secondary = (a13 * a22 * a31 + 
                 a11 * a23 * a32 + 
                 a12 * a21 * a33)
    
    return main - secondary

# Загрузка данных из файла
data = []
with open('lab2_data.csv', 'r') as f:
    lines = f.readlines()
    header = lines[0].strip()
    for line in lines[1:]:
        if line.strip():
            x_str, y_str = line.strip().split(';')
            x = int(x_str)
            if y_str != 'NaN':
                y = float(y_str)
            else:
                y = np.nan
            data.append((x, y))

data_array = np.array(data)
x_vals = data_array[:, 0]  # все строки, первый столбец
y_vals = data_array[:, 1]  # все строки, второй столбец

# Исходный график
plt.figure(figsize=(10, 6))
plt.plot(x_vals, y_vals, 'o-', label='Исходные данные (с NaN)', color='gray', alpha=0.7)
plt.title('Исходные данные')
plt.xlabel('x')
plt.ylabel('y')
plt.grid(True)
plt.legend()
plt.show()

# Интерполяции вручную

# Линейная интерполяция по двум точкам (x0,y0) и (x1,y1) для заданного x
def linear_interp(x, x0, y0, x1, y1):
    return y0 + (y1 - y0) * (x - x0) / (x1 - x0)

# Квадратичная интерполяция по трём точкам
# Решение системы методом Крамера (поиск коэффициентов a,b,c: y = a*x^2 + b*x + c)
# Матрица коэффициентов
# | x0^2  x0  1 | |a| = |y0|
# | x1^2  x1  1 | |b| = |y1|
# | x2^2  x2  1 | |c| = |y2|
def quadratic_interp(x, x0, y0, x1, y1, x2, y2):
    # Главная матрица
    A_main = np.array([
        [x0**2, x0, 1],
        [x1**2, x1, 1],
        [x2**2, x2, 1]
    ])
    
    # Матрица для a
    A_a = np.array([
        [y0, x0, 1],
        [y1, x1, 1],
        [y2, x2, 1]
    ])
    
    # Матрица для b
    A_b = np.array([
        [x0**2, y0, 1],
        [x1**2, y1, 1],
        [x2**2, y2, 1]
    ])
    
    # Матрица для c
    A_c = np.array([
        [x0**2, x0, y0],
        [x1**2, x1, y1],
        [x2**2, x2, y2]
    ])
    
    # Вычисление определителей
    det_main = determinant_3x3(A_main)
    det_a = determinant_3x3(A_a)
    det_b = determinant_3x3(A_b)
    det_c = determinant_3x3(A_c)
    
    # Коэффициенты
    a = det_a / det_main
    b = det_b / det_main
    c = det_c / det_main
    
    # Значение в точке x
    return a * x**2 + b * x + c

# Индексы пропущенных значений
nan_indices = []
for i in range(len(y_vals)):
    if np.isnan(y_vals[i]):
        nan_indices.append(i)

# Копии для заполнения
y_linear = y_vals.copy()
y_quadratic = y_vals.copy()

# Заполнение пропусков
for index in nan_indices:
    x_nan_indices = x_vals[index]
    
    # Линейная интерполяция
    # Ближайшие известные точки слева и справа
    left_index = None
    right_index = None
    
    for i in range(index-1, -1, -1):
        if not np.isnan(y_vals[i]):
            left_index = i
            break
    
    for i in range(index+1, len(x_vals)):
        if not np.isnan(y_vals[i]):
            right_index = i
            break
    
    if left_index is not None and right_index is not None:
        y_linear[index] = linear_interp(x_nan_indices, 
                                       x_vals[left_index], y_vals[left_index],
                                       x_vals[right_index], y_vals[right_index])
    
    # Квадратичная интерполяция
    points = []
    
    # Сбор известных точек вокруг пропуска
    for i in range(index-1, -1, -1):
        if not np.isnan(y_vals[i]):
            points.append((x_vals[i], y_vals[i]))
            if len(points) >= 2:
                break
    
    for i in range(index+1, len(x_vals)):
        if not np.isnan(y_vals[i]):
            points.append((x_vals[i], y_vals[i]))
            if len(points) >= 3:
                break
    
    # 3 точки (2 слева + 1 справа или 1 слева + 2 справа)
    if len(points) >= 3:
        p0, p1, p2 = points[0], points[1], points[2]
        y_quadratic[index] = quadratic_interp(x_nan_indices, 
                                             p0[0], p0[1],
                                             p1[0], p1[1],
                                             p2[0], p2[1])
    else:
        # Если недостаточно точек для квадратичной, используется линейная
        y_quadratic[index] = y_linear[index]

# Графики с заполненными данными
plt.figure(figsize=(12, 5))

# График с линейной интерполяцией
plt.subplot(1, 2, 1)
plt.plot(x_vals, y_linear, 'o-', color='blue', label='Линейная интерполяция')
plt.scatter([x_vals[i] for i in nan_indices], [y_linear[i] for i in nan_indices], 
            color='red', s=50, label='Восстановленные точки')
plt.title('Линейная интерполяция')
plt.xlabel('x')
plt.ylabel('y')
plt.grid(True)
plt.legend()

# График с квадратичной интерполяцией
plt.subplot(1, 2, 2)
plt.plot(x_vals, y_quadratic, 'o-', color='green', label='Квадратичная интерполяция')
plt.scatter([x_vals[i] for i in nan_indices], [y_quadratic[i] for i in nan_indices], 
            color='red', s=50, label='Восстановленные точки')
plt.title('Квадратичная интерполяция')
plt.xlabel('x')
plt.ylabel('y')
plt.grid(True)
plt.legend()

plt.tight_layout()
plt.show()

# Восстановленные значения
print("Восстановленные значения (линейная интерполяция):")
for index in nan_indices:
    print(f"  x = {x_vals[index]}, y = {y_linear[index]}")

print("Восстановленные значения (квадратичная интерполяция):")
for index in nan_indices:
    print(f"  x = {x_vals[index]}, y = {y_quadratic[index]}")