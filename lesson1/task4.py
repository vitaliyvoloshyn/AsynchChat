'''Преобразовать слова «разработка», «администрирование», «protocol», «standard» из
строкового представления в байтовое и выполнить обратное преобразование (используя
методы encode и decode).'''

strs = ['разработка', 'администрирование', 'protocol', 'standard']


def printout(func):
    """декоратор вывода"""
    def wrapper(*args):
        res = func(*args)
        print(f'{func.__name__} - {res}')
        return res

    return wrapper


@printout
def to_byte_type(*args: str) -> list[bytes]:
    """преобразование строки в байтовый тип"""
    return [arg.encode() for arg in args]


@printout
def to_str_type(*args: bytes) -> list[str]:
    """преобразование байт в строковый тип"""
    return [arg.decode() for arg in args]


to_str_type(*to_byte_type(*strs))
