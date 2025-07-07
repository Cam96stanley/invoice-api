from decimal import Decimal
from sqlalchemy import event
from sqlalchemy.orm import object_session
from models import InvoiceItem, Invoice, db

@event.listens_for(InvoiceItem, "before_insert")
@event.listens_for(InvoiceItem, "before_update")
def set_total(mapper, connection, target: InvoiceItem):
  target.total = target.quantity * target.unit_price

@event.listens_for(InvoiceItem, "after_insert")
@event.listens_for(InvoiceItem, "after_update")
@event.listens_for(InvoiceItem, "after_delete")
def invoice_item_change(mapper, connection, target: InvoiceItem):
  session = object_session(target)
  if session:
    invoice = target.invoice
    if invoice:
      invoice.total_amount = sum(
        (item.total or Decimal("0.00")) for item in invoice.invoice_items
      )
      session.add(invoice)

@event.listens_for(Invoice, "before_insert")
def generate_invoice_number(mapper, connection, target: Invoice):
  prefix = "INV-"
  last_number = connection.execute(
    db.text("SELECT invoice_number FROM invoices WHERE user_id = :uid ORDER BY id DESC LIMIT 1"), {"uid": target.user_id}
  ).scalar()
  
  if last_number and last_number.startswith(prefix):
    try:
      last_int = int(last_number.replace(prefix, ""))
    except ValueError:
      last_int = 0
  else:
    last_int = 0
  
  new_number = f"{prefix}{last_int + 1:05d}"
  target.invoice_number = new_number