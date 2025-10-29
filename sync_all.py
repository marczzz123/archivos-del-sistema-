from github import Github
import os

# Token y repo
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
REPO_FULL_NAME = "marczzz123/archivos-del-sistema-"  # Cambia si tu repo es otro

# Carpeta local a sincronizar
LOCAL_FOLDER = "C:\\misScripts"  # Cambia si tu carpeta es diferente

# Conectar a GitHub
g = Github(GITHUB_TOKEN)
repo = g.get_repo(REPO_FULL_NAME)

# Listar archivos en la carpeta local
local_files = [f for f in os.listdir(LOCAL_FOLDER) if os.path.isfile(os.path.join(LOCAL_FOLDER, f))]

for file_name in local_files:
    file_path = os.path.join(LOCAL_FOLDER, file_name)
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    try:
        # Intentar obtener el archivo en GitHub
        repo_file = repo.get_contents(file_name)
        repo.update_file(repo_file.path, f"Actualizando {file_name}", content, repo_file.sha)
        print(f"[UPDATE] Actualizado {file_name} en GitHub")
    except:
        # Si no existe, crearlo
        repo.create_file(file_name, f"Subiendo {file_name}", content)
        print(f"[UPLOAD] Subido {file_name} a GitHub")
