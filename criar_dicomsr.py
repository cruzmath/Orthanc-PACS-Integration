from pydicom.dataset import Dataset, FileDataset
from pydicom.sr.coding import Code
from pydicom.uid import generate_uid, ExplicitVRLittleEndian
import json
import datetime
import re
import requests
from io import BytesIO
from requests.auth import HTTPBasicAuth
import os

json_results_path = 'resultados.json'
def create_dicom_sr(json_results_path:str)-> None:
    # Regex para extrair informações da chave
    pattern = re.compile(
        r'id_(?P<patient_id>[^\\]+)\\Study_(?P<study_instance_uid>[^\\]+)\\Series_(?P<series_instance_uid>[^\\]+)\\image-(?P<image_instance_uid>[^\\]+)'
    )
    # Lendo os resultados do arquivo json
    with open(json_results_path, 'r') as json_file:
        data = json.load(json_file)

    # Create a new DICOM dataset
    file_meta = Dataset()
    file_meta.MediaStorageSOPClassUID = '1.2.840.10008.5.1.4.1.1.88.22'  # SR Document
    file_meta.MediaStorageSOPInstanceUID = generate_uid()
    file_meta.TransferSyntaxUID = ExplicitVRLittleEndian

    # Copy relevant attributes from the original DICOM file
    for key, findings in data.items():
        match = pattern.match(key)
        if match:
            patient_id = match.group('patient_id')
            study_instance_uid = match.group('study_instance_uid')
            series_instance_uid = match.group('series_instance_uid')
            image_instance_uid = match.group('image_instance_uid')
            output_sr_path = f"SR/id_{patient_id}Study_{study_instance_uid}Series_{series_instance_uid}DICOM_SR.dcm"

            # Create the FileDataset instance
            ds = FileDataset(output_sr_path, {}, file_meta=file_meta, preamble=b"\0" * 128) #type: ignore

            ds.PatientID = patient_id
            ds.StudyInstanceUID = study_instance_uid
            ds.SeriesInstanceUID = series_instance_uid
            ds.SOPInstanceUID = = generate_uid()  # Gerar um novo UID para o SR para evitar conflitos

            # Set SR-specific attributes
            ds.SOPClassUID = file_meta.MediaStorageSOPClassUID
            ds.SOPInstanceUID = file_meta.MediaStorageSOPInstanceUID
            ds.Modality = 'SR'
            ds.ContentDate = datetime.date.today().strftime('%Y%m%d')
            ds.ContentTime = datetime.datetime.now().strftime('%H%M%S')

            # Create the SR content
            content_seq = Dataset()
            content_seq.ValueType = 'CONTAINER'
            #'12' - Indicates the "Findings" branch of the DICOM coding hierarchy
            #'1111' - Indicates a more specific concept within the "Findings" domain, in this case, the "AI Analysis Report"
             # Criando um Dataset para ConceptNameCodeSequence
            concept_name_code = Dataset()
            concept_name_code.CodeValue = '121111'
            concept_name_code.CodingSchemeDesignator = 'DCM'
            concept_name_code.CodeMeaning = 'AI Analysis Report'
            content_seq.ConceptNameCodeSequence = [concept_name_code] #precisa que a entrada seja um dataset

            content_seq.ContinuityOfContent = 'SEPARATE'

            template_seq = Dataset()
            template_seq.TemplateIdentifier = '2000'
            content_seq.ContentTemplateSequence = [template_seq] #precisa que a entrada seja um dataset
            
            content_seq.ContentSequence = []
            # Add AI results to the SR content
            for finding, value in findings.items():
                finding_item = Dataset()
                finding_item.RelationshipType = 'CONTAINS'
                finding_item.ValueType = 'TEXT'
                
                # Criando um Dataset para ConceptNameCodeSequence
                finding_concept = Dataset()
                #'12' - Indicates the "Findings" branch of the DICOM coding hierarchy, just like the '121111' code we discussed earlier.
                #'11' - This part of the code value suggests that this is a more specific type of "Finding" within the DICOM terminology.
                #'06' - Indicate that this is the 6th specific "Finding" concept defined within this branch of the DICOM coding scheme.
                finding_concept.CodeValue = '121106'
                finding_concept.CodingSchemeDesignator = 'DCM'
                finding_concept.CodeMeaning = 'Finding'
                finding_item.ConceptNameCodeSequence = [finding_concept]

                finding_item.TextValue = f"{finding}: {value}"
                content_seq.ContentSequence.append(finding_item)

            ds.ContentSequence = [content_seq]

            # Save the DICOM SR file
            ds.save_as(output_sr_path)

            print(f"DICOM SR file created successfully: {output_sr_path}")

def enviar_arquivos()-> None:
    orthanc_url = 'http://localhost:8042'
    auth = HTTPBasicAuth("matheus", "malia123")

    for file_name in os.listdir("SR"):
        # Verificar se o arquivo é um DICOM (por exemplo, extensão .dcm)
        if file_name.endswith('.dcm'):
            file_path = os.path.join("SR", file_name)

            # Ler o arquivo DICOM como bytes
            with open(file_path, 'rb') as dicom_file:
                dicom_bytes = dicom_file.read()
                
                # Enviar o arquivo DICOM para o Orthanc
                response = requests.post(f'{orthanc_url}/instances',
                                         files={'file': BytesIO(dicom_bytes)},
                                         auth=auth)

                # Verificar o código de status HTTP
                if response.status_code == 200:
                    try:
                        response_json = response.json()
                        print(f'Uploaded {file_name}:', response_json)
                    except requests.exceptions.JSONDecodeError:
                        print(f'Uploaded {file_name}, but the response is not in JSON format.')
                        print(f'Response content: {response.text}')
                else:
                    print(f'Failed to upload {file_name}. HTTP Status Code: {response.status_code}')
                    print(f'Response content: {response.text}')

create_dicom_sr(json_results_path)
enviar_arquivos()
