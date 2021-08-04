#-*- coding: utf-8 -*-

from odoo import models, fields, api
import logging

_logger = logging.getLogger(__name__)


class account_invoice_bi(models.Model):
    _inherit = 'account.invoice.line'

    diferencia_moneda = fields.Monetary(store=True, readonly=True, compute='_compute_diferecia_moneda')

    @api.depends('price_subtotal')
    def _compute_diferecia_moneda(self):
        _logger.info("#######_compute_diferecia_moneda######")
            #campo type o inv
            # in_invoice = Factura de Proveedor
            # out_invoice = Factura de Cliente
            # in_refund = Nota de Credito emitida por Proveedor
            # out_refund = Nota de Credito enviada al cliente
            # if rec.invoice_id.type == 'out_invoice':
            # moneda = rec.env['res.currency'].search([('id','=',3)])

        if self.invoice_id.currency_id:
            factura = self.env['account.invoice'].search([('id','=',self.invoice_id.id)])
            if factura.date_invoice:
                _logger.info("#######moneda######")
                moneda = self.env['res.currency'].search([('id','=',self.invoice_id.currency_id.id)])
                _logger.info(moneda)
                if moneda and moneda.id == 3:
                    self.diferencia_moneda = self.price_subtotal
                    _logger.info("#######if moneda.id######")
                    _logger.info(moneda.id)
                elif moneda and moneda.id !=3:
                    _logger.info("#######elif moneda.id######")
                    _logger.info(moneda.id)
                    tasa_moneda = self.env['res.currency.rate'].search([('currency_id', '=', 3),
                                                                         ('name', '=',factura.date_invoice)])
                    _logger.info("#######tasa_moneda######")
                    _logger.info(tasa)

                        # if rec.currency_id.id == 3:
                        #     rec.diferencia_moneda = rec.price_subtotal
                        # else:
                        #     if rec.price_subtotal > 0 and rec.currency_id.rate_bi > 0:
                        # rec.diferencia_moneda = rec.price_subtotal / rec.currency_id.rate_bi
                    if tasa_moneda and tasa_moneda.inverse_rate:
                        self.diferencia_moneda = self.price_subtotal / tasa_moneda.inverse_rate
                    else:
                        self.diferencia_moneda = 0
                else:
                    self.diferencia_moneda = 0
            else:
                self.diferencia_moneda = 0
        else:
            self.diferencia_moneda = 0



