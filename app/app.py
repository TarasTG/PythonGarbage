import io
import base64
import json
from time import sleep
import csv
from itertools import chain

import requests
import pandas

FILE_UPLOAD_HTML = """<html>
Convert PDF to .xlsx
<br>
<form action="https://hndrdphv58.execute-api.us-east-1.amazonaws.com/default/pdfConverterTTG" method="post" enctype="multipart/form-data">
  Select image to upload:
  <input type="file" name="fileToUpload" id="fileToUpload">
  <input type="submit" value="Upload PDF" name="submit">
</form>
</html>"""

START_CONVERSION_URL = "http://api.convertio.co/convert"
API_KEY = "608745a3c9efe0236d0369f591d304ee"
GET_CONVERSION_STATUS_URL = "https://api.convertio.co/convert/{id}/status"
GET_CONVERTED_FILE_URL = "https://api.convertio.co/convert/{id}/dl"
SLEEP_TIME = 10

level_1_destination_delimiter = '^level_1^'
level_2_destination_delimiter = '^level_2^'
to_replace = {"Актуальна інформація про об’єкт нерухомого майна": level_1_destination_delimiter,
              "ВІДОМОСТІ ПРО ОБ’ЄКТ НЕРУХОМОГО МАЙНА": level_1_destination_delimiter,
              "Відомості про права власності": level_2_destination_delimiter,
              "ВІДОМОСТІ ПРО ПРАВА ВЛАСНОСТІ": level_2_destination_delimiter,
              "Дата внесення запису": level_2_destination_delimiter + "Дата внесення запису",
              chr(12): ""
              }

main_info_starts = ["Реєстраційний номер", ]
own_info_starts = ["Дата внесення запису", "Номер запису про право власності / довірчої власності"]
skippers = ['стор.', 'RRP-', 'ВІДОМОСТІ', "З РЕЄСТРУ ПРАВ ВЛАСНОСТІ НА НЕРУХОМЕ МАЙНО"]

key_substitution = {"Реєстраційний номер об’єкта нерухомого майна:": "Реєстраційний номер майна:",
                    "Об’єкт нерухомого майна:": "Тип майна:",
                    "Загальна площа (кв.м):": "Площа:",
                    "Адреса нерухомого майна:": "Адреса:"
                    }

csv_keys = list(key_substitution.values())
csv_keys.append("Власники")


def pdf2txt(file_content):
    # file_content = base64.b64encode(file_content).decode('utf-8')
    result = requests.post(url=START_CONVERSION_URL,
                           data=json.dumps({"apikey": API_KEY, "input": "base64", "file": file_content,
                                            "filename": "in.pdf", "outputformat": "file_content"}))

    if result.status_code != 200:
        raise Exception(result.text)

    data = result.json()['data']
    id = data['id']
    print(f"Start conversion response: {data}")

    while True:
        print(f"Start sleeping for {SLEEP_TIME} seconds")
        sleep(SLEEP_TIME)

        result = requests.get(url=GET_CONVERSION_STATUS_URL.format(id=id))
        if result.status_code != 200:
            raise Exception(result.text)

        data = result.json()['data']
        print(f"Conversion status response: {data}")

        if data['step'] == 'finish':
            break

    result = requests.get(url=GET_CONVERTED_FILE_URL.format(id=id))
    if result.status_code != 200:
        raise Exception(result.text)

    data = result.json()['data']
    if data.get('error'):
        print(f"Conversion error: {data.get('error')}")
        raise Exception(data.get('error'))

    return base64.b64decode(data['content']).decode('utf-8')


def txt2dict(file_content: str):
    def _cut_starts(data, templates):
        for template in templates:
            if template in data:
                return data[data.index(template):]
        return data

    def _skip_unneeded_items(record, unneeded_items):
        result_record = []
        for line in record:

            new_line = []
            for block in line:
                skip_block = any(filter(lambda x: (x in block) or (not block.strip()), unneeded_items))
                if skip_block:
                    continue
                new_line.append(block)

            result_record.append(new_line)

        return result_record

    def _cleanup_record(record):
        result_record = []
        for line in record:
            new_line = [block for block in line if block.strip()]
            if new_line:
                result_record.append(new_line)

        return result_record

    def _build_dict_record(record):
        main_info_block = record[0]

        key_parts = [item[:item.index(':') + 1].strip() if ':' in item else item[:25].strip() for item in
                     main_info_block]
        value_parts = [item[item.index(':') + 1:].strip() if ':' in item else item[25:].strip() for item in
                       main_info_block]

        key_index = 0
        key = ''
        keys = []
        for key_part in key_parts:
            key_index += 1
            key += key_part + ' '
            if ':' in key_part:
                keys.append((key.strip(), key_index))
                key = ''
                key_index = 0

        if key:
            keys.append((key.strip(), key_index))

        fixed_keys = []

        offset = 0
        for index in range(len(keys) - 1, -1, -1):
            if not keys[index][0]:
                offset += 1
            else:
                fixed_keys.append((keys[index][0], keys[index][1] + offset))
                offset = 0

        record[0] = {}

        index = 0
        fixed_keys.reverse()
        for key, cnt in fixed_keys:
            record[0][key] = ' '.join(value_parts[index:index + cnt])
            index += cnt

        return record

    def _build_dict_records(records):
        return [_build_dict_record(record) for record in records]

    for from_what, to_what in to_replace.items():
        file_content = file_content.replace(from_what, to_what)

    file_content = file_content.split(level_1_destination_delimiter)[1:]

    records = []

    for block in file_content:
        data = block.split(level_2_destination_delimiter)

        record = [_cut_starts(data[0], main_info_starts).split('\n'),
                  *[_cut_starts(owner, own_info_starts).split('\n') for owner in data[1:]]]

        record = _skip_unneeded_items(record, skippers)
        record = _cleanup_record(record)
        if record:
            records.append(record)

    records = _build_dict_records(records)

    for record in records:
        record[0] = {key_substitution.get(key, key): value for key, value in record[0].items()}
        record[0]['Власники'] = chr(10).join(chain(*record[1:]))
        del record[1]

    return [record[0] for record in records]


def dict2csv(data):
    result_string = io.StringIO('')
    writer = csv.DictWriter(result_string, fieldnames=csv_keys, quoting=csv.QUOTE_ALL)
    writer.writerows(data)

    result_string.seek(0)
    return result_string.read()


def dict2xlsx(data):
    df = pandas.DataFrame(data)
    result_stringresult = io.BytesIO()
    df.to_excel(result_stringresult)
    return result_stringresult


def pdf2xlsx(pdf_data):
    data = txt2dict(pdf2txt(pdf_data))
    return dict2xlsx(data)


def lambda_handler(event, context):
    method = event['requestContext']['http']['method']
    if method == 'GET':
        return {
            'statusCode': 200,
            'headers': {'content-type': 'text/html'},
            'body': FILE_UPLOAD_HTML
        }
    elif method == 'POST':
        return {
            'statusCode': 200,
            'headers': {'content-type': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'},
            'body': pdf2xlsx(event['requestContext']['body'])
        }

    return {
        'statusCode': 400,
        'content-type': 'text/html',
        'body': f"Unsupported HTTP method {method}. Correct are: GET, POST"
    }
