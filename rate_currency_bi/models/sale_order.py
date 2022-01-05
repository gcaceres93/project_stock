#-*- coding: utf-8 -*-

from odoo import models, fields, api


class sale_order_bi(models.Model):
    _inherit = 'sale.order'

#     diferencia_moneda = fields.Monetary(store=True, readonly=True, compute='_compute_diferecia_moneda')

#     @api.depends('currency_id','amount_untaxed')
#     def _compute_diferecia_moneda(self):
#         for rec in self:
#             if rec.currency_id.id == 3:
#                 rec.diferencia_moneda = rec.amount_untaxed
#             else:
#                 if rec.amount_untaxed > 0 and rec.currency_id.rate_bi > 0:
#                     rec.diferencia_moneda = rec.amount_untaxed / rec.currency_id.rate_bi
    
    def calcula_cambio(self):
        _logger.info("#######calcula_cambio######")
            #campo type o inv
            # in_invoice = Factura de Proveedor
            # out_invoice = Factura de Cliente
            # in_refund = Nota de Credito emitida por Proveedor
            # out_refund = Nota de Credito enviada al cliente
            # if rec.invoice_id.type == 'out_invoice':
            # moneda = rec.env['res.currency'].search([('id','=',3)])
        list_obj = self.env['account.invoice.line'].search([])
        for rec in list_obj:
            if rec.currency_id:
                _logger.info(rec.currency_id.id)
                _logger.info("#####if rec.currency_id:#####")
                _logger.info(rec.invoice_id.id)
                if rec.invoice_id.date_invoice:

                    if rec.currency_id.id == 3:
                        rec.diferencia_moneda = rec.price_subtotal
                            
                    else:
#                         if rec.invoice_id.currency_rate:
#                             rec.diferencia_moneda = rec.price_subtotal / rec.invoice_id.currency_rate
                         tasa_moneda = rec.env['res.currency.rate'].search([('currency_id', '=', 3),
                                                                              ('name', '=',rec.invoice_id.date_invoice)])

                         if tasa_moneda and tasa_moneda.rate:
                              _logger.info("#######tasa_moneda and tasa_moneda.rate######")
                              round_curr = rec.currency_id.round
                              inverse_rate = round_curr(1/tasa_moneda.rate)
                              _logger.info(inverse_rate)
                              rec.diferencia_moneda = rec.price_subtotal / inverse_rate





