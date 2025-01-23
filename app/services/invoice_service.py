from Models.invoicesModel import InvoicesModel
from database.conn import session

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


    # @staticmethod
    # def agregar_factura(type_id, provider_id, path_storage,blob_sas, name_invoice ):
    #     try:
    #         logging.info("Creando nueva factura...")
    #         new_invoice = InvoicesModel(
    #             type_id=type_id,
    #             provider_id=provider_id,
    #             path_storage=path_storage,
    #             blob_sas=blob_sas,
    #             name_invoice=name_invoice
    #         )
    #         logging.info(f"Factura creada: {new_invoice}")
            
    #         session.add(new_invoice)
    #         session.commit()
            
    #         return {
    #             "msg": "Factura cargada en la base de datos de manera exitosa",
    #             "statusCode": 200
    #         }
    #     except Exception as e:
    #         logging.error(f"Error al agregar la factura: {e}")
    #         return {
    #             "msg": f"Error al agregar la factura: {e}",
    #             "statusCode": 500
    #         }