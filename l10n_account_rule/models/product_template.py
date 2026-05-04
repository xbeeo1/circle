# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from datetime import datetime, date
from odoo.exceptions import UserError
from odoo.exceptions import ValidationError

class ProductTemplateInheritEmc(models.Model):
    _inherit = 'product.template'

    product_brand_id = fields.Many2one("product.brand", string="Product Brand")
    parts_history_line = fields.One2many('product.parts.history', 'product_part_id', string='Parts History Line')


    """CREATE METHOD FOR VALIDATION ON SAME PRODUCT WITH SAME BRAND NAME"""
    def create(self, vals):
        if 'name' in vals:
            existing_product = self.env['product.template'].search([('product_brand_id', '=', vals['product_brand_id']), ('name', '=', vals['name'])], limit=1)
            if existing_product:
                raise ValidationError("Same Product With Same Brand & Same Internal Reference Already Exist.")
        return super(ProductTemplateInheritEmc, self).create(vals)




class ProductPartsHistoryLine(models.Model):
    _name = 'product.parts.history'
    _description = 'product.part.history'

    product_part_id = fields.Many2one("product.template", string="Part ID")
    part_number = fields.Char(string="Part Number")
    date_from = fields.Date(string="Date From", default=date.today())
    date_to = fields.Date(string="Date To", default=date.today())
    engine_id = fields.Many2one('engine.number', string='Engine Number')
    engine_capacity = fields.Float(string="Capacity")

