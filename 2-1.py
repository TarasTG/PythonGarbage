import sys
import os
from itertools import takewhile

txt = ''

to_replace = {"(кв.м):": "(кв.м) - ",

              "Реєстраційний номер\nоб’єкта нерухомого\nмайна:": "Реєстраційний номер об’єкта нерухомого майна:",
              "Реєстраційний номер\nмайна:": "Реєстраційний номер об’єкта нерухомого майна:",

              "Об’єкт нерухомого\nмайна:": "Об’єкт нерухомого майна:",
              "Тип майна:": "Об’єкт нерухомого майна:",

              "Адреса нерухомого\nмайна:": "Адреса:",
              "\nЗагальна площа": "\nПлоща: Загальна площа",
              "ВІДОМОСТІ ПРО ОБ’ЄКТ НЕРУХОМОГО МАЙНА": "Актуальна інформація про об’єкт нерухомого майна",
              "ВІДОМОСТІ ПРО ПРАВА ВЛАСНОСТІ": "Відомості про права власності"
            }

to_drop = ["стор.", "RRP"]

csv_keys=[
"Реєстраційний номер об’єкта нерухомого майна",
"Об’єкт нерухомого майна",
"Площа",
"Адреса",
"Номер запису про право власності",
"Форма власності",
"Розмір частки",
"Власники",
"Номер запису про право власності2",
"Форма власності2",
"Розмір частки2",
"Власники2",
]

record_delimiter = "Актуальна інформація про об’єкт нерухомого майна"
internal_delimiter = "Відомості про права власності"

with open('input.txt', 'r', encoding='windows-1251') as my_file:
    txt = my_file.read()
    for key in to_replace:
        txt = txt.replace(key, to_replace[key])
    result = txt.replace(":\n", ":")

    result_1 = []
    result_2 = []

    for record in result.split(record_delimiter)[1:]:
        for line in record.split("\n"):
            if any([line.startswith(start) for start in to_drop]) or not line.strip():
                continue

            if (":" in line) or (line == internal_delimiter):
                result_1.append(line.strip())
            else:
                result_1[-1] += line.strip()

        full_record = []    
        record_gen = iter(result_1)
        full_record.extend(takewhile(lambda x: x != internal_delimiter, record_gen))

        record_dict = {}

        for elem in full_record:
            key, value = elem.split(":")
            record_dict[key] = value

        record_dict["Власники"] = '{soft}'.join(list(takewhile(lambda x: True, record_gen)))

        result_2.append(record_dict)

        result_1 = []

header = list(result_2[0].keys())
    
with open('out-2.csv','w', encoding='windows-1251') as my_file:
    my_file.write('|'.join(header))
    my_file.write("\n")
    for record in result_2:
        my_file.write('|'.join([str(record[key]) for key in header]))
        my_file.write("\n")


