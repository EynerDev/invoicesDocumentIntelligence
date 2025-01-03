from sqlalchemy import Column, NVARCHAR, String, DateTime, Integer, BigInteger
from database.conn import Base
from sqlalchemy.sql.functions import current_timestamp


class InvoicesModel(Base):

    __tablename__ = "invoices"

    id = Column(Integer, nullable=False, primary_key=True )
    type_id = Column(Integer, nullable=False)
    provider_id = Column(Integer, nullable=False)
    path_storage = Column(String(500), nullable=False)
    active = Column(Integer, nullable=True, default=1)
    created_at = Column(DateTime, default=current_timestamp())
    update_at = Column(DateTime, default=current_timestamp(),
                        onupdate=current_timestamp())

    def __init__(self, data):
        self.id = data.get('id')

    def __repr__(self):
        return {
            "id": self.id,
            "type_id": self.type_id,
            "provider_id": self.provider_id,
            "path_storage": self.path_storage,
            "active": self.active
        }