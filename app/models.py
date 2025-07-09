from decimal import Decimal
import enum
from datetime import datetime, date
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Integer, DateTime, func, ForeignKey, Date, Enum as SQLAEnum, Numeric
from typing import List


class InvoiceStatus(enum.Enum):
  DRAFT = "draft"
  SENT = "sent"
  PAID = "paid"
  OVERDUE = "overdue"
  CANCELED = "canceled"

class Base(DeclarativeBase):
  pass

db = SQLAlchemy(model_class=Base)

class User(db.Model):
  __tablename__ = "users"
  
  id: Mapped[int] = mapped_column(primary_key=True)
  name: Mapped[str] = mapped_column(String(150), nullable=False)
  email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
  password: Mapped[str] = mapped_column(String(250), nullable=False)
  company_name: Mapped[str] = mapped_column(String(150))
  
  created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
  updated_at: Mapped[datetime] = mapped_column(
    DateTime,
    server_default=func.now(),
    onupdate=func.now()
  )
  
  clients: Mapped[List["Client"]] = relationship(back_populates="user", cascade="all, delete-orphan")
  invoices: Mapped[List["Invoice"]] = relationship(back_populates="user")


class Client(db.Model):
  __tablename__ = "clients"
  
  id: Mapped[int] = mapped_column(primary_key=True)
  user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
  name: Mapped[str] = mapped_column(String(250), nullable=False)
  company_name: Mapped[str] = mapped_column(String(250))
  email: Mapped[str] = mapped_column(String(150), unique=True, nullable=False)
  password: Mapped[str] = mapped_column(String(250), nullable=False)
  phone: Mapped[str] = mapped_column(String(50), nullable=False)
  address_line1: Mapped[str] = mapped_column(String(250), nullable=False)
  address_line2: Mapped[str] = mapped_column(String(150))
  city: Mapped[str] = mapped_column(String(100), nullable=False)
  state: Mapped[str] = mapped_column(String(100), nullable=False)
  postal_code: Mapped[str] = mapped_column(String(50), nullable=False)
  
  created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
  updated_at: Mapped[datetime] = mapped_column(
    DateTime,
    server_default=func.now(),
    onupdate=func.now()
  )

  user: Mapped["User"] = relationship(back_populates="clients")
  invoices: Mapped[List["Invoice"]] = relationship(back_populates="client")


class Invoice(db.Model):
  __tablename__ = "invoices"
  
  id: Mapped[int] = mapped_column(primary_key=True)
  user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
  client_id: Mapped[int] = mapped_column(ForeignKey("clients.id"))
  invoice_number: Mapped[str] = mapped_column(String(50), unique=True)
  issue_date: Mapped[date] = mapped_column(Date, default=date.today)
  due_date: Mapped[date] = mapped_column(Date, nullable=False)
  status: Mapped[InvoiceStatus] = mapped_column(
    SQLAEnum(InvoiceStatus),
    default=InvoiceStatus.DRAFT,
    nullable=False
  ) 
  total_amount: Mapped[Decimal] = mapped_column(Numeric(10, 2), default=0.00, nullable=False)
  
  created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
  updated_at: Mapped[datetime] = mapped_column(
    DateTime,
    server_default=func.now(),
    onupdate=func.now()
  )
  
  client: Mapped["Client"] = relationship(back_populates="invoices")
  user: Mapped["User"] = relationship(back_populates="invoices")
  invoice_items: Mapped[List["InvoiceItem"]] = relationship(back_populates="invoice", cascade="all, delete-orphan")
  


class InvoiceItem(db.Model):
  __tablename__ = "invoice_items"
  
  id: Mapped[int] = mapped_column(primary_key=True)
  invoice_id: Mapped[int] = mapped_column(ForeignKey("invoices.id"))
  description: Mapped[str] = mapped_column(String(500), nullable=False)
  quantity: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
  unit_price: Mapped[Decimal] = mapped_column(Numeric(10, 2), default=Decimal("0.00"), nullable=False)
  total: Mapped[Decimal] = mapped_column(Numeric(10, 2), default=Decimal("0.00"), nullable=False)
  
  created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
  updated_at: Mapped[datetime] = mapped_column(
    DateTime,
    server_default=func.now(),
    onupdate=func.now()
  )
  
  invoice: Mapped["Invoice"] = relationship(back_populates="invoice_items")

from . import listeners