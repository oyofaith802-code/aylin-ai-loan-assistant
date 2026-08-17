from persistent_conversation import process_persistent_message
from application_manager import get_current_application


phone = "+996000000000"


print("\nMESSAGE 1")
result1 = process_persistent_message(
    phone=phone,
    message="У меня Toyota Camry 2021 года, хочу получить 500000 сом"
)

print(result1)


print("\nMESSAGE 2")
result2 = process_persistent_message(
    phone=phone,
    message="Примерная стоимость автомобиля 1500000 сом"
)

print(result2)


print("\nDATABASE CHECK")

customer = get_current_application(phone)


print(customer)

if customer:
    print("Car:", customer.car_model)
    print("Year:", customer.car_year)
    print("Value:", customer.car_value)
    print("Loan:", customer.loan_amount)