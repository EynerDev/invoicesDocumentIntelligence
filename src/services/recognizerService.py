from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.ai.documentintelligence.models import AnalyzeResult, AnalyzeDocumentRequest
from azure.core.credentials import AzureKeyCredential
from dotenv import load_dotenv
import os

# Cargar variables de entorno
load_dotenv()

class DocumentIntelligence:  
    @staticmethod
    def get_field_value(fields, key):
        field = fields.get(key)
        if not field:
            return ""
        if hasattr(field, "value") and field.value is not None:
            return field.value
        if hasattr(field, "content") and field.content:
            return field.content
        return str(field)

    @staticmethod
    def analyze_invoice(path_url, id_invoice):
        endpoint = os.getenv("ENDPOINT_DOCUMENT_INTELLIGENCE")
        key = os.getenv("KEY_DOCUMENT_INTELLIGENCE")
        modelID  = "Model-Public-Services"
        if not endpoint or not key:
            raise ValueError(
                "Debes configurar ENDPOINT_DOCUMENT_INTELLIGENCE y KEY_DOCUMENT_INTELLIGENCE en tu .env"
            )

        client = DocumentIntelligenceClient(
            endpoint=endpoint,
            credential=AzureKeyCredential(key)
        )

        poller = client.begin_analyze_document(
            modelID, AnalyzeDocumentRequest(url_source=path_url)
        )
        result: AnalyzeResult = poller.result()

        for invoice in result.documents:
            data = {
                'Proveedor': DocumentIntelligence.get_field_value(invoice.fields, "ProovedorServicio"),
                'Nit_proveedor': DocumentIntelligence.get_field_value(invoice.fields, "NitProveedor"),
                'Fecha_Ultimo_Pago': DocumentIntelligence.get_field_value(invoice.fields, "FechaUltimoPago"),
                'Direccion_Residencia': DocumentIntelligence.get_field_value(invoice.fields, "DirecionResidencia"),
                'Valor_Ultimo_Pago': DocumentIntelligence.get_field_value(invoice.fields, "ValorUltimoPago"),
                'Total_A_Pagar': DocumentIntelligence.get_field_value(invoice.fields, "Total_pagar"),
                'Fecha_Limite_pago': DocumentIntelligence.get_field_value(invoice.fields, "FechaLimitePago"),
                'Fecha_Emision_factura': DocumentIntelligence.get_field_value(invoice.fields, "FechaEmisionFactura"),
                'Subtotal': DocumentIntelligence.get_field_value(invoice.fields, "Subtotal"),
                'Deuda': DocumentIntelligence.get_field_value(invoice.fields, "Deuda"),
                'N° Contrato': DocumentIntelligence.get_field_value(invoice.fields, "#Contrato"),
                'Mes_Facturaacion': DocumentIntelligence.get_field_value(invoice.fields, "MesFacturacion"),
                'Cupon_Pago': DocumentIntelligence.get_field_value(invoice.fields, "CuponPago")
            }

        return {
            "invoice_data": data,
            "invoice_id": id_invoice
        }
