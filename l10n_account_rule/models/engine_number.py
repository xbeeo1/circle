# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError
from odoo.exceptions import ValidationError


class EngineNumber(models.Model):
    _name = "engine.number"
    _description = "Engine Number"

    name = fields.Char(string="Name")
    description = fields.Char(string="Description")
