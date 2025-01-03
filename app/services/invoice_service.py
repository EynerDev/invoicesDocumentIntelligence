from Models.invoicesModel import InvoicesModel
from database.conn import session

class InvoiceService:
    
    @staticmethod
    def obtener_todas_facturas():
        # Aquí deberías devolver todas las facturas de la base de datos
        pass

    @staticmethod
    def agregar_factura(data):
        # Crear la nueva factura, pasando los datos necesarios
        new_invoice = InvoicesModel(data)  # Pasar 'data' como argumento
        session.add(new_invoice)
        session.commit()
        
        return {
                "msg": "Factura cargada en la base de datos de manera exitosa",
                "statusCode": 200
               }
