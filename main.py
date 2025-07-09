import subprocess
import os
import sys

def main():
    root_path = os.path.dirname(os.path.abspath(__file__))

    # 👇 Esto permite importar desde 'utilities'
    sys.path.insert(0, root_path)

    script_path = os.path.join(root_path, "scripts", "create_base_structure.py")
    print(f"Ejecutando: {script_path}")

    result = subprocess.run([sys.executable, "-m", "scripts.create_base_structure"],
                            cwd=root_path,
                            env={**os.environ, "PYTHONPATH": root_path}
                            )

    if result.returncode != 0:
        print("❌ Error al ejecutar el script.")
        sys.exit(result.returncode)
    else:
        print("✅ Script ejecutado correctamente.")

if __name__ == "__main__":
    main()
