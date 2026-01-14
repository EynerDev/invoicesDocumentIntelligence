from models.providerModel import ProviderModel
from database.conn import session
import json
from sqlalchemy import func


class ProviderService:
    
    @staticmethod
    def obtener_proveedores():
        try:
            providers = session.query(ProviderModel).all()
            if not providers:
                raise AssertionError("No se encontraron proveedores")
            
            else:
                return {
                "msg" : "Proveedores encontrados con exito",
                "data" : [provider.__repr__() for provider in providers],
                "statusCode" : 200
                }
            
        except Exception as e:
            return {
                "statusCode": 400,
                "msg": f"Error: {str(e)}"
            }
            
            
    @staticmethod
    def create_provider(data):
        
        name = data.get("Provider_name")
        nit = data.get("Provider_NIT")
        email = data.get("Email")
        address = data.get("Adress")
        number = data.get("number")
        website = data.get("website")
        
        if not name and nit:
                return jsonify({"error": "Missing required data (Name and NIT)"}), 400
        try:
            valdidate_provider_exists = ProviderService.validate_provider_active_id(nit)
            
            if valdidate_provider_exists:
                raise AssertionError ("Error: Ya existe un proveedor con este NIT")
            
            new_provider = ProviderModel(
                name=name,
                nit=nit,
                email=email,
                address=address,
                number=number,
                website=website,
            )  # Asegúrate de que los campos coinciden con el modelo
            # print(new_provider.name)
            session.add(new_provider)
            session.commit()
            
            return {
                "msg": "Proveedor Creado con exito",
                "data": [new_provider.__repr__()],
                "statusCode": 200
            }
            
        except Exception as e:
            return {
                "msg": f"Error al crear el proveedor: {str(e)}",
                "statusCode": 500
            }
    @staticmethod
    def validate_provider_active_id(nit):
        try:
            validate_if_provider_exists = session.query(ProviderModel).filter(
                ProviderModel.nit == nit,
                ProviderModel.active == 1
            ).first()
            return validate_if_provider_exists
        except Exception as e:
            return False
        
    @staticmethod
    def get_or_create_provider(nit, proveedor_nombre: str, ) -> int:
        if not proveedor_nombre:
            return 1  # proveedor por defecto

        proveedor_normalizado = proveedor_nombre.strip().lower()

        proveedor = session.query(ProviderModel).filter(
            func.lower(ProviderModel.name) == proveedor_normalizado,
            ProviderModel.active == 1
        ).first()

        if proveedor:
            return proveedor.id

        # Si no existe, lo creamos
        nuevo_proveedor = ProviderModel(
            name=proveedor_normalizado,
            nit=nit,
            email="",
            address="",
            number="",
            website=""
        )
        session.add(nuevo_proveedor)
        session.commit()

        return nuevo_proveedor.id
