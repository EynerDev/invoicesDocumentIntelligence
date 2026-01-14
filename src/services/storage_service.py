from azure.storage.blob import BlobServiceClient, BlobSasPermissions, StandardBlobTier , generate_blob_sas
from azure.core.exceptions import ResourceExistsError
from dotenv import load_dotenv
from datetime import datetime, timedelta
from services.invoice_service import InvoiceService
import os
import base64
import time
import json

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

    def upload_file_to_azure(self, file_data):
        try:
            # Verificar que los parámetros necesarios estén en los datos
            
            if not file_data:
                raise ValueError("Faltan parámetros necesarios: 'file_data', 'type_id' o 'provider_id'")

            # Decodificar el archivo Base64
            decoded_file = base64.b64decode(file_data)

            # Crear un nombre único para el archivo en el contenedor
            blob_name = f"factura_{int(time.time())}.pdf"

            # Crear el cliente del blob
            blob_client = self.container_client.get_blob_client(blob_name)

            # Subir el archivo decodificado al contenedor de Azure
            blob_client.upload_blob(decoded_file, overwrite=True)
            print(f"Archivo subido con éxito: {blob_name}")

            # Generar y devolver la URL con SAS
            account_name = self.blob_service_client.account_name
            print("Esta es la account_name: ", account_name)
            
            blob_url, blob_sas = self.generate_token_sas(
                storage_account_name=account_name,
                container_name=self.container_name,
                blob_name=blob_name
            ) 

            # Llamar al servicio de facturas para agregar la factura a la base de datos
            invoice_service = InvoiceService()
            result = invoice_service.agregar_factura(
                type_id=1,
                path_storage=blob_url,
                name_invoice=blob_name,
                )

            # Retornar la respuesta final
            return {
                "result": result,
                "url_blob": blob_client.url,
                "blob_url_sas": blob_url,
                "blob_name": blob_name,
            }

        except Exception as e:
            raise Exception(f"Error al subir o procesar el archivo: {str(e)}")

    def generate_token_sas(self, storage_account_name, container_name, blob_name):
        # Extraer el account key desde la cadena de conexión
        account_key = os.getenv("ACCOUNT_KEY")
        
        # Configurar la duración del token SAS
        sas_expiry = datetime.utcnow() + timedelta(hours=2)  # Expira en 2 horas

        # Generar el token SAS para un blob específico
        sas_token = generate_blob_sas(
            account_name=storage_account_name,
            container_name=container_name,
            blob_name=blob_name,
            account_key=account_key,
            permission=BlobSasPermissions(read=True),
            expiry=sas_expiry
        )

        # Construir la URL completa del blob con el token SAS
        blob_url = f"https://{storage_account_name}.blob.core.windows.net/{self.container_name}/{blob_name}?{sas_token}"
        return blob_url, sas_token

    def list_blobs(self):       
        try:
            blobs = self.container_client.list_blobs()
            print(blobs)
            for blob in blobs:
                blob_client = self.container_client.get_blob_client(blob.name)

                blobs_info = {
                    "name": blob.name,
                    "blob_type": blob.blob_type,
                    "blob_url": blob_client.url
                }     
                       
            if not blobs_info:
                print("No hay blobs en el contenedor")
        except Exception as e:
            print(f"An error occurred: {e}")
            
        return blobs_info