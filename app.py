import os
import subprocess
from flask import Flask, send_from_directory, abort
import logging

logging.getLogger("werkzeug").disabled = True

SITE_DIR = "site"

# Sempre roda mkdocs build ao iniciar
print(">> Gerando site com MkDocs...")
subprocess.run(["mkdocs", "build"], check=True)

app = Flask(__name__, static_folder=SITE_DIR)
PORT = int(os.environ.get("PORT", 8080))

@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def serve(path):
    full_path = os.path.join(SITE_DIR, path)

    # Se for diretório, tenta index.html
    if os.path.isdir(full_path):
        return send_from_directory(full_path, "index.html")

    # Se for arquivo existente, serve direto
    if os.path.isfile(full_path):
        return send_from_directory(SITE_DIR, path)

    # Se a rota termina com /, tenta index.html dentro
    if path.endswith("/"):
        new_path = os.path.join(SITE_DIR, path, "index.html")
        if os.path.isfile(new_path):
            return send_from_directory(os.path.join(SITE_DIR, path), "index.html")

    abort(404)

if __name__ == "__main__":
    print(f">> Servidor rodando em http://localhost:{PORT}/")
    app.run(host="0.0.0.0", port=PORT, debug=False)