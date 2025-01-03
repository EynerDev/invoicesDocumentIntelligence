from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
from dotenv import load_dotenv
from azure.core.exceptions import ResourceExistsError

import os
import base64
import time

# Cargar las variables de entorno desde un archivo .env
load_dotenv()

class StorageService:
    def __init__(self):
        # Usar la cadena de conexión de la cuenta de almacenamiento de Azure
        self.connection_string = os.getenv("KEY_STORAGE_ACCOUNT")   # Asegúrate de que esta variable esté en tu .env
        if not self.connection_string:
            raise ValueError("La cadena de conexión no está definida en el archivo .env")

        # Crear un cliente del servicio de blobs
        self.blob_service_client = BlobServiceClient.from_connection_string(self.connection_string)

        # Nombre del contenedor
        self.container_name = "invoices"
        
        # Crear o acceder al contenedor
        self.container_client = self.blob_service_client.get_container_client(self.container_name)
        
        # Crear el contenedor si no existe
        try:
            self.container_client.create_container()  # Si el contenedor no existe, lo crea
            print(f"Contenedor '{self.container_name}' creado con éxito.")
        except ResourceExistsError:
            print(f"El contenedor '{self.container_name}' ya existe.")
        except Exception as e:
            raise Exception(f"Error al crear o acceder al contenedor: {str(e)}")

    def upload_file_to_azure(self, file_data):
        # Decodificar el archivo Base64
        try:
            decoded_file = base64.b64decode(file_data)
        except Exception as e:
            raise ValueError(f"Error decodificando el archivo: {str(e)}")

        # Crear un nombre único para el archivo en el contenedor
        blob_name = "factura_" + str(int(time.time())) + ".pdf"  # O el tipo de archivo que estés subiendo

        # Crear el cliente del blob
        blob_client = self.container_client.get_blob_client(blob_name)

        # Subir el archivo decodificado al contenedor de Azure
        try:
            blob_client.upload_blob(decoded_file, overwrite=True)
            print(f"Archivo subido con éxito: {blob_name}")
            return blob_client.url  # Retorna la URL del archivo subido
        except Exception as e:
            raise Exception(f"Error subiendo el archivo a Azure: {str(e)}")


