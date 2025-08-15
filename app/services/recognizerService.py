from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.ai.documentintelligence.models import AnalyzeResult
from azure.ai.documentintelligence.models import AnalyzeDocumentRequest
from azure.core.credentials import AzureKeyCredential

from dotenv import load_dotenv
import os

# Cargar variables de entorno
load_dotenv()

class DocumentIntelligence:

    @staticmethod
    def analyze_invoice(path_url, id_invoice):
        endpoint = os.getenv("ENDPOINT_DOCUMENT_INTELLIGENCE")
        key = os.getenv("KEY_DOCUMENT_INTELLIGENCE")

        if not endpoint or not key:
            raise ValueError("Debes configurar ENDPOINT_DOCUMENT_INTELLIGENCE y KEY_DOCUMENT_INTELLIGENCE en tu .env")

        document_intelligence_client = DocumentIntelligenceClient(
        endpoint=endpoint, credential=AzureKeyCredential(key))

        poller = document_intelligence_client.begin_analyze_document(
            "prebuilt-invoice", AnalyzeDocumentRequest(url_source=path_url
        ))

        result: AnalyzeResult = poller.result()
        print("Estamos aqui")

        invoice_data = []
        id_invoice = id_invoice
        for invoice in result.documents:
            # Preparar diccionario de factura
            data = {
                

                'vendor_address' : invoice.fields.get("VendorAddress"),
                'vendor_address_recipient' : invoice.fields.get("VendorAddressRecipient"),
                'customer_name' : invoice.fields.get("CustomerName"),
                'customer_id' : invoice.fields.get("CustomerId"),
                'customer_address' : invoice.fields.get("CustomerAddress"),
                'customer_address_recipient' : invoice.fields.get("CustomerAddressRecipient"),
                'invoice_id' : invoice.fields.get("InvoiceId"),
                'invoice_date' : invoice.fields.get("InvoiceDate"),
                'invoice_total' : invoice.fields.get("InvoiceTotal"),
                'due_date' : invoice.fields.get("DueDate"),
                'purchase_order' : invoice.fields.get("PurchaseOrder"),
                'billing_address': invoice.fields.get("BillingAddress"),
                'billing_address_recipient': invoice.fields.get("BillingAddressRecipient"),
                'shipping_address': invoice.fields.get("ShippingAddress"),
                'shipping_address_recipient' : invoice.fields.get("ShippingAddressRecipient"),
                'subtotal' : invoice.fields.get("SubTotal"),
                'total_tax' : invoice.fields.get("TotalTax"),
                'previous_unpaid_balance' : invoice.fields.get("PreviousUnpaidBalance"),
                'amount_due' : invoice.fields.get("AmountDue"),
                'service_start_date' : invoice.fields.get("ServiceStartDate"),
                'service_end_date' : invoice.fields.get("ServiceEndDate"),
                'service_address' : invoice.fields.get("ServiceAddress"),
                'service_address_recipient' : invoice.fields.get("ServiceAddressRecipient"),
                'remittance_address' : invoice.fields.get("RemittanceAddress"),
                'remittance_address_recipient' : invoice.fields.get("RemittanceAddressRecipient"),
                'numero_contrato' : invoice.fields.get("Contrato")
            }
            invoice_data.append(data)
            print(invoice_data)
            print(id_invoice)
        return invoice_data, id_invoice
    

