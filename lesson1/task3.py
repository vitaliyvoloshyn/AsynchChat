'''Определить, какие из слов «attribute», «класс», «функция», «type» невозможно записать в
байтовом типе.'''


def to_byte_type(*args: str) -> None:
    """преобразует строку в байтовый тип"""
    for arg in args:
        print(arg.encode())


strs = ['attribute', 'класс', 'функция', 'type']
to_byte_type(*strs)

# Вывод 
# b'attribute'
# b'\xd0\xba\xd0\xbb\xd0\xb0\xd1\x81\xd1\x81'
# b'\xd1\x84\xd1\x83\xd0\xbd\xd0\xba\xd1\x86\xd0\xb8\xd1\x8f'
# b'type'
# строки "класс" и "функция" невозможно записать в байтовом типе
