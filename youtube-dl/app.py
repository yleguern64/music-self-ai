from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic import BaseModel
import os
import subprocess

app = FastAPI()
security = HTTPBasic()

# Credentials via variables d'environnement
USERNAME = os.getenv("API_USERNAME", "admin")
PASSWORD = os.getenv("API_PASSWORD", "secret")

class DownloadRequest(BaseModel):
    url: str  # URL YouTube
    start_time: int = 0  # Début en secondes
    end_time: int = None  # Fin en secondes (optionnel)

def check_auth(credentials: HTTPBasicCredentials = Depends(security)):
    if credentials.username != USERNAME or credentials.password != PASSWORD:
        raise HTTPException(status_code=401, detail="Unauthorized")

@app.post("/download-audio")
def download_audio(request: DownloadRequest, credentials: HTTPBasicCredentials = Depends(check_auth)):
    input_dir = "/input"
    input_template = f"{input_dir}/%(title)s.%(ext)s"

    # Construire l'argument de démarrage et de fin
    postprocessor_args = []
    if request.start_time is not None:
        postprocessor_args.append(f"-ss {request.start_time}")
    if request.end_time is not None:
        postprocessor_args.append(f"-to {request.end_time}")

    try:
        # Exécuter YouTube-DL pour extraire uniquement l’audio
        command = [
            "yt-dlp",
            "-x", "--audio-format", "mp3",  # Extraire l’audio en MP3
            "--audio-quality", "0",  # Best qualité audio
            "-o", input_template,  # Modèle de sortie
            request.url
        ]

        # Si on a un start_time ou end_time, on passe les arguments
        if postprocessor_args:
            command.extend(["--postprocessor-args", " ".join(postprocessor_args)])

        result = subprocess.run(command, capture_output=True, text=True, check=True)

        return {"message": "Téléchargement terminé", "url": request.url, "logs": result.stdout}

    except subprocess.CalledProcessError as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors du téléchargement : {e.stderr}")
