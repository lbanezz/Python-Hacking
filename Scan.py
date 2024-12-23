import socket
from concurrent.futures import ThreadPoolExecutor
import tkinter as tk
from tkinter import messagebox

# Função para verificar se uma porta está aberta
def scan_port(ip, port, output):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(1)  # Define um tempo limite para a conexão
        result = s.connect_ex((ip, port))  # Tenta se conectar
        if result == 0:
            output.insert(tk.END, f"Porta {port} está aberta\n")
        else:
            output.insert(tk.END, f"Porta {port} está fechada\n")

# Função principal para escanear as portas
def scan_ip(ip, start_port, end_port, output):
    output.delete(1.0, tk.END)  # Limpa o output
    output.insert(tk.END, f"Iniciando o scan no IP {ip} de {start_port} a {end_port}\n")
    with ThreadPoolExecutor(max_workers=100) as executor:
        for port in range(start_port, end_port + 1):
            executor.submit(scan_port, ip, port, output)

# Função para iniciar o escaneamento a partir da interface gráfica
def start_scan():
    ip = ip_entry.get()
    try:
        start_port = int(start_port_entry.get())
        end_port = int(end_port_entry.get())
        if start_port > end_port:
            messagebox.showerror("Erro", "A porta inicial deve ser menor ou igual à porta final.")
            return
        scan_ip(ip, start_port, end_port, output_text)
    except ValueError:
        messagebox.showerror("Erro", "Por favor, insira valores numéricos válidos para as portas.")

# Criação da interface gráfica
root = tk.Tk()
root.title("Escaneador de Portas")

# Labels e campos de entrada
tk.Label(root, text="IP a ser escaneado:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
ip_entry = tk.Entry(root, width=30)
ip_entry.grid(row=0, column=1, padx=5, pady=5)

tk.Label(root, text="Porta inicial:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
start_port_entry = tk.Entry(root, width=10)
start_port_entry.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)

tk.Label(root, text="Porta final:").grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
end_port_entry = tk.Entry(root, width=10)
end_port_entry.grid(row=2, column=1, padx=5, pady=5, sticky=tk.W)

# Botão para iniciar o escaneamento
scan_button = tk.Button(root, text="Iniciar Scan", command=start_scan)
scan_button.grid(row=3, column=0, columnspan=2, pady=10)

# Área de texto para mostrar os resultados
output_text = tk.Text(root, width=50, height=15)
output_text.grid(row=4, column=0, columnspan=2, padx=5, pady=5)

# Inicia o loop principal da interface gráfica
root.mainloop()
