# читаем адресную книгу в формате CSV в список contacts_list
import csv
import re


def clean_csv_phonebook(source_csv: str, clean_csv: str):
    with open(source_csv, encoding='utf-8') as f:
        rows = csv.reader(f, delimiter=",")
        contacts_list = list(rows)

    # TODO 1: выполните пункты 1-3 ДЗ
    clean_phonebook = {}
    last_name = ''
    first_name = ''
    sur_name = ''
    work_place = ''
    work_position = ''
    phone_number = ''
    e_mail = ''

    for item in contacts_list:

        line = ','.join(item)
        contact_id = str(re.findall(r'^[\w]+', line)).strip(" '[]")
        clean_phonebook[contact_id] = []

        person_regex = r'^([А-Я]?[а-я]+)(\s|,)([А-Я]?[а-я]+)(\s|,)([А-Я]?[а-я]+)(\s|,)+([\w]+)'
        person_data = re.findall(person_regex, line)
        for record in person_data:
            last_name = record[0]
            first_name = record[2]
            sur_name = record[4]
            work_place = record[6]
        contact_proxy = [last_name, first_name,
                         sur_name, work_place,'']

        position_regex = r'^([А-Я]?[а-я]+)(\s|,)([А-Я]?[а-я]+)(\s|,)([А-Я]?[а-я]+)(\s|,)+([\w]+)(\s|,)([\w /–]+)'
        position_data = re.findall(position_regex, line)
        for record in position_data:
            work_position = record[8]
            contact_proxy[4] = work_position

        phone_regex = r'[0-9\-]+'
        aux_phone_regex = r'(?<=доб. )[0-9]{4}'
        phone_string = re.findall(phone_regex, line)
        aux_phone_string = re.findall(aux_phone_regex, line)
        phone_digits = ''.join(phone_string).replace('-', '')
        if phone_string:
            phone_number = f'+7({phone_digits[1:4]})' \
                           f'{phone_digits[4:7]}-{phone_digits[7:9]}-' \
                           f'{phone_digits[9:11]}'
            if 'доб.' in line:
                phone_number += f' доб. {str(aux_phone_string[0])}'
            contact_proxy.append(phone_number)

        e_mail = str(re.findall(
            r'([\w/.]+@[a-zA-Z_]+?\.[a-zA-Z]{2,6})',
            ' '.join(item))).strip("'[]")
        contact_proxy.append(e_mail)

        clean_phonebook[contact_id] = contact_proxy

    del(clean_phonebook['lastname'])

    pb_output = [contacts_list[0]]
    for value in clean_phonebook.values():
        pb_output.append(value)
    pb_output = sorted(pb_output)

    # TODO 2: сохраните получившиеся данные в другой файл
    # код для записи файла в формате CSV
    with open(clean_csv, "wt",
              encoding='utf-8', newline='') as f:
        datawriter = csv.writer(f, delimiter=',', dialect='excel')
        # Вместо contacts_list подставьте свой список
        datawriter.writerows(pb_output)


if __name__ == '__main__':
    clean_csv_phonebook("phonebook_raw.csv", "clean_phonebook.csv")
