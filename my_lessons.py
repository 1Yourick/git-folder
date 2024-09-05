# У Тимура имеется немало друзей из других городов или стран, которые часто приезжают к нему
# в гости с целью увидеться и развлечься. Чтобы не забыть ни об одной встрече, Тимур записывает
# имена и фамилии друзей в csv файл, дополнительно указывая для каждого дату и время встречи.
# Вам доступен этот файл, имеющий название meetings.csv, в котором в первом столбце записана фамилия,
# во втором — имя, в третьем — дата в формате DD.MM.YYYY , в четвертом — время в формате HH:MM:
# Напишите программу, которая выводит фамилии и имена друзей Тимура, предварительно отсортировав
# их по дате и времени встречи от самой ранней до самой поздней. Фамилии и имена должны быть расположены каждые на отдельной строке.

import csv
from datetime import datetime
from collections import namedtuple

with open('meetings.csv', encoding='utf-8') as csv_file:
    headers = csv_file.readline()
    rows = csv.reader(csv_file)
    frends_list = list()

    # Friends = namedtuple('Friends', headers)
    for row in rows:
        d = datetime.strptime(row[2]+'_'+row[3], '%d.%m.%Y_%H:%M')
        frends_list.append(
            [row[0] + ' ' + row[1], d])

    frends_list = sorted(frends_list, key=lambda x: x[1])
for f in frends_list:
    print(f[0])
