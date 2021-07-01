#-*- coding: utf-8 -*-

from odoo import models, fields, api


class rate_currency_bi(models.Model):
    _inherit = 'res.currency'

    rate_bi = fields.Float(compute='_compute_current_rate_bi', string='Current Rate', digits=(12, 6),
                        help='The rate of the currency to the currency of rate 1.', store=True)

    # @api.depends('rate')
    # def _compute_current_rate_bi(self):
    #     date = self._context.get('date') or fields.Date.today()
    #     company = self.env['res.company'].browse(self._context.get('company_id')) or self.env['res.users']._get_company()
    #     # the subquery selects the last rate before 'date' for the given currency/company
    #     currency_rates = self._get_rates(company, date)
    #     for currency in self:
    #         currency.rate_bi = currency_rates.get(currency.id) or 1.0

    @api.multi
    @api.depends('rate_ids.rate')
    def _compute_current_rate_bi(self):
        date = self._context.get('date') or fields.Date.today()
        company_id = self._context.get('company_id') or self.env['res.users']._get_company().id
        # the subquery selects the last rate before 'date' for the given currency/company
        query = """SELECT c.id, (SELECT r.rate FROM res_currency_rate r
                                     WHERE r.currency_id = c.id AND r.name <= %s
                                       AND (r.company_id IS NULL OR r.company_id = %s)
                                  ORDER BY r.company_id, r.name DESC
                                     LIMIT 1) AS rate
                      FROM res_currency c
                      WHERE c.id IN %s"""
        self._cr.execute(query, (date, company_id, tuple(self.ids)))
        currency_rates = dict(self._cr.fetchall())
        for currency in self:
            currency.rate_bi = currency_rates.get(currency.id) or 1.0