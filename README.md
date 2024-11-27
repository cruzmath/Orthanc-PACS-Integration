# Orthanc-PACS-Integration

## Table of Contents
1. [Technologies Used](#technologies-used)
2. [Issues Encountered](#issues-encountered)
3. [Solutions to Issues](#solutions-to-issues)
4. [Knowledge Acquired](#knowledge-acquired)
5. [Project Phases](#project-phases)
   - [Phase 1: Creating and Running an Orthanc PACS Server on Docker](#phase-1-creating-and-running-an-orthanc-pacs-server-on-docker)
   - [Phase 2: Adding DICOM Files to the Server Using Python](#phase-2-adding-dicom-files-to-the-server-using-python)
   - [Phase 3: Data Classification Using a Pre-Trained Machine Learning Model](#phase-3-data-classification-using-a-pre-trained-machine-learning-model)
   - [Phase 4: Creating a DICOM SR (Structured Report) File](#phase-4-creating-a-dicom-sr-structured-report-file)

---

## Technologies Used

- **Docker**
- **Python Libraries**:
  - `requests` → Handles HTTP communication with the server.
  - `zipfile` → Reads ZIP files without extraction.
  - `io` → Reads DICOM files as bytes.
  - `torchxrayvision` → Provides pre-trained machine learning models.
  - `pydicom` → Reads and writes DICOM files.
  - `pathlib` → Enables handling file paths easily.
  - `json` → Creates and reads JSON files.
  - `re` → Simplifies string extraction.
  - `datetime` → Provides current date and time for DICOM SR metadata.

---

## Issues Encountered

1. File uploads to the server weren't persistent across restarts.
2. Although data persistence was achieved using a Docker volume, accessing files within the volume from another image was problematic.
3. Some `.dcm` files had double the maximum intensity supported by the `xrv.utils.read_xray_dcm` function.
4. Limited information available on creating DICOM SR files.
5. While creating the DICOM SR, the following error appeared:
> UserWarning: Invalid value for VR UI: '72682317.56696215.32367375.69516389.09416010'. Please see "https://dicom.nema.org/medical/dicom/current/output/html/part05.html#table_6.2-1" for allowed values for each VR.


---

## Solutions to Issues

1. Configured the volume to use the same path as the `StorageDirectory` defined in the `orthanc.json` file.
2. Specified the volume path in the Docker Compose file to allow shared access.
3. Used `pydicom` to preprocess the DICOM files and adjust pixel intensity before passing them to `torchxrayvision`.
4. Although no definitive solution for DICOM SR creation issues was found, research and experimentation with different tools helped clarify some aspects.
5. The exact cause of the VR UI error remains unknown. The issue might relate to the DICOM standard's strict rules, though the provided value appears to conform.

---

## Knowledge Acquired

Through this project, I gained:
- Practical experience in configuring Docker containers, images, and volumes, appreciating its benefits:
- Isolating virtual environments with required dependencies.
- Reducing local storage requirements by leveraging cloud storage.
- Hands-on understanding of applying pre-trained AI models for patient diagnostics using `.dcm` files.
- Knowledge of reading and writing `.dcm` files programmatically.
- Insights into server operations and REST API communication.

---

## Project Phases

### Phase 1: Creating and Running an Orthanc PACS Server on Docker

This phase involved setting up a Dockerized PACS server. Using an `orthanc.json` file, user accounts with remote access were configured. 

Steps:
1. Install Docker and follow the installation guide.
2. Create `docker-compose.yml` and `orthanc.json` files in the same directory.
3. Run the following command in the terminal:
```bash
docker-compose up -d
```
In which: 
* docker-compose manages the .yml file.
* up initializes the container.
* -d runs the container in detached mode.

### Phase 2: Adding DICOM Files to the Server Using Python
DICOM files were uploaded to the Orthanc server using a Python script (enviar_arquivos.py). These files were:

* Read as binary data to preserve integrity.
* Sent to the server via HTTP using the Orthanc REST API.
How to execute:

1. Place the .zip files in the designated folder.
2. Run the script while the server is operational.

### Phase 3: Data Classification Using a Pre-Trained Machine Learning Model
A script (classificar.py) was developed to classify the data:

Extract files from the Docker volume.
Read and preprocess the .dcm files.
Use the densenet121-res224-all model to diagnose and output results in a JSON format.
Execution Steps:

Create a Dockerfile specifying dependencies.
Build an image using:
```bash
docker build -t teste_xray_imagem .
```
-t: name the image with the following text.

Run the container with:
```bash
docker run --rm -v docker_teste_orthanc_db:/var/lib/orthanc/db teste_xray_imagem
```
--rm: Removes the container after execution.
-v: Maps the volume to share data between containers.

### Phase 4: Creating a DICOM SR (Structured Report) File
The criar_dicomsr.py script generates DICOM SR files:

* Reads results from resultados.json.
* Saves SR files to a local SR folder.
* Uploads them to the Orthanc server via its REST API.
How to execute:

* Place the script in the directory containing resultados.json.
* Run the script while the server is active.
> Note: The Orthanc server organizes files based on metadata, not folder structure. Ensure proper file metadata for correct categorization.
