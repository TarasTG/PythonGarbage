import sys
import os
from itertools import takewhile
import locale
import csv
import openpyxl
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import StringIO

default_encoding = locale.getpreferredencoding()


def convert_pdf_to_txt(path):
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
    fp = open(path, 'rb')
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    password = ""
    maxpages = 0
    caching = True
    pagenos=set()

    for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password,caching=caching, check_extractable=True):
        interpreter.process_page(page)

    text = retstr.getvalue()

    fp.close()
    device.close()
    retstr.close()
    return text


def convert_csv_to_xlsx(csv_filename, xlsx_filename, csv_delimiter=",", csv_file_encoding=default_encoding):
    workbook = openpyxl.Workbook()
    worksheet = workbook.active
    with open(csv_filename, "r", encoding=csv_file_encoding) as fobj:
        csv_reader = csv.reader(fobj, delimiter=csv_delimiter)
        for row_index, row in enumerate(csv_reader):
            for col_index, value in enumerate(row):
                worksheet.cell(row_index + 1, col_index + 1).value = value
    workbook.save(xlsx_filename)


def do_convert(delimiter, encoding, csv_file, xlsx_file):
    """Convert csv file to xlsx file.

    Usage:

    convert-csv-to-xlsx test.csv test.xlsx
    """
    if not xlsx_file:
        name, ext = os.path.splitext(csv_file)
        xlsx_file = name + ".xlsx"
    convert_csv_to_xlsx(csv_file, xlsx_file, delimiter, encoding)
    print("Excel file created at: {0}".format(xlsx_file))


def prepare_csv():
    soft_delimiter = '\x0A'
    soft_delimiter = '^^'

    to_replace = {"(кв.м):": "(кв.м) - ",

                  "Реєстраційний номер\nоб’єкта нерухомого\nмайна:": "Реєстраційний номер об’єкта нерухомого майна:",
                  "Реєстраційний номер\nмайна:": "Реєстраційний номер об’єкта нерухомого майна:",

                  "Об’єкт нерухомого\nмайна:": "Об’єкт нерухомого майна:",
                  "Тип майна:": "Об’єкт нерухомого майна:",

                  "Адреса нерухомого\nмайна:": "Адреса:",
                  "\nЗагальна площа": "\nПлоща: Загальна площа",
                  "ВІДОМОСТІ ПРО ОБ’ЄКТ НЕРУХОМОГО МАЙНА": "Актуальна інформація про об’єкт нерухомого майна",
                  "ВІДОМОСТІ ПРО ПРАВА ВЛАСНОСТІ": "Відомості про права власності",
                  "\"": "'"
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

        to_drop.append(result[:13])

        for record in result.split(record_delimiter)[1:]:
            for line in record.split("\n"):
                if any([line.startswith(start) for start in to_drop]) or not line.strip():
                    continue

                if (":" in line) or (line == internal_delimiter):
                    result_1.append(line.strip())
                else:
                    result_1[-1] += ' ' + line.strip()

            full_record = []
            record_gen = iter(result_1)
            full_record.extend(takewhile(lambda x: x != internal_delimiter, record_gen))

            record_dict = {}
            additional_info = None
            for elem in full_record:
                try:
                    key, value = elem.split(":")
                except:
                    additional_info = elem
                else:                   
                    record_dict[key] = value

            record_dict["Власники"] = '"' + (additional_info or soft_delimiter.join(list(takewhile(lambda x: True, record_gen)))) + '"'

            result_2.append(record_dict)

            result_1 = []

    header = list(result_2[0].keys())

    with open('out-2.csv','w', encoding='windows-1251') as my_file:
        my_file.write('|'.join(header))
        my_file.write("\n")
        for record in result_2:
            my_file.write('|'.join([str(record.get(key, '')) for key in header]))
            my_file.write("\n")


convert_pdf_to_txt("test.pdf")
#prepare_csv()

#do_convert(delimiter='|', encoding='utf-8', csv_file='out-2.csv', xlsx_file='out.xlsx')