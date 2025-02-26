FROM python:3.10-slim

# Installer FFmpeg (nécessaire pour Spleeter)
RUN apt-get update && apt-get install -y ffmpeg && rm -rf /var/lib/apt/lists/*

# Mettre à jour pip et installer les dépendances manuelles
RUN pip install --upgrade pip setuptools wheel

# Installer FastAPI et Uvicorn
RUN pip install fastapi uvicorn

# Installer une version compatible de NumPy (NumPy 1.x)
RUN pip install "numpy<2"

# Installer TensorFlow compatible
RUN pip install "tensorflow<2.15" "tensorflow-probability<0.24"

# Installer Spleeter
RUN pip install spleeter

# Copier l'API
WORKDIR /app
COPY app.py .

# Exposer le port pour l'API
EXPOSE 8000

# Démarrer l'API au lancement
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
