from flask import Blueprint, request, jsonify
from src.services.storage_service import StorageService
from src.services.invoice_service import InvoiceService

# Crear un Blueprint para las rutas de facturas
factura_bp = Blueprint('factura', __name__)

storage_service = StorageService()
Invoices_service= InvoiceService()


@factura_bp.route('/hola', methods=['GET'])
def hola():
    return jsonify({'message': 'Hola mundo'})


@factura_bp.route('/get_invoices', methods=['GET'])
def get_invoice():
    
    try:
        get_invoice_db = Invoices_service.obtener_todas_facturas()
        return jsonify({"message": "Facturas encontradas", 
                        "url": get_invoice_db}), 200
    except Exception as e:
        return jsonify({"error": f"Error uploading file: {str(e)}"}), 500

@factura_bp.route('/upload_invoice', methods=['POST'])
def upload_blob():
    # Recibir los datos JSON desde la solicitud
    data = request.json

    # Obtener el archivo codificado en base64
    file_data = data.get("file")

    # Verificar si el archivo está presente
    if not file_data:
        return jsonify({"error": "Missing required data (file)"}), 400

    try:
        # Llamar al servicio para subir el archivo a Azure
        file_url = storage_service.upload_file_to_azure(file_data)
        
        return jsonify({"message": "File uploaded successfully", "url": file_url}), 200
    except Exception as e:
        return jsonify({"error": f"Error uploading file: {str(e)}"}), 500

@factura_bp.route('/get_blobs', methods=['GET'])
def get_blobs():
    try:
        # Llamar al servicio para subir el archivo a Azure
        blobs_list = storage_service.list_blobs()
        
        return jsonify({"message": "File uploaded successfully", "blobs": blobs_list}), 200
    except Exception as e:
        return jsonify({"error": f"Error uploading file: {str(e)}"}), 500
    
@factura_bp.route('/get_invoice_detaeil', methods=['POST'])    
def get_invoive_details():
    data = request.json
    id_invoice = data.get("invoice_detail_id")
    if not id_invoice:
        return jsonify({"error": "Missing required data (invoice_detail_id)"}), 400
    try:
        list_detail = Invoices_service.list_detail_invoice(id_invoice)
        return jsonify({"message": "Factura encontrada", "Details_invoice": list_detail}), 200
    except Exception as e:
        pass
    