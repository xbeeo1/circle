from odoo import models, fields, api

class AccountMoveLineInheritLs(models.Model):
    _inherit = 'account.move.line'

    discount_amount = fields.Monetary(string='Discount', currency_field='currency_id', store=True)
    discount = fields.Float(string="Discount (%)", compute='_compute_discount', store=True, readonly=False, precompute=True, digits=(16, 4))

    @api.onchange('discount_amount')
    def _onchange_discount_amount(self):
        for line in self:
            if line.discount_amount:
                total_amount = line.price_unit * line.quantity
                percentage_discount = (line.discount_amount / total_amount) * 100
                line.discount = percentage_discount


