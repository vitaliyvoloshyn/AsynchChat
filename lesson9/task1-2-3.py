from ipaddress import ip_address

import pythonping
import tabulate


def host_gen(count: int = 1, base_ip: str = '192.168.1.100') -> list[str]:
    """
    Генерирует список ip адресов путем арифметического добавления 1 к последнему октету базового адреса
    """
    base_ip = ip_address(base_ip)
    return [str(base_ip + i) for i in range(count)]


def ping_tab(ips: list[str]) -> None:
    """Проверяет доступность хостов из списка пингованием"""
    res = {'reachable': [],
           'unreachable': []}
    for ip in ips:
        ping_resp = pythonping.ping(ip, timeout=2, count=1).success()
        if ping_resp:
            res['reachable'].append(ip)
        else:
            res['unreachable'].append(ip)
    print(tabulate.tabulate(res, headers='keys', tablefmt='grid'))


ip_list = host_gen(10)
ping_tab(ip_list)

# вывод:
# +---------------+---------------+
# | reachable     | unreachable   |
# +===============+===============+
# | 192.168.1.101 | 192.168.1.100 |
# +---------------+---------------+
# | 192.168.1.102 | 192.168.1.103 |
# +---------------+---------------+
# | 192.168.1.105 | 192.168.1.104 |
# +---------------+---------------+
# |               | 192.168.1.106 |
# +---------------+---------------+
# |               | 192.168.1.107 |
# +---------------+---------------+
# |               | 192.168.1.108 |
# +---------------+---------------+
# |               | 192.168.1.109 |
# +---------------+---------------+
