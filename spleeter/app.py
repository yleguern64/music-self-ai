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

class WorkerRequest(BaseModel):
    file: str  # Nom du fichier à traiter

def check_auth(credentials: HTTPBasicCredentials = Depends(security)):
    if credentials.username != USERNAME or credentials.password != PASSWORD:
        raise HTTPException(status_code=401, detail="Unauthorized")

@app.post("/run-worker")
def run_worker(request: WorkerRequest, credentials: HTTPBasicCredentials = Depends(check_auth)):
    input_file = f"/input/{request.file}"
    output_dir = "/output"

    # Vérifier si le fichier existe
    if not os.path.exists(input_file):
        raise HTTPException(status_code=400, detail="Le fichier spécifié n'existe pas")

    # Exécuter Spleeter via subprocess
    try:
        result = subprocess.run([
            "spleeter", "separate", "-p", "spleeter:5stems",
            "-o", output_dir, input_file
        ], capture_output=True, text=True, check=True)

        return {"message": "Traitement terminé", "file": request.file, "logs": result.stdout}

    except subprocess.CalledProcessError as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de l'exécution de Spleeter : {e.stderr}")
