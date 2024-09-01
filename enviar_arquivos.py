import zipfile
import requests
from io import BytesIO
from requests.auth import HTTPBasicAuth

# Definindo a URL do Orthanc e as credenciais de autenticação
orthanc_url = 'http://localhost:8042'
# Se a segurança for um elemento necessário para a sua situação, 
# pode ser necessário o uso de variáveis de ambiente ao invés de deixar elas explícitas, 
# mas como esse é um projeto simples e local, não julguei necessário
auth = HTTPBasicAuth("matheus", "malia123")

# Caminho para o arquivo zip que contém as pastas e os arquivos DICOM
zip_file_path = 'dicom_samples.zip'

# A sequência de códigos abaixo já possibilita o envio dos arquivos DICOM sem a necessidade de extrair o zip
# Abrir o arquivo zip
with zipfile.ZipFile(zip_file_path, 'r') as zip_file:
    # Iterar sobre todos os arquivos dentro do zip
    for file_name in zip_file.namelist():
        # Verificar se o arquivo é um DICOM (por exemplo, extensão .dcm)
        if file_name.endswith('.dcm'):
            # Ler o arquivo DICOM como bytes
            with zip_file.open(file_name) as dicom_file:
                dicom_bytes = dicom_file.read()

                # Enviar o arquivo DICOM para o Orthanc
                response = requests.post(f'{orthanc_url}/instances',
                                         files={'file': BytesIO(dicom_bytes)},
                                         auth=auth)
                
                # Exibir a resposta
                print(f'Uploaded {file_name}:', response.json())