from sqlalchemy import Column, NVARCHAR, String, DateTime, Integer, BigInteger
from database.conn import Base
from sqlalchemy.sql.functions import current_timestamp


class InvoicesModel(Base):

    __tablename__ = "invoices"

    id = Column(Integer, nullable=False, primary_key=True )
    type_id = Column(Integer, nullable=True)
    path_storage = Column(String(500), nullable=False)
    active = Column(Integer, nullable=True, default=1)
    created_at = Column(DateTime, default=current_timestamp())
    updated_at = Column(DateTime, default=current_timestamp(),
                        onupdate=current_timestamp())
    name_invoice = Column(String(250), nullable=False)
    
    
    def __init__(self, type_id,  path_storage, name_invoice):
        
        self.type_id = type_id
        self.path_storage = path_storage
        self.active = 1  # Por defecto el valor es 1
        self.name_invoice = name_invoice 
    def __repr__(self):
        return {
            "id": self.id,
            "type_id": self.type_id,
            "path_storage": self.path_storage,
            "name_invoice": self.name_invoice,
            "active": self.active
        }