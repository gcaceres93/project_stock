#-*- coding: utf-8 -*-

from odoo import models, fields, api


class sale_order_bi(models.Model):
    _inherit = 'sale.order'

    diferencia_moneda = fields.Monetary(store=True, readonly=True, compute='_compute_diferecia_moneda')

    @api.depends('currency_id','amount_untaxed')
    def _compute_diferecia_moneda(self):
        for rec in self:
            if rec.currency_id.id == 3:
                rec.diferencia_moneda = rec.amount_untaxed
            else:
                if rec.amount_untaxed > 0:
                    rec.diferencia_moneda = rec.currency_id.rate_bi / rec.amount_untaxed





