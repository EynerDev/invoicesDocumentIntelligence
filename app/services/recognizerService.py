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
            return None
        if hasattr(field, "value") and field.value is not None:
            return field.value
        if hasattr(field, "content") and field.content:
            return field.content
        return str(field)

    @staticmethod
    def analyze_invoice(path_url, id_invoice):
        endpoint = os.getenv("ENDPOINT_DOCUMENT_INTELLIGENCE")
        key = os.getenv("KEY_DOCUMENT_INTELLIGENCE")

        if not endpoint or not key:
            raise ValueError(
                "Debes configurar ENDPOINT_DOCUMENT_INTELLIGENCE y KEY_DOCUMENT_INTELLIGENCE en tu .env"
            )

        client = DocumentIntelligenceClient(
            endpoint=endpoint,
            credential=AzureKeyCredential(key)
        )

        poller = client.begin_analyze_document(
            "prebuilt-invoice", AnalyzeDocumentRequest(url_source=path_url)
        )
        result: AnalyzeResult = poller.result()

        for invoice in result.documents:
            data = {
                'vendor_address': DocumentIntelligence.get_field_value(invoice.fields, "VendorAddress"),
                'vendor_address_recipient': DocumentIntelligence.get_field_value(invoice.fields, "VendorAddressRecipient"),
                'customer_name': DocumentIntelligence.get_field_value(invoice.fields, "CustomerName"),
                'customer_id': DocumentIntelligence.get_field_value(invoice.fields, "CustomerId"),
                'customer_address': DocumentIntelligence.get_field_value(invoice.fields, "CustomerAddress"),
                'customer_address_recipient': DocumentIntelligence.get_field_value(invoice.fields, "CustomerAddressRecipient"),
                'invoice_id': DocumentIntelligence.get_field_value(invoice.fields, "InvoiceId"),
                'invoice_date': DocumentIntelligence.get_field_value(invoice.fields, "InvoiceDate"),
                'invoice_total': DocumentIntelligence.get_field_value(invoice.fields, "InvoiceTotal"),
                'due_date': DocumentIntelligence.get_field_value(invoice.fields, "DueDate"),
                'purchase_order': DocumentIntelligence.get_field_value(invoice.fields, "PurchaseOrder"),
                'billing_address': DocumentIntelligence.get_field_value(invoice.fields, "BillingAddress"),
                'billing_address_recipient': DocumentIntelligence.get_field_value(invoice.fields, "BillingAddressRecipient"),
                'shipping_address': DocumentIntelligence.get_field_value(invoice.fields, "ShippingAddress"),
                'shipping_address_recipient': DocumentIntelligence.get_field_value(invoice.fields, "ShippingAddressRecipient"),
                'subtotal': DocumentIntelligence.get_field_value(invoice.fields, "SubTotal"),
                'total_tax': DocumentIntelligence.get_field_value(invoice.fields, "TotalTax"),
                'previous_unpaid_balance': DocumentIntelligence.get_field_value(invoice.fields, "PreviousUnpaidBalance"),
                'amount_due': DocumentIntelligence.get_field_value(invoice.fields, "AmountDue"),
                'service_start_date': DocumentIntelligence.get_field_value(invoice.fields, "ServiceStartDate"),
                'service_end_date': DocumentIntelligence.get_field_value(invoice.fields, "ServiceEndDate"),
                'service_address': DocumentIntelligence.get_field_value(invoice.fields, "ServiceAddress"),
                'service_address_recipient': DocumentIntelligence.get_field_value(invoice.fields, "ServiceAddressRecipient"),
                'remittance_address': DocumentIntelligence.get_field_value(invoice.fields, "RemittanceAddress"),
                'remittance_address_recipient': DocumentIntelligence.get_field_value(invoice.fields, "RemittanceAddressRecipient"),
                'numero_contrato': DocumentIntelligence.get_field_value(invoice.fields, "Contrato"),
            }

        return {
            "invoice_data": data,
            "invoice_id": id_invoice
        }
