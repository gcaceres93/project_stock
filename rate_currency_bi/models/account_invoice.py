#-*- coding: utf-8 -*-

from odoo import models, fields, api
import logging

_logger = logging.getLogger(__name__)


class account_invoice_bi(models.Model):
    _inherit = 'account.invoice.line'

    diferencia_moneda = fields.Monetary(store=True, compute='_compute_diferecia_moneda')

    @api.one
    @api.depends('price_subtotal','quantity','invoice_line_tax_ids')
    def _compute_diferecia_moneda(self):
#         _logger.info("#######_compute_diferecia_moneda######")
            #campo type o inv
            # in_invoice = Factura de Proveedor
            # out_invoice = Factura de Cliente
            # in_refund = Nota de Credito emitida por Proveedor
            # out_refund = Nota de Credito enviada al cliente
            # if rec.invoice_id.type == 'out_invoice':
            # moneda = rec.env['res.currency'].search([('id','=',3)])
        for rec in self:
            if rec.currency_id:
                if rec.invoice_id.date_invoice:

                    if rec.currency_id.id == 3:
                        rec.diferencia_moneda = rec.price_subtotal
                            
                    else:
                        if rec.invoice_id.currency_rate:
                            rec.diferencia_moneda = rec.price_subtotal / rec.invoice_id.currency_rate
#                         tasa_moneda = rec.env['res.currency.rate'].search([('currency_id', '=', 3),
                                                                             ('name', '=',rec.invoice_id.date_invoice)])

#                         if tasa_moneda and tasa_moneda.rate:
#                              round_curr = rec.currency_id.round
#                              inverse_rate = round_curr(1/tasa_moneda.rate)
#                              rec.diferencia_moneda = rec.price_subtotal / inverse_rate
                        

