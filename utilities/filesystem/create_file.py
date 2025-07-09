def create_file(path, content=""):
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"[+] Archivo creado: {path}")
