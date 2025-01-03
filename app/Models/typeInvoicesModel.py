from sqlalchemy import Column, String, DateTime, Integer, BigInteger
from Database.conn import Base
from sqlalchemy.sql.functions import current_timestamp


class ProgramsModel(Base):

    __tablename__ = "type_invoices"

    id = Column(Integer, nullable=False, primary_key=True,
                        autoincrement=True)
    name = Column(String(50), nullable=False)
    active = Column(Integer, nullable=True, default=1)
    created_at = Column(DateTime, default=current_timestamp())
    updated_at = Column(DateTime, default=current_timestamp(),
                        onupdate=current_timestamp())

    def __init__(self, data):
        self.name = data.get('name').upper()

    def __repr__(self):
        return {
            "id": self.id,
            "name": self.name,
            "active": self.active

        }