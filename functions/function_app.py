import os, logging
import azure.functions as func

from recognizerService import DocumentIntelligence
from storage_service import StorageService


app = func.FunctionApp()
@app.function_name(name="ProcessInvoice")
@app.blob_trigger(arg_name="blob",
                  path="invoices/{name}",
                  connection="AzureWebJobsStorage")
def process_invoice(blob: func.InputStream):
    
    storage_service = StorageService()
    document_intelligence = DocumentIntelligence()
    
    blob_name = blob.name.split("/", 1)[1] 
    container_name="invoices"
    account_name = os.getenv("STORAGE_ACCOUNT_NAME")
    
    sas_url, sas_token  = storage_service.generate_token_sas(account_name, container_name,blob_name)
    
    blob_url = f"https://{account_name}.blob.core.windows.net/{container_name}/{blob_name}?{sas_token}"
    
    result = document_intelligence.analyze_invoice(blob_url)
    data = result["invoice_data"]
    
    print(f"data: {data}")
    print(f"url {blob_url}")
    print(f"sas_toke {sas_token}")
    #Aquí llamas tu lógica (ej: analizar con Document Intelligence)
    logging.info(
        f"Factura detectada en Blob: {blob.name}, tamaño: {blob.length} bytes, Token: {sas_token}")
    