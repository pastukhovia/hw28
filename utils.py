# Здесь происходит чтение данных из CSV файлов и их сохранение в JSON

import csv
import json


def read_from_csv(filename):
    # Чтение из CSV

    with open(f'./datasets/{filename}', encoding='utf-8', newline='') as csvfile:
        reader = csv.reader(csvfile)

        data = [row for row in reader]

        return data


def write_ads_to_json(data):
    # Запись в JSON файла ads.csv

    with open(f'./fixtures/ads.json', mode='w', encoding='utf-8') as jsonfile:
        data.pop(0)
        for row in data:
            if row[5] == 'TRUE':
                row[5] = True
            elif row[5] == 'FALSE':
                row[5] = False
        jsondata = [
            {
                "model": "ads.ad",
                "pk": row[0],
                "fields": {
                    "name": row[1],
                    "author": row[2],
                    "price": row[3],
                    "desc": row[4],
                    "is_published": row[5],
                    "image": row[6],
                    'category': row[7]
                }
            } for row in data]

        json.dump(jsondata, jsonfile, ensure_ascii=False, indent=4)


def write_categories_to_json(data):
    # Запись в JSON файла categories.csv

    with open(f'./fixtures/categories.json', mode='w', encoding='utf-8') as jsonfile:
        data.pop(0)
        jsondata = [
            {
                "model": "categories.category",
                "pk": row[0],
                "fields":
                    {
                        "name": row[1]
                    }
            } for row in data
        ]

        json.dump(jsondata, jsonfile, ensure_ascii=False, indent=4)


def write_locations_to_json(data):
    # Запись в JSON файла categories.csv

    with open(f'./fixtures/location.json', mode='w', encoding='utf-8') as jsonfile:
        data.pop(0)
        jsondata = [
            {
                "model": "locations.location",
                "pk": row[0],
                "fields":
                    {
                        "name": row[1],
                        'lat': row[2],
                        'lng': row[3]
                    }
            } for row in data]

        json.dump(jsondata, jsonfile, ensure_ascii=False, indent=4)


# id,first_name,last_name,username,password,role,age,location_id
def write_users_to_json(data):
    # Запись в JSON файла categories.csv

    with open(f'./fixtures/user.json', mode='w', encoding='utf-8') as jsonfile:
        data.pop(0)
        jsondata = [
            {
                "model": "users.user",
                "pk": row[0],
                "fields":
                    {
                        'first_name': row[1],
                        'last_name': row[2],
                        'username': row[3],
                        'password': row[4],
                        'role': row[5],
                        'age': row[6],
                        'location_id': row[7]
                    }
            } for row in data]

        json.dump(jsondata, jsonfile, ensure_ascii=False, indent=4)


write_ads_to_json(read_from_csv('ad.csv'))
write_categories_to_json(read_from_csv('category.csv'))
write_locations_to_json(read_from_csv('location.csv'))
write_users_to_json(read_from_csv('user.csv'))
