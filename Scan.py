import socket
from concurrent.futures import ThreadPoolExecutor

# Função para verificar se uma porta está aberta
def scan_port(ip, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(1)  # Define um tempo limite para a conexão
        result = s.connect_ex((ip, port))  # Tenta se conectar
        if result == 0:
            print(f"Porta {port} está aberta")
        else:
            print(f"Porta {port} está fechada")

# Função principal para escanear as portas
def scan_ip(ip, start_port, end_port):
    print(f"Iniciando o scan no IP {ip} de {start_port} a {end_port}")
    with ThreadPoolExecutor(max_workers=100) as executor:
        for port in range(start_port, end_port + 1):
            executor.submit(scan_port, ip, port)

# Exemplo de uso
if __name__ == "__main__":
    target_ip = input("Digite o IP a ser escaneado: ")
    start_port = int(input("Digite a porta inicial: "))
    end_port = int(input("Digite a porta final: "))
    scan_ip(target_ip, start_port, end_port)
