from datetime import date, timedelta, datetime
import json
date_pattern = "%d.%m.%Y"
#Создание JSON файла с расписанием на месяц. Словарь[дата][время] = none
day_shedule = {'9:00':None, '10:30':None, '12:00':None, '13:30':None, '15:00':None, '16:30':None, '18:00':None, '19:30':None} #расписание на день
month_shedule = {}
now = datetime.now()
for d in range(30):
    month_shedule[(now + timedelta(days=d)).strftime(date_pattern)] = day_shedule.copy()

with open ('month.json', 'w', encoding='utf-8') as file:
    json.dump(month_shedule, file)
#Конец создания json
print('JSON файл успешно создан')