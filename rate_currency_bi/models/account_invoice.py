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
        _logger.info("#######_compute_diferecia_moneda######")
        #campo type o inv
        # in_invoice = Factura de Proveedor
        # out_invoice = Factura de Cliente
        # in_refund = Nota de Credito emitida por Proveedor
        # out_refund = Nota de Credito enviada al cliente
        # if rec.invoice_id.type == 'out_invoice':
        # moneda = rec.env['res.currency'].search([('id','=',3)])
        for rec in self:
            if rec.currency_id:
                _logger.info(rec.currency_id.id)
                _logger.info("#####if rec.currency_id:#####")
                _logger.info(rec.invoice_id.id)
                if rec.invoice_id.date_invoice:
                    if rec.currency_id.id == 2:
                        rec.diferencia_moneda = rec.price_subtotal
                            
                    else:
                         tasa_moneda = rec.env['res.currency.rate'].search([('currency_id', '=', 2),
                                                                              ('name', '=',rec.invoice_id.date_invoice)])

                         if tasa_moneda and tasa_moneda.set_venta:
                              _logger.info("#######tasa_moneda and tasa_moneda.set_venta######")
                              rec.diferencia_moneda = rec.price_subtotal / tasa_moneda.set_venta
