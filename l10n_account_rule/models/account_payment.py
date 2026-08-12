from odoo import models, fields


class AccountPayment(models.Model):
    _inherit = 'account.payment'

    ref_by = fields.Many2one(
        'res.partner',
        string='Ref By'
    )


class AccountPaymentRegister(models.TransientModel):
    _inherit = 'account.payment.register'

    def _create_payments(self):
        invoices = self.line_ids.move_id

        salesperson = False
        if invoices:
            salesperson = invoices[0].invoice_user_id

        payments = super()._create_payments()

        if salesperson and payments:
            payments.write({
                'ref_by': salesperson.partner_id.id
            })

        return payments