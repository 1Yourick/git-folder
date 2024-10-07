import datetime
import locale

locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')

current_date = datetime.date.today()
tomorow = current_date + datetime.timedelta(days=1)
print(datetime.datetime.weekday(tomorow))
#print(tomorow.strftime('%d.%m.%Y'))

week_list = list()
for i in range(8):
    week_list.append((datetime.date.today() + datetime.timedelta(days=i)).strftime('%d.%m.%Y %A'))

for d in week_list:
    print(d)
