import socket
import threading
import queue
from concurrent.futures import ThreadPoolExecutor
import tkinter as tk
from tkinter import messagebox

result_queue = queue.Queue()

def scan_port(ip, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(0.3)
        result = s.connect_ex((ip, port))
        try:
            service = socket.getservbyport(port)
        except OSError:
            service = "Serviço desconhecido"
        status = "aberta" if result == 0 else "fechada"
        result_queue.put(f"Porta {port} está {status} - {service}\n")

def scan_ip(ip, start_port, end_port):
    result_queue.put(f"Iniciando o scan no IP {ip} de {start_port} a {end_port}\n")
    with ThreadPoolExecutor(max_workers=300) as executor:
        for port in range(start_port, end_port + 1):
            executor.submit(scan_port, ip, port)

def start_scan():
    ip = ip_entry.get()
    try:
        start_port = int(start_port_entry.get())
        end_port = int(end_port_entry.get())
        if start_port > end_port:
            messagebox.showerror("Erro", "A porta inicial deve ser menor ou igual à porta final.")
            return
        output_text.delete(1.0, tk.END)
        threading.Thread(target=scan_ip, args=(ip, start_port, end_port), daemon=True).start()
    except ValueError:
        messagebox.showerror("Erro", "Por favor, insira valores numéricos válidos para as portas.")

def update_output():
    try:
        while True:
            message = result_queue.get_nowait()
            output_text.insert(tk.END, message)
            output_text.see(tk.END)
    except queue.Empty:
        pass
    root.after(100, update_output)

root = tk.Tk()
root.title("Scanner de Portas com Serviços")

tk.Label(root, text="IP a ser escaneado:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
ip_entry = tk.Entry(root, width=30)
ip_entry.grid(row=0, column=1, padx=5, pady=5)

tk.Label(root, text="Porta inicial:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
start_port_entry = tk.Entry(root, width=10)
start_port_entry.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)

tk.Label(root, text="Porta final:").grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
end_port_entry = tk.Entry(root, width=10)
end_port_entry.grid(row=2, column=1, padx=5, pady=5, sticky=tk.W)

scan_button = tk.Button(root, text="Iniciar Scan", command=start_scan)
scan_button.grid(row=3, column=0, columnspan=2, pady=10)

output_text = tk.Text(root, width=60, height=20)
output_text.grid(row=4, column=0, columnspan=2, padx=5, pady=5)

root.after(100, update_output)
root.mainloop()
