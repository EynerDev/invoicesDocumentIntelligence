from sqlalchemy import Column, String, DateTime, Integer, BigInteger
from database.conn import Base
from sqlalchemy.sql.functions import current_timestamp


class ProviderModel(Base):

    __tablename__ = "provider"

    id = Column(Integer, nullable=False, primary_key=True,
                        autoincrement=True)
    name = Column(String(150), nullable=False)
    nit = Column(Integer, nullable=False)
    email = Column(String(150), nullable=True)
    address = Column(String(150), nullable=True)
    number = Column(String(150), nullable=True)
    website = Column(String(250), nullable=True)
    active = Column(Integer, nullable=True, default=1)
    created_at = Column(DateTime, default=current_timestamp())
    update_at = Column(DateTime, default=current_timestamp(),
                        onupdate=current_timestamp())

    def __init__(self, name, nit, email, address, number, website):
        self.name = name
        self.nit = nit
        self.email = email
        self.address = address
        self.number = number
        self.website = website

    def __repr__(self):
        return {
            "id":self.id,
            "name": self.name,
            "nit": self.nit,
            "email": self.email,
            "address": self.address,
            "number": self.number,
            "website": self.website,
            "active": self.active

        }