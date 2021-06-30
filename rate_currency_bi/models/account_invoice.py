#-*- coding: utf-8 -*-

from odoo import models, fields, api


class account_invoice_bi(models.Model):
    _inherit = 'account.invoice.line'

    diferencia_moneda = fields.Monetary(store=True, readonly=True, compute='_compute_diferecia_moneda')

    @api.depends('currency_id','price_subtotal')
    def _compute_diferecia_moneda(self):
        for rec in self:
            #campo type o inv
            # in_invoice = Factura de Proveedor
            # out_invoice = Factura de Cliente
            # in_refund = Nota de Credito emitida por Proveedor
            # out_refund = Nota de Credito enviada al cliente
            # if rec.invoice_id.type == 'out_invoice':
            if rec.currency_id.id == 3:
                rec.diferencia_moneda = rec.price_subtotal
            else:
                if rec.price_subtotal != 0:
                    rec.diferencia_moneda = rec.price_subtotal / rec.currency_id.rate_bi





