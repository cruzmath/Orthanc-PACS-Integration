# Use uma imagem base oficial do Python
FROM python:3.11-slim

# Instale dependências do sistema
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Instale PyTorch e TorchXRayVision
RUN pip install --no-cache-dir torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
RUN pip install --no-cache-dir torchxrayvision scikit-image pydicom
RUN pip install requests

# Crie o diretório de trabalho
WORKDIR /app

# Copiar os arquivos da pasta atual
COPY . /app 

# Comando para rodar o script Python
CMD ["python", "classificar.py"]
