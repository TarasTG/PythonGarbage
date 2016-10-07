import sys
import os
import re

txt = ''

to_remove = {'Актуальна інформація про право власності',
             'права власності:',
             'реєстрації:',
             'запису:',
             'об’єкта нерухомого майна:',
             '"'}

level_1 = {'Актуальна інформація про об’єкт нерухомого майна','ВІДОМОСТІ ПРО ОБ’ЄКТ НЕРУХОМОГО МАЙНА'}

level_2 = {'Форма власності:','Частка власності:','Реєстраційний номер',
           'Тип майна:','Адреса нерухомого','Підстава виникнення',
           'Дата внесення','Об’єкт нерухомого','Площа:','Адреса:','Номер запису про право',
           'Дата, час державної','Державний реєстратор:','Підстава внесення','Розмір частки:','Власники:',
           'Вид спільної власності:','Додаткові відомості:','Відомості про реєстрацію',
           'Технічний опис майна:','Дата прийняття рішення','ПІБ:',
           'Дата реєстрації:', 'Дата :'}

level_2_set = set(level_2)

replace_to = [('ПІБ:', 'Власники:'),
              ('вартира №','в-ра №'),
              ('Загальна площа','\nЗагальна площа'),
              ('Дата внесення запису:','Дата, час державної'),
              ('Дата внесення','Дата, час державної'),
              ('приміщення №', 'кв-ра №'),
              ('приміщення', 'квартира')
             ]

with open('input.txt','r') as my_file:
    txt = my_file.read().replace('\n',' ')

    for obj in replace_to:
        txt = txt.replace(obj[0],obj[1])    

    for obj in level_1:
        txt = txt.replace(obj,'\n=====')
    
    for obj in to_remove:
        txt = txt.replace(obj,'')

    for obj in level_2_set:
        txt = txt.replace(obj,'\n' + obj.replace(':','') + ':')

    txt = txt.replace('квартира','\nКвартира:')    

    res_l = txt.split('\n=====')
        
res_out = []

with open('out_raw.txt','w') as my_file:
    my_file.write(txt)

for obj in res_l:
    list_2 = str(obj).split('\n')

    kv = ''
    vlas = ''
    data = ''

    for obj2 in list_2:
        if re.search(r'^Квартира:',obj2):
            kv = obj2.replace('Квартира:','').replace(' ','')
        elif  re.search(r'^Власники:',obj2):
            vlas += obj2.replace('Власники:','') + ','
        elif  re.search(r'^Дата, час державної:',obj2):
            data = obj2.replace('Дата, час державної:','').replace(' ','')
    
    res_out.append([kv, vlas, data, str(obj)])

txt = ''

with open('out.txt','w') as my_file:
    res_out[0]=['Квартира','Собственники','Дата регистрации','Общая информация']
    for obj in res_out:
        txt += obj[0] + '|' + obj[1] + '|' + obj[2] + '|"' + obj[3].replace('\n','<br>') + '"\n'
    
    my_file.write(txt)