from azure.storage.blob import BlobServiceClient, BlobSasPermissions, generate_blob_sas
from azure.core.exceptions import ResourceExistsError
from dotenv import load_dotenv
from datetime import datetime, timedelta
import os
import base64
import time

# Cargar las variables de entorno desde un archivo .env
load_dotenv()

class StorageService:
    def __init__(self):
        # Usar la cadena de conexión de la cuenta de almacenamiento de Azure
        self.connection_string = os.getenv("KEY_STORAGE_ACCOUNT")  # Asegúrate de que esta variable esté en tu .env
        if not self.connection_string:
            raise ValueError("La cadena de conexión no está definida en el archivo .env")

        # Crear un cliente del servicio de blobs
        self.blob_service_client = BlobServiceClient.from_connection_string(self.connection_string)

        # Nombre del contenedor
        self.container_name = "invoices"
        
        # Crear o acceder al contenedor
        self.container_client = self.blob_service_client.get_container_client(self.container_name)
        try:
            self.container_client.create_container()  # Si el contenedor no existe, lo crea
            print(f"Contenedor '{self.container_name}' creado con éxito.")
        except ResourceExistsError:
            print(f"El contenedor '{self.container_name}' ya existe.")
        except Exception as e:
            raise Exception(f"Error al crear o acceder al contenedor: {str(e)}")

    import base64


    def upload_file_to_azure(self, file_data):
        # Decodificar el archivo Base64
        try:
            decoded_file = base64.b64decode(file_data)
        except Exception as e:
            raise ValueError(f"Error decodificando el archivo: {str(e)}")

        # Crear un nombre único para el archivo en el contenedor
        blob_name = f"factura_{int(time.time())}.pdf"

        # Crear el cliente del blob
        blob_client = self.container_client.get_blob_client(blob_name)

        # Subir el archivo decodificado al contenedor de Azure
        try:
            blob_client.upload_blob(decoded_file, overwrite=True)
            print(f"Archivo subido con éxito: {blob_name}")
            
            # Generar y devolver la URL con SAS
            account_name = self.blob_service_client.account_name
            blob_url, sas_token = self.generate_token_sas(account_name, blob_name)
            return {"url_blob" : blob_client.url ,
                    "blob_url_sas": blob_url, 
                    "sas_token": sas_token}
        except Exception as e:
            raise Exception(f"Error subiendo el archivo a Azure: {str(e)}")

    def generate_token_sas(self, storage_account_name, blob_name):
        # Extraer el account key desde la cadena de conexión
        account_key = os.getenv("ACCOUNT_KEY")
        
        # Configurar la duración del token SAS
        sas_expiry = datetime.utcnow() + timedelta(hours=2)  # Expira en 2 horas

        # Generar el token SAS para un blob específico
        sas_token = generate_blob_sas(
            account_name=storage_account_name,
            account_key=account_key,
            container_name=self.container_name,
            blob_name=blob_name,
            permission=BlobSasPermissions(read=True),
            expiry=sas_expiry
        )

        # Construir la URL completa del blob con el token SAS
        blob_url = f"https://{storage_account_name}.blob.core.windows.net/{self.container_name}/{blob_name}?{sas_token}"
        return blob_url, sas_token
