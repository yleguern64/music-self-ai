FROM python:3.10-slim

# Installer FFmpeg (nécessaire pour Demucs)
RUN apt-get update && apt-get install -y ffmpeg && rm -rf /var/lib/apt/lists/*

# Mettre à jour pip et installer les dépendances manuelles
RUN pip install --upgrade pip setuptools wheel

# Installer FastAPI et Uvicorn
RUN pip install fastapi uvicorn

# Installer NumPy compatible
RUN pip install "numpy<2"

# Installer Torch + Demucs
RUN pip install torch torchaudio torchvision
RUN pip install demucs

# Copier l'API
WORKDIR /app
COPY app.py .

# Exposer le port pour l'API
EXPOSE 8000

# Démarrer l'API au lancement
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
