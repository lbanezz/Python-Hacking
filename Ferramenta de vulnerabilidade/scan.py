import nmap

def scan_network(ip_range):
    """Realiza o scan da rede usando o nmap."""
    scanner = nmap.PortScanner()
    print(f"Iniciando scan em {ip_range}...")

    try:
        scanner.scan(hosts=ip_range, arguments='-sV --script vuln')
        for host in scanner.all_hosts():
            print(f"\nHost: {host} ({scanner[host].hostname()})")
            print(f"State: {scanner[host].state()}")

            for proto in scanner[host].all_protocols():
                print(f"\nProtocol: {proto}")
                ports = scanner[host][proto].keys()

                for port in ports:
                    port_info = scanner[host][proto][port]
                    print(f"Port: {port}\tState: {port_info['state']}\tService: {port_info.get('name', 'unknown')}")

                    if 'script' in port_info:
                        print("Vulnerabilities:")
                        for script, output in port_info['script'].items():
                            print(f"  - {script}: {output}")

    except nmap.PortScannerError as e:
        print(f"Erro ao executar o nmap: {e}")
    except Exception as e:
        print(f"Erro inesperado: {e}")

if __name__ == "__main__":
    # Defina o intervalo de IPs para escanear
    ip_range = input("Digite o intervalo de IPs (ex.: 192.168.0.1/24): ")
    scan_network(ip_range)
