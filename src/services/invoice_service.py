from Models.invoicesModel import InvoicesModel
from Models.invoicesDetailModel import InvoiceDetailsModels
from services.invoice_details_service import DetailsDocumentIntelligence
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
                "data": [factura.__repr__() for factura in facturas],  # Mejor usar un método to_dict en el modelo
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
    def agregar_factura(type_id, path_storage,
                    name_invoice):
        try:
     
            # Crear la nueva factura, pasando los datos necesarios
            ReconizerService = DocumentIntelligence()
            InvoiceDetailsService = DetailsDocumentIntelligence()

            new_invoice = InvoicesModel(
                type_id=type_id,
                path_storage=path_storage,
                name_invoice=name_invoice,
            )  # Asegúrate de que los campos coinciden con el modelo
            print(new_invoice.name_invoice)
            session.add(new_invoice)
            session.commit()
            session.refresh(new_invoice)
            
            id_invoice = InvoiceService.getInvoiceNombre(name_invoice)
            result = ReconizerService.analyze_invoice(path_storage, id_invoice)
             
            data = result["invoice_data"]
            id = result["invoice_id"]
             
            detalles = InvoiceDetailsService.agregar_detalle_factura(data, id)
            
            print("esta es la data de la factura", result["invoice_data"])
            print("este es el id de la factura", result["invoice_id"])

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
    def getInvoiceNombre(name_invoice):
        try:
         
            invoice = session.query(InvoicesModel).filter(
                InvoicesModel.name_invoice == name_invoice,
                InvoicesModel.active == 1
            ).first()
            return invoice.id if invoice else None
        except Exception as e:
            return {
                "msg": f"Error al encontrar la factura con ese nombre: {str(e)}",
                "statusCode": 500
            }

    @staticmethod
    def list_detail_invoice(id_invoice):
        try:

            validate_invoice_id = InvoiceService.validate_invoice_active_id(id_invoice)
            if not validate_invoice_id:
                raise AssertionError("¡ERROR! no fue encontrada una factura con ese ID")

            facturas_details = session.query(InvoiceDetailsModels).filter(
                InvoiceDetailsModels.id_invoice == id_invoice,
                InvoiceDetailsModels.active == 1
            ).first()
            
            if not facturas_details:
                return {
                    "message": "No existen detalles registrados con este id de factura",
                    "statusCode": 200
                }
            else:
                return {
                    "message": "Informacion de Factura",
                    "data": [facturas_details.__repr__()],
                    "statusCode": 200
                }

        except Exception as e:
            return {
                "message": f"Error al cargar los datos de la factura: {e}",
                "statusCode": 500
            }

    @staticmethod
    def validate_invoice_active_id(id_invoice):
        try:
            active = session.query(InvoicesModel).filter(
                InvoicesModel.id == id_invoice,
                InvoicesModel.active == 1
            ).first()
            return active
        except Exception as e:
            return False
