import pythonping
from ipaddress import ip_address


def host_gen(count: int = 1, base_ip: str = '192.168.1.100') -> list[str]:
    """
    Генерирует список ip адресов путем арифметического добавления 1 к последнему октету базового адреса
    """
    base_ip = ip_address(base_ip)
    return [str(base_ip + i) for i in range(count)]


def ping(ips: list[str]) -> None:
    """Проверяет доступность хостов из списка пингованием"""
    for ip in ips:
        ping_resp = pythonping.ping(ip, timeout=2, count=1).success()
        print(ip + ' - reachable' if ping_resp else ip + ' - unreachable')


ip_list = host_gen(10)
ping(ip_list)

# вывод:
# 192.168.1.100 - unreachable
# 192.168.1.101 - reachable
# 192.168.1.102 - reachable
# 192.168.1.103 - unreachable
# 192.168.1.104 - unreachable
# 192.168.1.105 - reachable
# 192.168.1.106 - unreachable
# 192.168.1.107 - unreachable
# 192.168.1.108 - unreachable
# 192.168.1.109 - unreachable
