# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from datetime import date, timedelta
from odoo.exceptions import UserError
from odoo.exceptions import ValidationError


class PartnerSaleHistory(models.Model):
    _name = 'partner.sale.history'

    order_id = fields.Many2one('sale.order', string='Sale Order', ondelete='cascade')
    sale_order_id = fields.Many2one('sale.order', string='Sale Order', ondelete='cascade')
    date_order = fields.Datetime(string="Order Date")
    company_id = fields.Many2one(related='order_id.company_id', store=True, index=True)
    currency_id = fields.Many2one('res.currency', string='Currency', required=True, default=lambda self: self.env.user.company_id.currency_id)

    # Fields specifying custom line logic
    display_type = fields.Selection(selection=[('line_section', "Section"), ('line_note', "Note"), ], default=False)

    sequence = fields.Integer(string="Sequence", help="Gives the sequence order when displaying a list of sale quote lines.", default=10)

    product_id = fields.Many2one(comodel_name='product.product', string="Product Variant",  check_company=True)
    product_template_id = fields.Many2one(comodel_name='product.template', string="Product", check_company=True)
    name = fields.Text(string="Description", store=True)
    product_uom = fields.Many2one(comodel_name='uom.uom', string="UOM", related='product_id.uom_id')
    # product_uom_category_id = fields.Many2one(related='product_id.uom_id.category_id')
    product_uom_qty = fields.Float(string='Quantity', required=True, digits='Product Unit of Measure', default=1)
    price_unit = fields.Monetary(string="Unit price")
    tax_id = fields.Many2many('account.tax', string="Taxes", store=True, context={'active_test': False},  check_company=True)
    price_tax = fields.Monetary(string="Tax Amount")
    discount = fields.Float(string="Disc%")
    discount_amount = fields.Monetary(string="Discount")
    price_subtotal = fields.Monetary(string="Subtotal")
    price_total = fields.Monetary(string="Amount Total")
    conversion_rate_pkr = fields.Float(string="Conversion Rate", compute='_compute_amount_in_pkr')
    amount_in_pkr = fields.Float(string="Amount PKR", compute='_compute_amount_in_pkr')


    """OTHER CURRENCY TO PKR AMOUNT"""
    @api.depends('amount_in_pkr', 'conversion_rate_pkr', 'price_subtotal', 'price_total')
    def _compute_amount_in_pkr(self):
        for line in self:
            if line.currency_id.name != 'PKR':
                rate = line.env['res.currency.rate'].search(
                    [('currency_id', '=', line.currency_id.id), ('name', '=', date.today())], limit=1)
                if rate:
                    print(f"Currency: {line.currency_id.name}, Date: {date.today()}, Rate: {rate.inverse_company_rate}")
                    line.amount_in_pkr = line.price_total * rate.inverse_company_rate  # Convert to PKR
                    line.conversion_rate_pkr = rate.inverse_company_rate  # Currency to PKR
                else:
                    print(f"No exchange rate found for {line.currency_id.name} on {date.today()}")
                    line.amount_in_pkr = line.price_total  # Keep original amount if no rate is found
                    line.conversion_rate_pkr = 1  # Keep original amount if no rate is found
            else:
                line.amount_in_pkr = line.price_total
                line.conversion_rate_pkr = 1







class TotalSaleHistory(models.Model):
    _name = 'total.sale.history'

    order_id = fields.Many2one('sale.order', string='Sale Order', ondelete='cascade')
    sale_order_id = fields.Many2one('sale.order', string='Sale Order', ondelete='cascade')
    date_order = fields.Datetime(string="Order Date")
    partner_id = fields.Many2one('res.partner', related='sale_order_id.partner_id', string="Customer", store=True)
    company_id = fields.Many2one(related='order_id.company_id', store=True, index=True)
    currency_id = fields.Many2one('res.currency', string='Currency', required=True,
                                  default=lambda self: self.env.user.company_id.currency_id)

    # Fields specifying custom line logic
    display_type = fields.Selection(selection=[('line_section', "Section"), ('line_note', "Note"), ], default=False)

    sequence = fields.Integer(string="Sequence",
                              help="Gives the sequence order when displaying a list of sale quote lines.", default=10)

    product_id = fields.Many2one(comodel_name='product.product', string="Product Variant", check_company=True)
    product_template_id = fields.Many2one(comodel_name='product.template', string="Product", check_company=True)
    name = fields.Text(string="Description", store=True)
    product_uom = fields.Many2one(comodel_name='uom.uom', string="UOM", related='product_id.uom_id')
    # product_uom_category_id = fields.Many2one(related='product_id.uom_id.category_id')
    product_uom_qty = fields.Float(string='Quantity', required=True, digits='Product Unit of Measure', default=1)
    price_unit = fields.Monetary(string="Unit price")
    tax_id = fields.Many2many('account.tax', string="Taxes", store=True, context={'active_test': False},
                              check_company=True)
    price_tax = fields.Monetary(string="Tax Amount")
    discount = fields.Float(string="Disc%")
    discount_amount = fields.Monetary(string="Discount")
    price_subtotal = fields.Monetary(string="Subtotal")
    price_total = fields.Monetary(string="Amount Total")
    conversion_rate_pkr = fields.Float(string="Conversion Rate", compute='_compute_amount_in_pkr')
    amount_in_pkr = fields.Float(string="Amount PKR", compute='_compute_amount_in_pkr')


    """OTHER CURRENCY TO PKR AMOUNT"""
    @api.depends('amount_in_pkr', 'price_subtotal', 'price_total')
    def _compute_amount_in_pkr(self):
        for line in self:
            if line.currency_id.name != 'PKR':
                rate = line.env['res.currency.rate'].search(
                    [('currency_id', '=', line.currency_id.id), ('name', '=', date.today())], limit=1)
                if rate:
                    print(f"Currency: {line.currency_id.name}, Date: {date.today()}, Rate: {rate.inverse_company_rate}")
                    line.amount_in_pkr = line.price_total * rate.inverse_company_rate  # Convert to PKR
                    line.conversion_rate_pkr = rate.inverse_company_rate  # Currency to PKR
                else:
                    print(f"No exchange rate found for {line.currency_id.name} on {date.today()}")
                    line.amount_in_pkr = line.price_total  # Keep original amount if no rate is found
                    line.conversion_rate_pkr = 1  # Keep original amount if no rate is found
            else:
                line.amount_in_pkr = line.price_total
                line.conversion_rate_pkr = 1  # Keep original amount if no pkr is found






class ProductSalePartsHistory(models.Model):
    _name = 'sale.product.parts.history'

    order_id = fields.Many2one('sale.order', string='Sale Order', ondelete='cascade')
    product_part_id = fields.Many2one("product.template", string="Product")
    part_number = fields.Char(string="Part Number")
    date_from = fields.Date(string="Date From", default=date.today())
    date_to = fields.Date(string="Date To", default=date.today())
    engine_id = fields.Many2one('engine.number', string='Engine Number')
    engine_capacity = fields.Float(string="Capacity")

