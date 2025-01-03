from sqlalchemy import Column, String, DateTime, Integer, BigInteger
from Database.conn import Base
from sqlalchemy.sql.functions import current_timestamp


class ProgramsModel(Base):

    __tablename__ = "provider"

    id = Column(Integer, nullable=False, primary_key=True,
                        autoincrement=True)
    name = Column(String(150), nullable=False)
    email = Column(String(150), nullable=False)
    address = Column(String(150), nullable=False)
    number = Column(String(150), nullable=False)
    website = Column(String(250), nullable=true)
    active = Column(Integer, nullable=True, default=1)
    created_at = Column(DateTime, default=current_timestamp())
    updated_at = Column(DateTime, default=current_timestamp(),
                        onupdate=current_timestamp())

    def __init__(self, data):
        self.name = data.get('name').upper()

    def __repr__(self):
        return {
            "id":self.id,
            "name": self.name,
            "email": self.email,
            "address": self.address,
            "number": self.number,
            "website": self.website,
            "active": self.active

        }