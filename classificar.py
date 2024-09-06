import torch, torchvision
import torchxrayvision as xrv
from pathlib import Path
import requests
from requests.auth import HTTPBasicAuth
import os
import pydicom

# Função para coletar os DICOMs da API do Orthanc, primeira solução utilizada
def coletar_dcms_api() -> list[str]:
  orthanc_url = 'http://orthanc:8042'
  auth = HTTPBasicAuth("matheus", "malia123")
  dcm_path_list = []
  i = 0

  # Obter a lista de estudos
  response = requests.get(f'{orthanc_url}/studies', auth=auth)
  studies = response.json()

  # iterando sobre cada estudo
  for study_id in studies:
    response = requests.get(f'{orthanc_url}/studies/{study_id}/series', auth=auth)
    series = response.json()

    # iterando sobre cada série dentro de cada estudo
    for serie in series:
      series_id = serie['ID']
      response = requests.get(f'{orthanc_url}/series/{series_id}/instances', auth=auth)
      instance_id = response.json()[0]['ID'] # coletando apenas o ID da instância

      # Baixar o arquivo DICOM do Orthanc
      response = requests.get(f'{orthanc_url}/instances/{instance_id}/file', auth=auth)

      # Caminho onde o arquivo será salvo
      dcm_path = Path(f"/app/temp{i}.dcm")
      dcm_path_list.append(dcm_path)

      # Salvar o arquivo DICOM no sistema de arquivos local
      with open(dcm_path, 'wb') as f:
          f.write(response.content)
      i +=1
  return dcm_path_list
# lista_pastas = coletar_dcms_api()

# Especificar o caminho do arquivo DICOM usando pathlib
dcm_folder = "/var/lib/orthanc/db"

# Função para listar todos os arquivos de uma pasta
def listar_arquivos_dcm(diretorio: str) -> list[str]:
  todos_caminhos = []
  for root, dirs, files in os.walk(diretorio):
    for file in files:
      todos_caminhos.append(os.path.join(root, file))
  # Como os arquivos não aparecem com extensão no docker, usei o critério de ter um nome longo, visto que isso implica um maior caminho o que seria equivalente ao documento.
  min_length = 50

  # Filtrar os caminhos com base no comprimento
  caminhos_dcm = [path for path in todos_caminhos if len(path) > min_length]
  return caminhos_dcm

lista_pastas = listar_arquivos_dcm(dcm_folder)
dict_resultados = {}
# Iterar sobre todos os arquivos na pasta
for dcm_path in lista_pastas:
  try:
    # Carregar a imagem DICOM como um objeto pydicom
    dicom_data = pydicom.dcmread(dcm_path)

    # Extrair informações do DICOM
    patient_id = dicom_data.PatientID
    study_id = dicom_data.StudyInstanceUID
    series_id = dicom_data.SeriesInstanceUID
    image_id = dicom_data.SOPInstanceUID

    # montando um caminho com as informações acima para salvar nos resultados como um identificador
    caminho = fr"{patient_id}\Study_{study_id}\Series_{series_id}\image-{image_id}"
    
    # Extrair a imagem como um array numpy
    dcm_image = dicom_data.pixel_array
    
    # Verificar o valor máximo da imagem
    max_pixel_value = dcm_image.max()
    
    # Ajustar o valor de maxval com base no valor máximo da imagem
    if max_pixel_value <= 4095:
        maxval = 4096
    elif max_pixel_value <= 8191:
        maxval = 8192
    else:
        raise Exception(f"Valor máximo inesperado: {max_pixel_value} em {dcm_path}")
    
    # Normalizar a imagem para a faixa [-1024, 1024]
    dcm_image = xrv.datasets.normalize(dcm_image, maxval)
    
    # Se a imagem tiver apenas 2 dimensões (escala de cinza), adicione a dimensão do canal
    if len(dcm_image.shape) == 2:
        dcm_image = dcm_image[None, :, :] 
    
    # Aplicar transformações
    transform = torchvision.transforms.Compose([
        xrv.datasets.XRayCenterCrop(), 
        xrv.datasets.XRayResizer(224)
    ])
    
    dcm_image = transform(dcm_image)
    
    # Converter a imagem para tensor PyTorch
    dcm_image_tensor = torch.from_numpy(dcm_image).float()
    
    # Adicionar uma dimensão adicional para batch (necessário para o modelo)
    dcm_image_tensor = dcm_image_tensor.unsqueeze(0)
    
    # Carregar o modelo pré-treinado
    model = xrv.models.DenseNet(weights="densenet121-res224-all")
    
    # Computar as saídas do modelo
    outputs = model(dcm_image_tensor)
    
    # Converter os resultados em um dicionário com as patologias e suas respectivas probabilidades
    resultados = dict(zip(model.pathologies, outputs[0].detach().numpy()))

    # adicionando o identificador de cada resultado
    dict_resultados[caminho] = resultados

  except Exception as e:
    print(f"Erro ao processar {dcm_path}: {e}")

# Exibir os resultados
print(dict_resultados)
