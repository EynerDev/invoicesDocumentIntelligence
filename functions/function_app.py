import os, logging, sys
import azure.functions as func

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from src.services.storage_service import StorageService


app = func.FunctionApp()
@app.function_name(name="ProcessInvoice")
@app.blob_trigger(arg_name="blob",
                  path="invoices/{name}",
                  connection="AzureWebJobsStorage")
def process_invoice(blob: func.InputStream):
    storage_service = StorageService()
    blob_name = blob.name
    
    account_name = os.getenv("STORAGE_ACCOUNT_NAME")
    
    sas_token  = storage_service.generate_token_sas(account_name,blob_name)
    #Aquí llamas tu lógica (ej: analizar con Document Intelligence)
    logging.info(
        f"Factura detectada en Blob: {blob.name}, tamaño: {blob.length} bytes, Token: {sas_token}")
    