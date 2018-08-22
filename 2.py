import sys
import os
import re

txt = ''

to_replace = {'Реєстраційний номер\nоб’єкта нерухомого\nмайна:':'Реєстраційний номер об’єкта нерухомого майна:',
              "Об’єкт нерухомого\nмайна":"Об’єкт нерухомого майна",
              "Відомості про права власності\n": "",
              "код ЄДРПОУ:": "код ЄДРПОУ - ",
              "(кв.м):": "(кв.м) - ",
              "RRP-4HHL4ICLR\n": "",
              "країна реєстрації:": "країна реєстрації - "
}

level_1 = "Реєстраційний номер об’єкта нерухомого майна"

with open('input.txt','r') as my_file:  
    txt = my_file.read()
    for key in to_replace:
        txt = txt.replace(key, to_replace[key])
    result = txt.replace(":\n", ":")
    result = [res for res in result.split("\n") if "стор." not in res]# [res for res in result.split(level_1) if "стор." not in res]
    result_1 = []
    txt = ""
    for i in range(0, len(result)-1):
        if ":" in result[i]:
            result_1.append(result[i])
        else:
            if len(result_1) > 0:
                result_1[len(result_1)-1] = result_1[len(result_1)-1] + ' ' + result[i]
            else:
                result_1.append(result[i])

    result = result_1

    result_1 = []

    for elem in '\n'.join(result).split(level_1):

        r = dict()

        for s in elem.split('\n'):
            if len(s.split(':')) > 1:
                r[s.split(':')[0]] = s.split(':')[1]

        result_1.append(r)

    result = ""

keys=[
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
  
result = '|'.join(keys)

for r in result_1:
    result = result + '|'.join(r.get(('' if k=="Реєстраційний номер об’єкта нерухомого майна" else k),'') for k in keys if k is not None) + '\n'

    
with open('out.csv','w') as my_file:
    my_file.write(result)

