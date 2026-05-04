# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError
from odoo.exceptions import ValidationError


class ProductBrand(models.Model):
    _name = "product.brand"
    _description = "ProjectRider"

    name = fields.Char(string="Name")
    description = fields.Char(string="Description")


    # """CREATE METHOD FOR VALIDATION ON DUPLICATION NAME AND DLS"""
    # def create(self, vals):
    #     if 'name' in vals:
    #         existing_name = self.search([('name', '=', vals['name'])], limit=1)
    #         if existing_name:
    #             raise ValidationError("Brand Name Already Exist.")
    #     return super(ProductBrand, self).create(vals)
    #
    # """WRITE METHOD FOR VALIDATION ON DUPLICATION NAME AND DLS"""
    # def write(self, vals):
    #     if 'name' in vals:
    #         existing_name = self.search([('name', '=', vals['name'])], limit=1)
    #         if existing_name:
    #             raise ValidationError("Brand Name Already Exist.")
    #     return super(ProductBrand, self).create(vals)