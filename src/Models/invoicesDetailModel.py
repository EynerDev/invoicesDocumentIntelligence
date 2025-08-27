from sqlalchemy import Column, String, DateTime, Integer, BigInteger
from database.conn import Base
from sqlalchemy.sql.functions import current_timestamp


class InvoiceDetailsModels(Base):

    __tablename__ = "invoices_details"

    id = Column(Integer, nullable=False, primary_key=True,
                        autoincrement=True)
    id_invoice = Column(Integer, nullable=False)
    billed_month = Column(String(150), nullable=False)
    issue_date = Column(String(150), nullable=False)
    expiration_date = Column(String(150), nullable=False)
    last_payment = Column(String(150), nullable=False)
    suspension_date = Column(String(150), nullable=False)
    total_overdue_debt = Column(String(150), nullable=False)
    total_invoices_month = Column(String(150), nullable=False)
    active = Column(Integer, nullable=True, default=1)
    created_at = Column(DateTime, default=current_timestamp())
    updated_at = Column(DateTime, default=current_timestamp(),
                        onupdate=current_timestamp())
    number_contract = Column(String(150), nullable=False)
    cupon_pago = Column(String(100), nullable=False)
    proveedor_id = Column(Integer, nullable=False)
    

    def __init__(self, data):
        self.id_invoice = data.get('id_invoice')
        self.billed_month = data.get('billed_month')
        self.issue_date = data.get('issue_date')
        self.expiration_date = data.get('expiration_date')
        self.last_payment = data.get('last_payment')
        self.suspension_date = data.get('suspension_date')
        self.total_overdue_debt = data.get('total_overdue_debt')
        self.total_invoices_month = data.get('total_invoices_month')
        self.active = data.get('active', 1)
        self.number_contract = data.get('number_contract')
        self.cupon_pago = data.get('cupon_pago')
        self.proveedor_id = data.get('proveedor_id')


    def to_dict(self):
        return {
            "id": self.id,
            "id_invoice": self.id_invoice,
            "number_contract": self.number_contract,
            "billed_month": self.billed_month,
            "issue_date": self.issue_date,
            "expiration_date": self.expiration_date,
            "last_payment": self.last_payment,
            "suspension_date": self.suspension_date,
            "total_overdue_debt": self.total_overdue_debt,
            "total_invoice_month": self.total_invoices_month,
            "active": self.active,
            "N° Contrato": self.number_contract,
            "Cupon Pago": self.cupon_pago
        }
