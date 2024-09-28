#Реализуйте функцию get_biggest(), которая принимает один аргумент:
#numbers — список целых неотрицательных чисел
#Функция должна возвращать наибольшее число, которое можно составить из чисел из списка numbers. Если список numbers пуст, функция должна вернуть число -1


def get_biggest(numbers):
    if len(numbers) == 0: return -1
    numbers =list(map(str, numbers))
    max_len = max(map(len, numbers))
    numbers = sorted(numbers, key = lambda x: x * max_len, reverse= True)
    
    return (int(''.join(numbers)))

print(get_biggest([0, 0, 0, 0, 0, 0]))