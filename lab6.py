import numpy as np
import matplotlib.pyplot as plt

data = np.loadtxt('company_sales_data.csv', delimiter=',', skiprows=1)

# Извлечение столбцов (все строки, нужные колонки)
month_number = data[:, 0]
facecream = data[:, 1]
facewash = data[:, 2]
toothpaste = data[:, 3]
bathingsoap = data[:, 4]
shampoo = data[:, 5]
moisturizer = data[:, 6]
total_units = data[:, 7]
total_profit = data[:, 8]

# ЗАДАНИЕ 1 
print("Задание 1: Линейный график общей прибыли")

plt.figure(figsize=(8, 5))
plt.plot(month_number, total_profit)
plt.xlabel('Номер месяца')
plt.ylabel('Общая прибыль')
plt.title('Общая прибыль по месяцам')
plt.grid(True, linestyle='--', alpha=0.7)
plt.show()

# ЗАДАНИЕ 2 
print("Задание 2: Линейный график с настройками стилей")

plt.figure(figsize=(8, 5))
plt.plot(month_number, total_units, 
         linestyle='--', 
         color='red', 
         marker='o', 
         markerfacecolor='black', 
         linewidth=3,
         label='Общее количество единиц')
plt.xlabel('Номер месяца')
plt.ylabel('Количество проданных единиц')
plt.title('Общее количество проданных единиц за последний год')
plt.legend(loc='lower right')
plt.grid(True, linestyle='--', alpha=0.7)
plt.show()

# ЗАДАНИЕ 3
print("Задание 3: Графики для каждого продукта")

# 3.1 Все продукты на одном графике
plt.figure(figsize=(10, 6))
plt.plot(month_number, facecream, label='Face Cream', marker='o')
plt.plot(month_number, facewash, label='Face Wash', marker='o')
plt.plot(month_number, toothpaste, label='Toothpaste', marker='o')
plt.plot(month_number, bathingsoap, label='Bathing Soap', marker='o')
plt.plot(month_number, shampoo, label='Shampoo', marker='o')
plt.plot(month_number, moisturizer, label='Moisturizer', marker='o')
plt.xlabel('Номер месяца')
plt.ylabel('Количество проданных единиц')
plt.title('Продажи всех продуктов по месяцам')
plt.legend(loc='upper left')
plt.grid(True, linestyle='--', alpha=0.7)
plt.show()

# 3.2 Каждый продукт на отдельном графике
fig, axes = plt.subplots(2, 3, figsize=(15, 10))

# Создание списков
products_list = [facecream, facewash, toothpaste, bathingsoap, shampoo, moisturizer]
names_list = ['Face Cream', 'Face Wash', 'Toothpaste', 'Bathing Soap', 'Shampoo', 'Moisturizer']

i = 0
for ax in axes.flat:
    ax.plot(month_number, products_list[i], marker='o', linewidth=2)
    ax.set_xlabel('Номер месяца')
    ax.set_ylabel('Количество продаж')
    ax.set_title(names_list[i])
    ax.grid(True, linestyle='--', alpha=0.7)
    i += 1

plt.tight_layout()
plt.show()

# ЗАДАНИЕ 4
print("Задание 4: Точечный график для зубной пасты")

plt.figure(figsize=(8, 5))
plt.scatter(month_number, toothpaste, color='blue', marker='o', s=100)
plt.xlabel('Номер месяца')
plt.ylabel('Количество проданных единиц')
plt.title('Продажи зубной пасты по месяцам')
plt.grid(True, linestyle='--', linewidth=0.5)
plt.show()

# ЗАДАНИЕ 5 
print("Задание 5: Столбчатая диаграмма для крема для лица и пенки для умывания")

plt.figure(figsize=(10, 6))

# Столбцы (смещение на 0.2 влево и вправо)
plt.bar(month_number - 0.2, facecream, 0.4, color='lightblue', label='Face Cream')
plt.bar(month_number + 0.2, facewash, 0.4, color='orange', label='Face Wash')

plt.xticks(month_number)
plt.xlabel('Номер месяца')
plt.ylabel('Количество продаж')
plt.title('Продажи крема для лица и пенки для умывания')
plt.legend(loc='upper left')
plt.grid(True, linestyle='--', alpha=0.7)

plt.show()

# ЗАДАНИЕ 6
print("Задание 6: Круговая диаграмма продаж за год")

# Сумма продаж за год по каждому продукту
total_sales = np.array([
    np.sum(facecream),
    np.sum(facewash),
    np.sum(toothpaste),
    np.sum(bathingsoap),
    np.sum(shampoo),
    np.sum(moisturizer)
])
product_names = ['Face Cream', 'Face Wash', 'Toothpaste', 'Bathing Soap', 'Shampoo', 'Moisturizer']
colors = ['gold', 'lightcoral', 'lightskyblue', 'lightgreen', 'orange', 'pink']

plt.figure(figsize=(8, 8))
plt.pie(total_sales, labels=product_names, autopct='%1.1f%%', colors=colors, startangle=90)
plt.title('Общие продажи продуктов за год')
plt.axis('equal')
plt.show()

# ЗАДАНИЕ 7
print("Задание 7: Слоеная диаграмма")

plt.figure(figsize=(10, 6))
plt.stackplot(month_number, 
              facecream, facewash, toothpaste, bathingsoap, shampoo, moisturizer,
              labels=['Face Cream', 'Face Wash', 'Toothpaste', 'Bathing Soap', 'Shampoo', 'Moisturizer'],
              colors=['lightblue', 'lightcoral', 'lightgreen', 'orange', 'pink', 'purple'],
              alpha=0.8)
plt.xlabel('Номер месяца')
plt.ylabel('Количество проданных единиц')
plt.title('Структура продаж всех продуктов')
plt.legend(loc='upper left')
plt.grid(True, linestyle='--', alpha=0.3)
plt.show()

# ЗАДАНИЕ 8 
print("Задание 8: Заготовка для расположения графиков")


plt.figure(figsize=(10, 6))


plt.subplot(2, 1, 1)
plt.title("Верхний график")


plt.subplot(2, 3, 4)
plt.title("Внизу 1")


plt.subplot(2, 3, 5)
plt.title("Внизу 2")


plt.subplot(2, 3, 6)
plt.title("Внизу 3")

plt.tight_layout()
plt.show()