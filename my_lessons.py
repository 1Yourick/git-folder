# Вам доступен текстовый файл files.txt, содержащий информацию о файлах.
# Каждая строка файла содержит три значения, разделенные символом пробела — имя файла, его размер (целое число) и единицы измерения:
#
# cant-help-myself.mp3 7 MB
# keep-yourself-alive.mp3 6 MB
# bones.mp3 5 MB
# ...
# Напишите программу, которая группирует данные файлы по расширению, определяя общий объем файлов каждой группы,
# и выводит полученные группы файлов, указывая для каждой ее общий объем. Группы должны быть расположены в
# лексикографическом порядке названий расширений, файлы в группах — в лексикографическом порядке их имен.
from collections import defaultdict

lines = defaultdict(list)

def file_size_in_bytes(value, unit):
    value = int(value)
    if unit == 'B':return value
    elif unit == 'KB':return value * 1024
    elif unit == 'MB':return value * 1024 * 1024
    elif unit == 'GB': return value * 1024 * 1024 * 1024

def hight_unit(value:int):
    u = 0
    u_dict = {0:'B', 1:'KB', 2:'MB', 3:'GB'}
    while value > 1023:
        value = value / 1024
        u += 1
    return round(value), u_dict[u]

with open('files.txt', 'r', encoding='utf-8') as file:
    for line in file.readlines():
        line = line.strip().split(' ')
        key = (line[0].split('.')[1])  # расширение файла (.ру)

        lines[key].append(line)


    for key in sorted(lines.keys()):
        file_size = 0 #bytes
        for file in sorted(lines[key], key = lambda x: x[0]):
            print(file[0])
            file_size += file_size_in_bytes(file[1], file[2])

        print('----------')
        fsu = hight_unit(file_size) # 1 MB  tuple
        print(f'Summary: {fsu[0]} {fsu[1]}')
        print()