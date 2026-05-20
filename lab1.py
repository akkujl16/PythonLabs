# coding: utf-8
import sys
import io
def calculate_delivery_cost_final(order, customer, address):
    if not order or not address:
        return {
            "success": False,
            "cost": 0,
            "message": "Ошибка: Заказ или адрес доставки не указаны"
        }
    
    weight = order.get('weight', 0)
    amount = order.get('amount', 0)
    
    if weight <= 0:
        return {
            "success": False,
            "cost": 0,
            "message": "Ошибка: Вес заказа должен быть положительным числом"
        }
    
    if weight > 50:
        return {
            "success": False,
            "cost": 0,
            "message": "Ошибка: Максимальный вес для доставки - 50 кг"
        }
    
    if amount < 1000:
        return {
            "success": False,
            "cost": 0,
            "message": "Ошибка: Минимальная стоимость заказа для доставки - 1000 рублей"
        }
    
    delivery_type = address.get('delivery_type', 'courier')
    is_remote = address.get('is_remote', False)
    is_vip = customer.get('is_vip', False)
    is_new = customer.get('is_new', False)
    
    if delivery_type == 'pickup':
        cost = 0
    else:
        if is_remote:
            cost = 1000 + (weight * 100)
        else:
            if weight <= 5:
                cost = 300
            elif weight <= 10:
                cost = 500
            else:
                cost = 500 + (weight - 10) * 50
        
        if (not is_remote and amount >= 10000) or (is_vip and amount >= 5000):
            cost = 0
        else:
            if is_new:
                cost = cost * 0.85
            if is_remote:
                cost = cost * 1.2
    
    return {
        "success": True,
        "cost": round(cost, 2),
        "message": f"Стоимость доставки: {round(cost, 2)} рублей"
    }

weight = 5      
amount = 3000   
is_vip = False  
is_new = True   
is_remote = False 
delivery_type = 'courier' 

order = {"weight": weight, "amount": amount}
customer = {"is_vip": is_vip, "is_new": is_new}
address = {
    "city": "Москва",
    "street": "Тверская",
    "delivery_type": delivery_type,
    "is_remote": is_remote
}

result = calculate_delivery_cost_final(order, customer, address)
print(f"\nРезультат: {result['message']}")