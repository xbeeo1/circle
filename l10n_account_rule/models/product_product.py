# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError
from odoo.exceptions import ValidationError

class ProductProductInheritCl(models.Model):
    _inherit = 'product.product'


    product_brand_id = fields.Many2one("product.brand", string="Product Brand", related='product_tmpl_id.product_brand_id', store=True)
    parts_history_line = fields.One2many('product.parts.history', 'product_part_id', related='product_tmpl_id.parts_history_line', string='Parts History Line')