from sqlalchemy import Column, String, DateTime, Integer, BigInteger
from database.conn import Base
from sqlalchemy.sql.functions import current_timestamp


class InvoiceDetailsModels(Base):

    __tablename__ = "invoices_details"

    id = Column(Integer, nullable=False, primary_key=True,
                        autoincrement=True)
    id_invoice = Column(Integer, nullable=False)
    number_invoice = Column(String(150), nullable=False)
    billed_month = Column(String(150), nullable=False)
    issue_date = Column(String(150), nullable=False)
    expiration_date = Column(String(150), nullable=False)
    last_payment = Column(String(150), nullable=False)
    suspension_date = Column(String(150), nullable=False)
    overdue_invoices = Column(String(150), nullable=False)
    total_overdue_debt = Column(String(150), nullable=False)
    total_invoices_month = Column(String(150), nullable=False)
    active = Column(Integer, nullable=True, default=1)
    created_at = Column(DateTime, default=current_timestamp())
    updated_at = Column(DateTime, default=current_timestamp(),
                        onupdate=current_timestamp())
    number_contract = Column(String(150), nullable=False)
    

    def __init__(self, data):
        self.id = data.get('id').upper()

    def __repr__(self):
        return {
            
            "id": self.id,
            "id_invoice": self.id_invoice,
            "number_invoice": self.number_invoice,
            "number_contract": self.number_contract,
            "billed_month": self.billed_month,
            "issue_date": self.issue_date,
            "expiration_date": self.expiration_date,
            "last_payment": self.last_payment,
            "suspension_date": self.suspension_date,
            "overdue_invoices": self.overdue_invoices,
            "total_overdue_debt": self.total_overdue_debt,
            "total_invoice_month": self.total_invoices_month,
            "active": self.active
            

        }