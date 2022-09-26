'''Выполнить пинг веб-ресурсов yandex.ru, youtube.com и преобразовать результаты из
байтовового в строковый тип на кириллице.'''

import subprocess

args1 = ['ping', 'yandex.ru']
args2 = ['ping', 'youtube.com']
subproc_ping1 = subprocess.Popen(args1, stdout=subprocess.PIPE)
subproc_ping2 = subprocess.Popen(args2, stdout=subprocess.PIPE)

for line in subproc_ping1.stdout:
    line = line.decode('cp866').encode('utf-8')
    print(line.decode('utf-8'), end='')

for line in subproc_ping2.stdout:
    line = line.decode('cp866').encode('utf-8')
    print(line.decode('utf-8'), end='')
