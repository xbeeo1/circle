from odoo import models, fields, api


class PurchaseOrderLineInheritLs(models.Model):
    _inherit = 'purchase.order.line'

    discount_amount = fields.Float(string='Disc Amount')
    discount = fields.Float(string="Discount (%)", digits=(16, 6), default=0.0)
    gst_amount = fields.Monetary(string='GST Amount', compute='_compute_gst_amount', store=True,currency_field='currency_id')

    @api.depends('tax_ids', 'price_unit', 'product_qty','discount_amount')
    def _compute_gst_amount(self):
        for line in self:
            gst_rate = 0.0
            if line.tax_ids:
                gst_rate = sum(tax.amount for tax in line.tax_ids) / 100
            line.gst_amount = (line.price_unit * line.product_qty - line.discount_amount) * gst_rate

    @api.onchange('discount_amount', 'price_unit', 'product_qty')
    def discount_amount_onchange(self):
        if self.discount_amount:
            amt = self.price_unit * self.product_qty
            pis_p = (self.discount_amount / amt) * 100
            self.discount = pis_p
        else:
            self.discount = 0

    @api.onchange('discount')
    def discount_p_onchange(self):
        if self.discount:
            amt = self.price_unit * self.product_qty
            pis_p = (amt / 100) * self.discount
            self.discount_amount = pis_p
        else:
            self.discount_amount = 0


    def _prepare_account_move_line(self, move=False):
        res = super()._prepare_account_move_line(move)
        res.update({'discount_amount': self.discount_amount})
        return res
