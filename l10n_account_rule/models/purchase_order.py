# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError
from odoo.exceptions import ValidationError

class PurchaseOrderInheritSl(models.Model):
    _inherit = 'purchase.order'


    partner_purchase_history = fields.One2many("partner.purchase.history", "order_id", string="Partner Purchase History")
    total_purchase_history = fields.One2many("total.purchase.history", "order_id", string="Total Purchase History")
    purchase_products_parts_history = fields.One2many("purchase.product.parts.history", "order_id", string="Total Purchase History")

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


    """GET PURCHASE HISTORY METHOD"""
    def get_product_purchase_history(self):
        for rec in self:
            rec.get_partner_purchase_history()
            rec.get_total_purchase_history()
            rec.get_product_parts_history()




    """RELATED PARTNER PURCHASE PRODUCTS"""
    def get_partner_purchase_history(self):
        for rec in self:
            # CHECK IF THERE ARE ORDER LINES
            if rec.order_line:

                # INITIALIZE AN EMPTY LIST TO STORE PARTNER PURCHASE HISTORY
                partner_purchase = []

                # GET THE LAST ORDER LINE
                last_line = rec.order_line[-1]  # Fetch the last product in order line

                # SEARCH FOR RELATED PURCHASE ORDER LINES FOR THE SAME PRODUCT TEMPLATE AND PARTNER
                purchase_line = self.env['purchase.order.line'].search([
                    ('product_id', '=', last_line.product_id.id),  # MATCH PRODUCT TEMPLATE
                    ('order_id.partner_id', '=', rec.partner_id.id),  # MATCH PARTNER
                    ('order_id.state', '=', 'purchase'), ('order_id.invoice_status', '=', 'invoiced')  # ONLY CONFIRMED PURCHASE
                ])

                # CHECK IF ANY PURCHASE LINES ARE FOUND
                if purchase_line:

                    # ITERATE THROUGH EACH PURCHASE LINE
                    for purchase_line in purchase_line:
                        # ADD PURCHASE LINE DETAILS TO PARTNER PURCHASE HISTORY
                        partner_purchase.append((0, 0, {
                            'product_id': purchase_line.product_id.id,  # PRODUCT TEMPLATE ID
                            'name': purchase_line.name,  # PRODUCT DESCRIPTION
                            'purchase_order_id': purchase_line.order_id.id,  # PURCHASE ORDER ID
                            'date_order': purchase_line.date_order,  # PURCHASE ORDER DATE
                            'currency_id': purchase_line.order_id.currency_id.id,  # PURCHASE ORDER CURRENCY
                            'product_uom': purchase_line.product_uom_id.id,  # UNIT OF MEASURE ID
                            'product_uom_qty': purchase_line.product_uom_qty,  # QUANTITY
                            'price_unit': purchase_line.price_unit,  # UNIT PRICE
                            'taxes_id': [(4, tax.id) for tax in purchase_line.tax_ids],  # APPLIED TAXES
                            'price_tax': purchase_line.price_tax,  # TAX AMOUNT
                            'discount': purchase_line.discount,  # DISCOUNT PERCENTAGE
                            'discount_amount': purchase_line.discount_amount,  # DISCOUNT AMOUNT
                            'price_subtotal': purchase_line.price_subtotal,  # SUBTOTAL
                            'price_total': purchase_line.price_total,  # TOTAL AMOUNT
                        }))


                # RESET AND UPDATE THE PARTNER PURCHASE HISTORY FIELD
                rec.partner_purchase_history = False
                rec.partner_purchase_history = partner_purchase

            else:
                # IF NO ORDER LINES, CLEAR THE PARTNER PURCHASE HISTORY FIELD
                rec.partner_purchase_history = False



    """OVERALL PURCHASE PRODUCTS"""
    def get_total_purchase_history(self):
        for rec in self:
            # CHECK IF THERE ARE ORDER LINES
            if rec.order_line:

                # INITIALIZE AN EMPTY LIST TO STORE TOTAL PURCHASE HISTORY
                total_purchase = []

                # GET THE LAST ORDER LINE
                last_line = rec.order_line[-1]  # Fetch the last product in order line

                # SEARCH FOR RELATED PURCHASE ORDER LINES FOR THE SAME PRODUCT TEMPLATE
                purchases_line = self.env['purchase.order.line'].search([
                    ('product_id', '=', last_line.product_id.id),  # MATCH PRODUCT TEMPLATE
                    ('order_id.state', '=', 'purchase'),
                    ('order_id.invoice_status', '=', 'invoiced')  # ONLY CONFIRMED PURCHASES
                ])

                # CHECK IF ANY PURCHASE LINES ARE FOUND
                if purchases_line:
                    # ITERATE THROUGH EACH PURCHASE LINE
                    for purchase_line in purchases_line:
                        # ADD PURCHASE LINE DETAILS TO TOTAL PURCHASE HISTORY
                        total_purchase.append((0, 0, {
                            'product_id': purchase_line.product_id.id,  # PRODUCT TEMPLATE ID
                            'name': purchase_line.name,  # PRODUCT DESCRIPTION
                            'purchase_order_id': purchase_line.order_id.id,  # PURCHASE ORDER ID
                            'date_order': purchase_line.date_order,  # PURCHASE ORDER DATE
                            'currency_id': purchase_line.order_id.currency_id.id,  # PURCHASE ORDER CURRENCY
                            'product_uom': purchase_line.product_uom_id.id,  # UNIT OF MEASURE ID
                            'product_uom_qty': purchase_line.product_uom_qty,  # QUANTITY
                            'price_unit': purchase_line.price_unit,  # UNIT PRICE
                            'taxes_id': [(4, tax.id) for tax in purchase_line.tax_ids],  # APPLIED TAXES
                            'price_tax': purchase_line.price_tax,  # TAX AMOUNT
                            'discount': purchase_line.discount,  # DISCOUNT PERCENTAGE
                            'discount_amount': purchase_line.discount_amount,  # DISCOUNT AMOUNT
                            'price_subtotal': purchase_line.price_subtotal,  # SUBTOTAL
                            'price_total': purchase_line.price_total,  # TOTAL AMOUNT
                        }))

                # RESET AND UPDATE THE TOTAL PURCHASE HISTORY FIELD
                rec.total_purchase_history = False
                rec.total_purchase_history = total_purchase

            else:
                # IF NO ORDER LINES, CLEAR THE TOTAL PURCHASE HISTORY FIELD
                rec.total_purchase_history = False



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
                rec.purchase_products_parts_history = False
                rec.purchase_products_parts_history = products_part_history

            else:
                # IF NO ORDER LINES, CLEAR THE TOTAL PURCHASE HISTORY FIELD
                rec.purchase_products_parts_history = False



























    # """OVERALL PURCHASE PRODUCTS"""
    # def get_product_parts_history(self):
    #     for rec in self:
    #         # CHECK IF THERE ARE ORDER LINES
    #         if rec.order_line:
    #
    #             # INITIALIZE AN EMPTY LIST TO STORE TOTAL PURCHASE HISTORY
    #             products_part_history = []
    #
    #             # ITERATE THROUGH EACH ORDER LINE
    #             for line in rec.order_line:
    #
    #                 # ADD A SECTION LINE FOR THE PRODUCT TEMPLATE
    #                 products_part_history.append((0, 0, {
    #                     'name': line.product_id.name,  # PRODUCT TEMPLATE NAME
    #                     'display_type': 'line_section',  # SET AS LINE SECTION
    #                 }))
    #
    #                 print('products_part_history', products_part_history)
    #
    #                 if line.product_id.parts_history_line:
    #
    #                     for parts_line in line.product_id.parts_history_line:
    #                         # ADD PARTS HISTORY LINE DETAILS TO TOTAL PURCHASE HISTORY
    #                         products_part_history.append((0, 0, {
    #                             'product_part_id': parts_line.product_part_id.id,  # PRODUCT TEMPLATE ID
    #                             'name': parts_line.product_part_id.display_name,  # PRODUCT TEMPLATE ID
    #                             'part_number': parts_line.part_number,  # PRODUCT TEMPLATE ID
    #                             'date_from': parts_line.date_from,  # PRODUCT TEMPLATE ID
    #                             'date_to': parts_line.date_to,  # PRODUCT TEMPLATE ID
    #                             'engine_id': parts_line.engine_id.id,  # PRODUCT TEMPLATE ID
    #                             'engine_capacity': parts_line.engine_capacity,  # PRODUCT TEMPLATE ID
    #
    #                         }))
    #
    #             # RESET AND UPDATE THE TOTAL PURCHASE HISTORY FIELD
    #             rec.purchase_products_parts_history = False
    #             rec.purchase_products_parts_history = products_part_history
    #
    #         else:
    #             # IF NO ORDER LINES, CLEAR THE TOTAL PURCHASE HISTORY FIELD
    #             rec.purchase_products_parts_history = False



