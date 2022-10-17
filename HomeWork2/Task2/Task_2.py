import os
import json

curr_dir = os.path.dirname(os.path.abspath(__file__))


def write_order_to_json(item, quantity, price, buyer, date):
    filename = os.path.join(curr_dir, 'orders.json')

    with open(filename, 'r', encoding="utf-8") as file:
        data = json.loads(file.read())
    data['orders'].append({'item': item, 'quantity': quantity, 'price': price, 'buyer': buyer, 'date': date})
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, separators=(',', ': '), ensure_ascii=False)


write_order_to_json('Тест', '11', '5', 'Кто-то', '17.10.2022')
write_order_to_json('Тест 2', '0', '3', 'Путин', '17.10.2022')
