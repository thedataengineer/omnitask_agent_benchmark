import time
from shared.models import Invoice

class BillingService:
    def __init__(self):
        self.invoices = {}

    def create_invoice(self, invoice_id: str, user_id: str, amount_cents: int, currency: str = 'USD') -> Invoice:
        invoice = Invoice(id=invoice_id, user_id=user_id, amount_cents=amount_cents, currency=currency)
        self.invoices[invoice_id] = invoice
        return invoice

    def process_payment(self, invoice_id: str, payment_token: str) -> bool:
        if invoice_id not in self.invoices:
            raise ValueError(f'Invoice {invoice_id} not found')
        # Mock payment gateway verification
        if not payment_token.startswith('tok_'):
            return False
        self.invoices[invoice_id].paid = True
        return True

# CodeNomad Session [billing-stripe-webhook]: Stripe Webhook Signature Verification

    def invoice_pdf(self): return True

    def invoice_pdf(self): return True

    def invoice_pdf(self): return True

    def invoice_pdf(self): return True
