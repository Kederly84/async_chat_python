import os
import re
import csv
import chardet

curr_dir = os.path.dirname(os.path.abspath(__file__))


def collect_data():
    data_dir = os.path.join(curr_dir)
    result = []
    source_files = [i for i in os.listdir(data_dir) if i.split('.')[1] == 'txt']
    detector = chardet.UniversalDetector()
    for filename in source_files:
        filepath = os.path.join(data_dir, filename)
        with open(filepath, 'rb') as file:
            for _ in file:
                detector.feed(_)
                if detector.done:
                    break
            detector.close()
        with open(filepath, encoding=detector.result['encoding']) as f:
            for line in f.readlines():
                result += re.findall(r'^(\w[^:]+).*:\s+([^:\n]+)\s*$', line)
    return result


def get_data():
    data = collect_data()
    os_prod_list, os_name_list, os_code_list, os_type_list = [], [], [], []
    main_data = [['Изготовитель системы', 'Название ОС', 'Код продукта', 'Тип системы']]
    for item in data:
        if item[0] == main_data[0][0]:
            os_prod_list.append(item[1])
        if item[0] == main_data[0][1]:
            os_name_list.append(item[1])
        if item[0] == main_data[0][2]:
            os_code_list.append(item[1])
        if item[0] == main_data[0][3]:
            os_type_list.append(item[1])
    for i in range(len(os_prod_list)):
        main_data.append([os_prod_list[i], os_name_list[i], os_code_list[i], os_type_list[i]])
    return main_data


def write_to_csv(filepath):
    data = get_data()
    with open(filepath, 'w', encoding='utf-8', newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter=',', quoting=csv.QUOTE_NONNUMERIC)
        for line in data:
            writer.writerow(line)


write_to_csv('main_data.csv')
