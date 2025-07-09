import os

def create_directory(path):
    os.makedirs(path, exist_ok=True)
    print(f"[+] Carpeta creada: {path}")
