txt = ''

to_replace = {'Реєстраційний номер\nоб’єкта нерухомого\nмайна:':'Реєстраційний номер об’єкта нерухомого майна:',
              #'Актуальна інформація про об’єкт нерухомого майна': '',
              "Об’єкт нерухомого\nмайна":"Об’єкт нерухомого майна",
              "Відомості про права власності\n": "",
              "код ЄДРПОУ:": "код ЄДРПОУ - ",
              "(кв.м):": "(кв.м) - ",
              "RRP-4HIA3O5J2": "",
              "країна реєстрації:": "країна реєстрації - "
}

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

level_1 = "Реєстраційний номер об’єкта нерухомого майна"

#with open('input.txt', 'r', encoding='windows-1251') as my_file:
with open('input.txt', 'r') as my_file:
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

        keys = list(s.split(':')[0] for s in elem.split('\n'))
        new_keys = []
        for key in keys:
            cnt = 2
            if key in new_keys:
                key = key + str(cnt)
                cnt += 1
            new_keys.append(key)

        new_dict = {}
        cnt = 0
        for s in elem.split('\n'):
            para = s.split(':')
            if len(para) <= 1: continue
            new_dict[new_keys[cnt]] = para[1]
            cnt += 1

        result_1.append(new_dict)

    result = ""
  
result = '|'.join(csv_keys)

result_1.pop(0)

for record in result_1:
    row = ''
    for key in csv_keys:
        row += record.get('' if key==csv_keys[0] else key, '') + '|'

    result += '\n' + row

#result+='\n'.join('|'.join(r.get(('' if k=="Реєстраційний номер об’єкта нерухомого майна" else k),'') for k in keys if k is not None for r in result_1))
    
with open('out-1.csv','w', encoding='windows-1251') as my_file:
    my_file.write(result)

