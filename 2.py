import sys
import os
import re

txt = ''

to_replace = {'Реєстраційний номер\nоб’єкта нерухомого\nмайна:':'Реєстраційний номер об’єкта нерухомого майна:',
              "Об’єкт нерухомого\nмайна":"Об’єкт нерухомого майна",
              "Відомості про права власності\n": "",
              "код ЄДРПОУ:": "код ЄДРПОУ - ",
              "(кв.м):": "(кв.м) - ",
              "RRP-4HHL4ICLR\n": ""
}

level_1 = "Реєстраційний номер об’єкта нерухомого майна"

with open('input.txt','r') as my_file:  
    txt = my_file.read()
    for key in to_replace:
        txt = txt.replace(key, to_replace[key])
    result = txt.replace(":\n", ":")
    result = [res for res in result.split(level_1) if "стор." not in res]
    result_1 = []
    txt = ""
    for i in range(0, len(result)-1):
        if ":" in result[i]:
            result_1.append(result[i])
        else: 
            try:
                result_1[len(result_1)-1] = result_1[len(result_1)-1] + result[i]
            except: pass

    result = result_1
    

    
with open('out.txt','w') as my_file:        
    my_file.write(('\n=======================================\n'+level_1).join(result))