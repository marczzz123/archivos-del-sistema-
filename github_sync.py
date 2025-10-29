# github_sync.py
import os
import sys
from github import Github
from pathlib import Path

# Config
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
if not GITHUB_TOKEN:
    raise SystemExit("Error: define la variable de entorno GITHUB_TOKEN con tu token de GitHub.")

# Reemplaza con tu repo (usuario/nombre)
REPO_FULL_NAME = "marczzz123/archivos-del-sistema-"

# Inicializar cliente
g = Github(GITHUB_TOKEN)
repo = g.get_repo(REPO_FULL_NAME)

def upload_or_update(local_path: str, repo_path: str, commit_message: str):
    """Sube o actualiza un archivo en el repositorio."""
    local_path = Path(local_path)
    if not local_path.exists():
        print(f"[ERROR] Archivo local no encontrado: {local_path}")
        return

    content = local_path.read_text(encoding="utf-8")
    try:
        contents = repo.get_contents(repo_path)
        repo.update_file(contents.path, commit_message, content, contents.sha)
        print(f"[UPDATE] Actualizado {repo_path} con {local_path.name}")
    except Exception:
        repo.create_file(repo_path, commit_message, content)
        print(f"[CREATE] Creado {repo_path} desde {local_path.name}")

def download_file(repo_path: str, out_local_path: str):
    """Descarga un archivo del repo."""
    try:
        contents = repo.get_contents(repo_path)
        data = contents.decoded_content.decode("utf-8")
        Path(out_local_path).write_text(data, encoding="utf-8")
        print(f"[DOWNLOAD] Guardado {repo_path} -> {out_local_path}")
    except Exception as e:
        print("[ERROR] No se pudo descargar:", e)

def list_files(path=""):
    """Lista archivos del repo."""
    try:
        items = repo.get_contents(path)
        for it in items:
            print(f"- {it.path}  ({it.type})")
    except Exception as e:
        print("[ERROR] No se pudo listar:", e)

# Modo CLI
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso:\n  upload <local_path> <repo_path> <commit_message>\n  download <repo_path> <out_local_path>\n  list [path]")
        sys.exit(0)

    cmd = sys.argv[1].lower()
    if cmd == "upload" and len(sys.argv) >= 5:
        _, _, local, repo_p, *rest = sys.argv
        msg = " ".join(rest) if rest else "Actualización desde script"
        upload_or_update(local, repo_p, msg)
    elif cmd == "download" and len(sys.argv) >= 4:
        _, _, repo_p, outp = sys.argv
        download_file(repo_p, outp)
    elif cmd == "list":
        path = sys.argv[2] if len(sys.argv) >= 3 else ""
        list_files(path)
    else:
        print("Comando no reconocido o argumentos insuficientes.")
