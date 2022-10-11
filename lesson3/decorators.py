import inspect
import sys
from datetime import datetime

from log import FunctionCallLog


def function_log(func: callable):
    def wrapper(*args, **kwargs):
        logger = FunctionCallLog().create_logger()

        func(*args, **kwargs)
        logger.debug(
            f'Вызвана функция - {func.__name__}, из модуля {sys.argv[0]}, переданы аргументы - {*args, kwargs}')
        logger.debug(
            f'{datetime.now()} Функция {func.__name__} вызвана из функции {inspect.currentframe().f_back.f_code.co_name}')
    return wrapper
