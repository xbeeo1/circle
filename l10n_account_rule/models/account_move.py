# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError
from odoo.exceptions import ValidationError
from datetime import datetime


class AccountMoveInheritSl(models.Model):
    _inherit = 'account.move'

    invoice_number = fields.Char(string="Invoice Number")
    bill_number = fields.Char(string="Bill Number")

    partner_credit = fields.Monetary(string="Partner Credit", related='partner_id.debit')
    partner_debit = fields.Monetary(string="Partner Debit", related='partner_id.credit')
    partner_current_balance = fields.Monetary(string="Current Balance", compute='_compute_partner_current_balance')

    # Adding custom fields to store amounts by age category
    amount_0_30 = fields.Float(string='Amount 0-30 Days', compute='_compute_age_amounts')
    amount_31_60 = fields.Float(string='Amount 31-60 Days', compute='_compute_age_amounts')
    amount_61_90 = fields.Float(string='Amount 61-90 Days', compute='_compute_age_amounts')
    amount_90_120 = fields.Float(string='Amount 90-120 Days', compute='_compute_age_amounts')
    amount_120_plus = fields.Float(string='Amount 120+ Days', compute='_compute_age_amounts')
    ledger_balance = fields.Float(string='Ledger Balance', compute='_compute_age_amounts')

    """For Fetching Invoice Age"""
    @api.depends('status_in_payment','partner_id')
    def _compute_age_amounts(self):
        for record in self:
            record.amount_0_30 = 0.0
            record.amount_31_60 = 0.0
            record.amount_61_90 = 0.0
            record.amount_90_120 = 0.0
            record.amount_120_plus = 0.0
            record.ledger_balance = 0.0
            move_obj = self.env['account.move'].search([('partner_id','=',record.partner_id.id),('status_in_payment','in',['not_paid','partial'])])
            for line in move_obj:
                if line.amount_residual > 0:
                    due_date = fields.Date.from_string(record.invoice_date_due)
                    today = datetime.today().date()
                    delta_days = (today - due_date).days
                    record.ledger_balance += line.amount_residual
                    if delta_days <= 30:
                        record.amount_0_30 += line.amount_residual
                    elif delta_days <= 60:
                        record.amount_31_60 += line.amount_residual
                    elif delta_days <= 90:
                        record.amount_61_90 += line.amount_residual
                    elif delta_days <= 120:
                        record.amount_90_120 += line.amount_residual
                    else:
                        record.amount_120_plus += line.amount_residual


    """For Partner Current Balance"""
    @api.depends('partner_current_balance', 'partner_id')
    def _compute_partner_current_balance(self):
        for rec in self:
            if rec.partner_id:
                rec.partner_current_balance = rec.partner_id.credit - rec.partner_id.debit
            else:
                rec.partner_current_balance = False