
#Вам доступен именованный кортеж Animal, который содержит данные о животном. Первым элементом именованного кортежа является имя животного, вторым — семейство, третьим — пол, четвертым — цвет. Также доступен файл data.pkl, содержащий сериализованный список таких кортежей.
#Дополните приведенный ниже код, чтобы для каждого кортежа из этого списка он вывел названия его полей и значения этих полей в следующем формате:


from collections import namedtuple
import pickle

Animal = namedtuple('Animal', ['name', 'family', 'sex', 'color'])

with open('data.pkl', 'rb') as pfile:
    file = pickle.load(pfile)
    for line in file:
        for field, value in zip(Animal._fields,line):
            print(f'{field}: {value}')
        print()
