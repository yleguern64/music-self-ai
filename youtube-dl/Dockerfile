FROM python:3.10-slim

# Installer FFmpeg et youtube-dl
RUN apt-get update && apt-get install -y ffmpeg && rm -rf /var/lib/apt/lists/*
RUN pip install --upgrade pip setuptools wheel yt-dlp fastapi uvicorn

# Copier l'API
WORKDIR /app
COPY app.py .

# Exposer le port pour l'API
EXPOSE 8000

# Démarrer l'API au lancement
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
