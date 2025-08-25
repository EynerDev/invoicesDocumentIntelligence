from src.Models.providerModel import ProviderModel
from src.database.conn import session

class ProviderService:
    
    @staticmethod
    def get_provider_by_id():
        try:
            providers = session.query(ProviderModel).all()
            if not provider :
                raise AssertionError("¡ERROR! No se encontraron proveedores")
            
            return {
                "msg" : "Proveedores encontrados con exito",
                "data" : [provider.__repr__() for provider in providers ],
                "statusCode" : 200
            }
            
        except Exception as e:
            return {
                "statusCode" : 400,
                "msg": ""
            }
            
            