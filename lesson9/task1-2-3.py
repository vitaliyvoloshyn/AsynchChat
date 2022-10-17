import pythonping


ip_list = ['192.168.1.102', '192.168.1.103', '192.168.1.104', '192.168.1.105']


def ping(ips: list[str]) -> None:
    """Проверяет доступность хостов из списка пингованием"""
    for ip in ips:
        ping_resp = pythonping.ping(ip, timeout=2, count=1).success()
        print(ip + ' - reachable' if ping_resp else ip + ' - unreachable')


ping(ip_list)

# вывод:
# 192.168.1.102 - reachable
# 192.168.1.103 - reachable
# 192.168.1.104 - unreachable
# 192.168.1.105 - reachable
