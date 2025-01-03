from flask import Blueprint, request, jsonify
from services.storage_service import StorageService
from services.invoice_service import InvoiceService

# Crear un Blueprint para las rutas de facturas
factura_bp = Blueprint('factura', __name__)

storage_service = StorageService()
invoices_service= InvoiceService()


@factura_bp.route('/hola', methods=['GET'])
def hola():
    return jsonify({'message': 'Hola mundo'})



@factura_bp.route('/upload_invoice', methods=['POST'])
def upload_blob():
    # Recibir el archivo codificado en base64 desde la solicitud
    file_data = request.json.get("file")
    if not file_data:
        return jsonify({"error": "No file provided"}), 400

    try:
        # Llamar al servicio para subir el archivo a Azure
        file_url = storage_service.upload_file_to_azure(file_data)
        data = {
                "type_id": 1,
                "provider_id": 1,
                "path_storage": file_url
            }
        
        invoices_service.agregar_factura(data)
        return jsonify({"message": "File uploaded successfully", "url": file_url}), 200
    except Exception as e:
        return jsonify({"error": f"Error uploading file: {str(e)}"}), 500
