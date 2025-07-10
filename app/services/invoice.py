from datetime import date, timedelta

class Invoice:
  def __init__(self, invoice_id, client_id, amount, due_date, status):
    self.invoice_id = invoice_id
    self.client_id = client_id
    self.amount = amount
    self.due_date = due_date
    self.status = status
  
  def mark_as_sent(self):
    if self.status == "draft":
      self.status = "sent"
      return self.status
    else:
      return "Status can only be changed to 'sent' if current status is 'draft'."
  
  def mark_as_paid(self):
    if self.status == "sent":
      self.status == "paid"
      return self.status
    else:
      return "Status can only be changed to 'paid' if current status is 'sent'"
  
  def mark_as_overdue(self):
    if self.status == "paid":
      self.status = "overdue"
      return self.status
    else:
      return "Status can only be changed to 'overdue' if current status is 'paid'"
  
  def mark_as_canceled(self):
    self.status = "canceled"
    return self.status
  
  def check_payment_status(self):
    return self.status
  
  def extend_due_seven_days(self):
    y, m, d = [int(part) for part in self.due_date.split("/")]
    original_date = date(y, m, d)
    added_days = timedelta(days=7)
    self.due_date = original_date + added_days
    return self.due_date