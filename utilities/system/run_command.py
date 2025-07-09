import subprocess


def run_command(cmd, cwd=None):
    print(f"[RUNNING]: {cmd} (cwd={cwd})")
    result = subprocess.run(cmd, cwd=cwd, shell=True)
    if result.returncode != 0:
        raise Exception(f"Command failed: {cmd}")
