from Models.invoicesModel import InvoicesModel
from Models.invoicesDetailModel import InvoiceDetailsModels
from services.recognizerService import DocumentIntelligence
from database.conn import session
import json

class InvoiceService:
    
    @staticmethod
    def obtener_todas_facturas():
        try:
            # Obtener todas las facturas de la base de datos
            facturas = session.query(InvoicesModel).all()
            
            # Si no hay facturas, devolver un mensaje adecuado
            if not facturas:
                return {
                    "msg": "No se encontraron facturas",
                    "statusCode": 404
                }
            
            # Devolver las facturas encontradas
            return {
                "msg": "Facturas obtenidas con éxito",
                "data": [factura.__repr__() for factura in facturas],  # Asegúrate de tener un método to_dict en el modelo
                "statusCode": 200
            }
        except Exception as e:
            # Si ocurre un error al acceder a la base de datos, capturarlo
            session.rollback()  # Deshacer cualquier transacción no confirmada
            return {
                "msg": f"Error al obtener las facturas: {str(e)}",
                "statusCode": 500
            }

    @staticmethod
    def agregar_factura(type_id, provider_id, path_storage,  blob_sas ,name_invoice):
        try:
            # Crear la nueva factura, pasando los datos necesarios
            ReconizerService = DocumentIntelligence()
            
            ReconizerService.analyze_invoice(path_storage)
            new_invoice = InvoicesModel(
                        type_id = type_id,
                        provider_id = provider_id ,
                        path_storage = path_storage,
                        blob_sas = blob_sas,
                        name_invoice = name_invoice,
            )  # Asegúrate de que los campos de 'data' coinciden con el modelo
            session.add(new_invoice)
            session.commit()
            
            return {
                "msg": "Factura cargada en la base de datos de manera exitosa",
                "statusCode": 200
            }
            
        except Exception as e:
            session.rollback()  # Revertir cualquier cambio en caso de error
            return {
                "msg": f"Error al agregar la factura: {str(e)}",
                "statusCode": 500
            }


    @staticmethod
    def list_detail_invoice(id_invoice):
        try:  
            print("eyner ")
            validate_invoice_id = InvoiceService.validate_invoice_active_id(id_invoice)
            print("eyner no sale")
            if not validate_invoice_id:
                raise AssertionError("¡ERROR! no fue encontrada una factura con ese ID")
            
            facturas_details = session.query(InvoiceDetailsModels).filter(
                InvoiceDetailsModels.id_invoice == id_invoice,
                InvoiceDetailsModels.active == 1
            ).all()
            
            return {
                "msg": "Informacion de Factura",
                "data" : [factura.__repr__() for factura in facturas_details],
                "statusCode": 200
            }
            
        except Exception as e:         
            return {
                "msg": f"Error al cargar los datos de la factura: {e}",
                "statusCode": 500
            }
            
    @staticmethod
    def validate_invoice_active_id(id_invoice):
        print("eyner no sale la funcion")
        try:
            active = session.query(InvoicesModel).filter(
                InvoicesModel.id == id_invoice,
                InvoicesModel.active == 1
                    
            ).all()
            return active
        except Exception as e:
            return False