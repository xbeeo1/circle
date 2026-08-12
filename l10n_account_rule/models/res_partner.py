from odoo import models , api ,fields, _
from odoo.exceptions import ValidationError
from datetime import datetime, date
from dateutil.relativedelta import relativedelta



class ResPartnerInherit(models.Model):
    _inherit = "res.partner"

    partner_strn = fields.Char(string="STRN")
    district = fields.Char(string="District")
    cnic = fields.Char(
        string='CNIC',
        required=True,
    )
    phone = fields.Char(
        required=True,
    )

    district = fields.Char(
        required=True,
    )

    city = fields.Char(
        required=True,
    )