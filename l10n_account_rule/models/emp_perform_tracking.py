# -*- coding: utf-8 -*-
from email.policy import default

from odoo import models, fields, api, _
from datetime import date, datetime, timedelta
from odoo.exceptions import ValidationError



class EmployeePerformanceTracking(models.Model):
    _name = 'employee.performance.tracking'
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = 'Employee Performance Tracking'

    name = fields.Char(string="Sequence", default='New')
    image_1920 = fields.Binary(string="Image")

    # LEFT COLUMN
    employee_id = fields.Many2one('hr.employee', 'Employee', check_company=True)
    date_from = fields.Date(string="Date From", default=date.today(), check_company=True)
    user_id = fields.Many2one('res.users', string="Responsible", default=lambda self: self.env.user, check_company=True)

    # RIGHT COLUMN
    department_id = fields.Many2one('hr.department', 'Department', related='employee_id.department_id', store=True)
    date_to = fields.Date(string="Date To", default=date.today(), check_company=True)
    # INVISIBLE FIELDS
    currency_id = fields.Many2one('res.currency', string='Currency', required=True, default=lambda self: self._default_currency_id(), check_company=True)
    company_id = fields.Many2one('res.company', string='Currency', required=True, default=lambda self: self.env.company.id)


    total_expense_amount = fields.Monetary(string="Total Expense")
    total_invoice_amount = fields.Monetary(string="Total Amount", compute='_compute_total_invoice_amount')
    total_profit_amount = fields.Monetary(string="Total Profit", compute='_compute_total_profit_amount')


    def _default_currency_id(self):
        return self.env.user.company_id.currency_id


    @api.depends('date_from', 'date_to', 'total_expense_amount', 'total_invoice_amount', 'total_profit_amount')
    def _compute_total_invoice_amount(self):
        for rec in self:
            total_amount = 0

            invoices = self.env['account.move'].search([
                ('invoice_user_id.employee_id', '=', rec.employee_id.id),
                ('move_type', '=', 'out_invoice'),
                ('invoice_date', '>=', rec.date_from),
                ('invoice_date', '<=', rec.date_to)
                # ('payment_state', '=', 'paid')
            ])

            for invoice in invoices:
                payments = self.env['account.payment'].search(
                    [
                     ('memo', '=', invoice.name),
                     ('state', '=', 'paid'),
                     ('date', '>=', rec.date_from),
                     ('date', '<=', rec.date_to)], limit=1)

                print('invoice_____', invoice.name)
                if payments:
                    for payment in payments:
                        if payment.amount:
                            print('payment......', payment.name)
                            total_amount += payment.amount
                            print('\n')

            if total_amount:
                rec.total_invoice_amount = total_amount
            else:
                rec.total_invoice_amount = False






    @api.depends('employee_id','total_invoice_amount', 'total_expense_amount', 'total_profit_amount')
    def _compute_total_profit_amount(self):
        for rec in self:
            if rec.employee_id and rec.total_invoice_amount and rec.total_expense_amount:

                rec.total_profit_amount = rec.total_invoice_amount - rec.total_expense_amount

            elif rec.employee_id and rec.total_invoice_amount and not rec.total_expense_amount:
                rec.total_profit_amount = rec.total_invoice_amount

            else:
                rec.total_profit_amount = False



    @api.model
    def create(self, values):
        if values.get('name', _('New')) == _('New'):
            values['name'] = self.env['ir.sequence'].next_by_code('employee.performance.tracking') or _('New')
        res = super(EmployeePerformanceTracking, self).create(values)
        return res



    # @api.constrains('date')
    # def _check_unique_date(self):
    #     for rec in self:
    #         existing_orders = self.search([('employee_id', '=', rec.employee_id.id),('date_from', '=', rec.date_from),('date_to', '=', rec.date_to)])
    #         if existing_orders:
    #             raise ValidationError(_('Already Record Exist With Same Date Range for ', rec.employee_id.name))
    #
