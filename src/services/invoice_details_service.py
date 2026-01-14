from models.invoicesDetailModel import InvoiceDetailsModels
from services.provider_service import ProviderService
from database.conn import session

class DetailsDocumentIntelligence:
    
    @staticmethod
    def agregar_detalle_factura(data, id_invoice):
        try:  
            
            proveedor = data.get("Proveedor")
            nit = data.get("Nit_proveedor")
            proveedor_id = ProviderService.get_or_create_provider(nit, proveedor)  # 🔹 default 1 si no existe

            # Sanitizar cupon_pago
            try:
                cupon_pago = int(str(data.get("Cupon_Pago", "0")).replace(".", "").replace(",", ""))
            except ValueError:
                cupon_pago = 0

            # Diccionario limpio con valores por defecto
            detail_data = {
                "id_invoice": id_invoice,
                "billed_month": data.get("Mes_Facturaacion") or "N/A",
                "issue_date": data.get("Fecha_Emision_factura") or "N/A",
                "expiration_date": data.get("Fecha_Limite_pago") or "N/A",
                "last_payment": data.get("Valor_Ultimo_Pago") or "0",
                "suspension_date": data.get("Fecha_Limite_pago") or "N/A",
                "total_overdue_debt": data.get("Deuda") or "0",
                "total_invoices_month": data.get("Total_A_Pagar") or "0",
                "number_contract": data.get("N° Contrato") or "0",
                "cupon_pago": cupon_pago,
                "proveedor_id": proveedor_id
            }

            new_detail_invoice = InvoiceDetailsModels(detail_data)
            session.add(new_detail_invoice)
            session.commit()

            return {
                "msg": f"Detalles de factura {id_invoice} cargados en la base de datos de manera exitosa",
                "statusCode": 200
            }

        except Exception as e:
            session.rollback()
            raise  # 🔹 lanza el error real para debug
