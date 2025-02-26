from fastapi import FastAPI, HTTPException, UploadFile, File, Form, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import os
import subprocess
import json
import glob

app = FastAPI()
security = HTTPBasic()

# Credentials via variables d'environnement
USERNAME = os.getenv("API_USERNAME", "user")
PASSWORD = os.getenv("API_PASSWORD", "password")
NB_THREAD = os.getenv("NB_THREAD", "16")

def check_auth(credentials: HTTPBasicCredentials = Depends(security)):
    if credentials.username != USERNAME or credentials.password != PASSWORD:
        raise HTTPException(status_code=401, detail="Unauthorized")

@app.post("/transcribe")
async def transcribe_audio(
    file: UploadFile = File(...),
    language: str = Form("en"),  # Langue par défaut = français
    credentials: HTTPBasicCredentials = Depends(check_auth)
):
    output_dir = "/output"
    os.makedirs(output_dir, exist_ok=True)

    # Sauvegarder le fichier temporairement
    temp_file_path = f"{output_dir}/{file.filename}"
    with open(temp_file_path, "wb") as buffer:
        buffer.write(file.file.read())

    # Construire la commande Whisper CLI
    command = [
        "whisper", temp_file_path,
        "--language", language,
        "--task", "transcribe",
        "--output_format", "json",
        "--model=medium", "--device=cpu", "--verbose=True", f"--threads={NB_THREAD}",
        "--output_dir={output_dir}"
    ]

    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)

        # Trouver le fichier JSON généré (peut être renommé par Whisper)
        json_output_files = glob.glob(f"{output_dir}/*.json")
        if not json_output_files:
            raise HTTPException(status_code=500, detail="Aucun fichier JSON généré par Whisper")

        json_output_file = json_output_files[0]  # Prendre le premier fichier trouvé

        # Charger la transcription depuis le fichier JSON
        with open(json_output_file, "r") as json_file:
            transcription_data = json.load(json_file)

        return {
            "message": "Transcription terminée",
            "file": file.filename,
            "language": language,
            "transcription": transcription_data
        }

    except subprocess.CalledProcessError as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la transcription : {e.stderr}")
