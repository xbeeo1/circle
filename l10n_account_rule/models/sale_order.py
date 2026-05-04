# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError
from odoo.exceptions import ValidationError

class SaleOrderInheritSl(models.Model):
    _inherit = 'sale.order'


    partner_sale_history = fields.One2many("partner.sale.history", "order_id", string="Partner Sale History")
    total_sale_history = fields.One2many("total.sale.history", "order_id", string="Total Sale History")
    sale_products_parts_history = fields.One2many("sale.product.parts.history", "order_id", string="Product Parts History")

    partner_credit = fields.Monetary(string="Partner Credit", related='partner_id.debit')
    partner_debit = fields.Monetary(string="Partner Debit", related='partner_id.credit')
    partner_current_balance = fields.Monetary(string="Current Balance", compute='_compute_partner_current_balance')


    """COMPUTE PARTNER CURRENT BALANCE"""
    @api.depends('partner_current_balance', 'partner_id')
    def _compute_partner_current_balance(self):
        for rec in self:
            if rec.partner_id:
                rec.partner_current_balance = rec.partner_id.credit - rec.partner_id.debit
            else:
                rec.partner_current_balance = False



    """GET SALE HISTORY METHOD"""
    def get_product_sale_history(self):
        for rec in self:
            rec.get_partner_sale_history()
            rec.get_total_sale_history()
            rec.get_product_parts_history()




    """RELATED PARTNER SALE PRODUCTS"""
    def get_partner_sale_history(self):
        for rec in self:
            # CHECK IF THERE ARE ORDER LINES
            if rec.order_line:

                # INITIALIZE AN EMPTY LIST TO STORE PARTNER SALE HISTORY
                partner_sale = []

                # GET THE LAST ORDER LINE
                last_line = rec.order_line[-1]  # Get the last order line

                # SEARCH FOR RELATED SALE ORDER LINES FOR THE SAME PRODUCT TEMPLATE AND PARTNER
                sales_line = self.env['sale.order.line'].search([
                    ('product_template_id', '=', last_line.product_template_id.id),  # MATCH PRODUCT TEMPLATE
                    ('order_id.partner_id', '=', rec.partner_id.id),  # MATCH PARTNER
                    ('order_id.state', '=', 'sale'),('order_id.invoice_status', '=', 'invoiced')  # ONLY CONFIRMED SALES
                ])

                # CHECK IF ANY SALE LINES ARE FOUND
                if sales_line:

                    # ITERATE THROUGH EACH SALE LINE
                    for sale_line in sales_line:
                        # ADD SALE LINE DETAILS TO PARTNER SALE HISTORY
                        partner_sale.append((0, 0, {
                            'product_template_id': sale_line.product_template_id.id,  # PRODUCT TEMPLATE ID
                            'name': sale_line.name,  # PRODUCT DESCRIPTION
                            'sale_order_id': sale_line.order_id.id,  # SALE ORDER ID
                            'date_order': sale_line.order_id.date_order,  # SALE ORDER DATE
                            'product_uom': sale_line.product_uom.id,  # UNIT OF MEASURE ID
                            'product_uom_qty': sale_line.product_uom_qty,  # QUANTITY
                            'price_unit': sale_line.price_unit,  # UNIT PRICE
                            'currency_id': sale_line.order_id.currency_id.id,  # SALE ORDER CURRENCY
                            'tax_id': [(4, tax.id) for tax in sale_line.tax_ids],  # APPLIED TAXES
                            'price_tax': sale_line.price_tax,  # TAX AMOUNT
                            'discount': sale_line.discount,  # DISCOUNT PERCENTAGE
                            'discount_amount': sale_line.discount_amount,  # DISCOUNT AMOUNT
                            'price_subtotal': sale_line.price_subtotal,  # SUBTOTAL
                            'price_total': sale_line.price_total,  # TOTAL AMOUNT
                        }))


                # RESET AND UPDATE THE PARTNER SALE HISTORY FIELD
                rec.partner_sale_history = False
                rec.partner_sale_history = partner_sale

            else:
                # IF NO ORDER LINES, CLEAR THE PARTNER SALE HISTORY FIELD
                rec.partner_sale_history = False



    """OVERALL SALE PRODUCTS"""
    def get_total_sale_history(self):
        for rec in self:
            # CHECK IF THERE ARE ORDER LINES
            if rec.order_line:

                # INITIALIZE AN EMPTY LIST TO STORE TOTAL SALE HISTORY
                total_sale = []

                # GET THE LAST ORDER LINE
                last_line = rec.order_line[-1]  # Get the last order line

                # SEARCH FOR RELATED SALE ORDER LINES FOR THE SAME PRODUCT TEMPLATE
                sales_line = self.env['sale.order.line'].search([
                    ('product_template_id', '=', last_line.product_template_id.id),  # MATCH PRODUCT TEMPLATE
                    ('order_id.state', '=', 'sale'), ('order_id.invoice_status', '=', 'invoiced')  # ONLY CONFIRMED SALES
                ])

                # CHECK IF ANY SALE LINES ARE FOUND
                if sales_line:

                    # ITERATE THROUGH EACH SALE LINE
                    for sale_line in sales_line:

                        # CALCULATE CONVERTED VALUE IN BASE CURRENCY IF OTHER SALE IN OTHER CURRENCY
                        if sale_line.order_id.currency_id.name != 'PKR':

                            rate_id = self.env['res.currency.rate'].search([
                                ('currency_id', '=', sale_line.order_id.currency_id.id),
                                # ('name', '=', sale_line.order_id.validity_date)
                            ], limit=1)

                            print('rate_id Date', rate_id.name)
                            print('Sale Order Date', sale_line.order_id.date_order)

                        # ADD SALE LINE DETAILS TO TOTAL SALE HISTORY
                        total_sale.append((0, 0, {
                            'product_template_id': sale_line.product_template_id.id,  # PRODUCT TEMPLATE ID
                            'name': sale_line.name,  # PRODUCT DESCRIPTION
                            'sale_order_id': sale_line.order_id.id,  # SALE ORDER ID
                            'date_order': sale_line.order_id.date_order,  # SALE ORDER DATE
                            'product_uom': sale_line.product_uom.id,  # UNIT OF MEASURE ID
                            'product_uom_qty': sale_line.product_uom_qty,  # QUANTITY
                            'price_unit': sale_line.price_unit,  # UNIT PRICE
                            'currency_id': sale_line.order_id.currency_id.id,  # SALE ORDER CURRENCY
                            'tax_id': [(4, tax.id) for tax in sale_line.tax_ids],  # APPLIED TAXES
                            'price_tax': sale_line.price_tax,  # TAX AMOUNT
                            'discount': sale_line.discount,  # DISCOUNT PERCENTAGE
                            'discount_amount': sale_line.discount_amount,  # DISCOUNT AMOUNT
                            'price_subtotal': sale_line.price_subtotal,  # SUBTOTAL
                            'price_total': sale_line.price_total,  # TOTAL AMOUNT
                        }))

                # RESET AND UPDATE THE TOTAL SALE HISTORY FIELD
                rec.total_sale_history = False
                rec.total_sale_history = total_sale

            else:
                # IF NO ORDER LINES, CLEAR THE TOTAL SALE HISTORY FIELD
                rec.total_sale_history = False




    """GET PRODUCT PARTS HISTORY"""

    def get_product_parts_history(self):
        for rec in self:
            # CHECK IF THERE ARE ORDER LINES
            if rec.order_line:

                # INITIALIZE AN EMPTY LIST TO STORE TOTAL PURCHASE HISTORY
                products_part_history = []

                # GET THE LAST ORDER LINE
                last_line = rec.order_line[-1]  # Get the last order line

                print('products_part_history', products_part_history)

                if last_line.product_id.parts_history_line:
                    for parts_line in last_line.product_id.parts_history_line:
                        # ADD PARTS HISTORY LINE DETAILS TO TOTAL PURCHASE HISTORY
                        products_part_history.append((0, 0, {
                            'product_part_id': parts_line.product_part_id.id,  # PRODUCT TEMPLATE ID
                            'part_number': parts_line.part_number,  # PART NUMBER
                            'date_from': parts_line.date_from,  # DATE FROM
                            'date_to': parts_line.date_to,  # DATE TO
                            'engine_id': parts_line.engine_id.id,  # ENGINE NUMBER
                            'engine_capacity': parts_line.engine_capacity,  # ENGINE CAPACITY
                        }))

                # RESET AND UPDATE THE TOTAL PURCHASE HISTORY FIELD
                rec.sale_products_parts_history = False
                rec.sale_products_parts_history = products_part_history

            else:
                # IF NO ORDER LINES, CLEAR THE TOTAL PURCHASE HISTORY FIELD
                rec.sale_products_parts_history = False

