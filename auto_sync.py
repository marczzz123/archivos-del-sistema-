from github import Github, Auth
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time, os

# Token y repo
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
REPO_FULL_NAME = "marczzz123/archivos-del-sistema-"  # Cambia si tu repo es otro
LOCAL_FOLDER = "C:\\misScripts"  # Cambia si tu carpeta es diferente

# Conectar a GitHub usando la nueva forma recomendada
g = Github(auth=Auth.Token(GITHUB_TOKEN))
repo = g.get_repo(REPO_FULL_NAME)

class MyHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if not event.is_directory:
            file_name = os.path.basename(event.src_path)
            with open(event.src_path, "r", encoding="utf-8") as f:
                content = f.read()
            try:
                repo_file = repo.get_contents(file_name)
                repo.update_file(repo_file.path, f"Actualizando {file_name}", content, repo_file.sha)
                print(f"[UPDATE] Actualizado {file_name}")
            except:
                repo.create_file(file_name, f"Subiendo {file_name}", content)
                print(f"[UPLOAD] Subido {file_name}")

# Configurar el observador para monitorear la carpeta
observer = Observer()
observer.schedule(MyHandler(), LOCAL_FOLDER, recursive=False)
observer.start()

try:
    print("🟢 Auto-sync corriendo. Modifica o agrega archivos en C:\\misScripts para subirlos automáticamente a GitHub.")
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    observer.stop()
observer.join()
