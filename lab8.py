import numpy as np
import sympy as sp

# Задание функции и отрезка
x = sp.Symbol('x')
func = -x**2 + 5         
a, b = 0, 2

# Аналитическое решение
analyt_integ = sp.integrate(func, (x, a, b))
analyt_integ_val = float(analyt_integ)

# Численные методы
def f(x_val):
    return -x_val**2 + 5

def rectangle_method(f, a, b, n, mode='left'):
    h = (b - a) / n
    if mode == 'left':
        x_vals = np.linspace(a, b - h, n)
    elif mode == 'right':
        x_vals = np.linspace(a + h, b, n)
    elif mode == 'mid':
        x_vals = np.linspace(a + h/2, b - h/2, n)
    else:
        raise ValueError("неверный метод прямоугольников")
    return h * np.sum(f(x_vals))

def trapezoid_method(f, a, b, n):
    h = (b - a) / n
    x_vals = np.linspace(a, b, n+1)
    y_vals = f(x_vals)
    return h * (0.5 * y_vals[0] + np.sum(y_vals[1:-1]) + 0.5 * y_vals[-1])

def simpson_method(f, a, b, n):
    #n – чётное количество разбиений
    if n % 2 != 0:
        raise ValueError("Для метода Симпсона n должно быть чётным")
    h = (b - a) / n
    x_vals = np.linspace(a, b, n+1)
    y_vals = f(x_vals)
    s = y_vals[0] + y_vals[-1]
    s += 4 * np.sum(y_vals[1:-1:2])   # нечётные индексы
    s += 2 * np.sum(y_vals[2:-2:2])   # чётные индексы кроме первого и последнего
    return (h / 3) * s

# Исследование точности
def print_results_simple(n, analyt, rect_left, rect_right, trapez, simpson):
    print(f"Разбиение на {n} частей")
    print(f"Аналитически:                 {analyt:.10f}")
    print(f"Прямоугольники (левые):       {rect_left:.10f}")
    print(f"Прямоугольники (правые):      {rect_right:.10f}")
    print(f"Трапеций:                     {trapez:.10f}")
    print(f"Симпсона:                     {simpson:.10f}")

# РасчётЫ для разных n
n_values = [4, 8, 16, 32]
print(f"Аналитическое значение интеграла: {analyt_integ_val}\n")

for n in n_values:
    rect_left = rectangle_method(f, a, b, n, 'left')
    rect_right = rectangle_method(f, a, b, n, 'right')
    trap = trapezoid_method(f, a, b, n)
    simp = simpson_method(f, a, b, n)
    
    print_results_simple(n, analyt_integ_val, rect_left, rect_right, trap, simp)

# Что бы увеличить точность можно: увеличить количество отрезков разбиения n, использовать методы более высокого порядка точности.