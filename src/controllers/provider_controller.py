from flask import Blueprint, request, jsonify
from services.provider_service import ProviderService

# Crear un Blueprint para las rutas de facturas
provider_bp = Blueprint('provider', __name__)

provider_service = ProviderService()


@provider_bp.route('/get_providers', methods=['GET'])
def get_providers():
    
    try:
        get_providers = provider_service.obtener_proveedores()
        return jsonify({"message": "Proveedores encontrados", "data": get_providers}), 200
    except Exception as e:
         return jsonify({"error": f"Error: {str(e)}"}), 500

@provider_bp.route('/create_providers', methods=['POST'])
def upload_blob():
    # Recibir los datos JSON desde la solicitud
    data = request.json

    try:
        # Llamar al servicio para subir el archivo a Azure
        new_provider = provider_service.create_provider(data)
        
        return jsonify({"message": "Proveedor creado de forma exitosa ", "data": new_provider}), 200
    except Exception as e:
        return jsonify({"error": f"Error al crear el proveedor: {str(e)}"}), 500

@provider_bp.route('/get_blobs', methods=['GET'])
def get_blobs():
    try:
        # Llamar al servicio para subir el archivo a Azure
        blobs_list = storage_service.list_blobs()
        
        return jsonify({"message": "File uploaded successfully", "blobs": blobs_list}), 200
    except Exception as e:
        return jsonify({"error": f"Error uploading file: {str(e)}"}), 500
    
@provider_bp.route('/get_invoice_detaeil', methods=['POST'])    
def get_invoive_details():
    data = request.json
    id_invoice = data.get("invoice_detail_id")
    if not id_invoice:
        return jsonify({"error": "Missing required data (invoice_detail_id)"}), 400
    try:
        list_detail = invoices_service.list_detail_invoice(id_invoice)
        return jsonify({"message": "Factura encontrada", "Details_invoice": list_detail}), 200
    except Exception as e:
        pass
    