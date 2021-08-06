#-*- coding: utf-8 -*-

from odoo import models, fields, api
import logging

_logger = logging.getLogger(__name__)


class account_invoice_bi(models.Model):
    _inherit = 'account.invoice.line'

    diferencia_moneda = fields.Monetary(compute='_compute_diferecia_moneda',store=True)
    is_dolar = fields.Boolean(compute='compute_moneda_valor',store = True)
    
    @api.depends('currency_id')
    def compute_moneda_valor(self):
        for rec in self:
            if rec.currency_id and rec.currency_id.id == 3:
                rec.is_dolar = True
            else:
                rec.is_dolar = False
    
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
        for rec in self:
            if rec.invoice_id.currency_id:
                factura = rec.env['account.invoice'].search([('id','=',rec.invoice_id.id)])
                if factura.date_invoice:
                    _logger.info("#######moneda######")
                    moneda = rec.env['res.currency'].search([('id','=',rec.invoice_id.currency_id.id)])
                    _logger.info(moneda)
                    if moneda:
                       if rec.is_dolar:
                            rec.diferencia_moneda = rec.price_subtotal
                            #_logger.info("#######if moneda.id######")
                            #_logger.info(moneda.id)
                            #tasa_moneda = rec.env['res.currency.rate'].search([('currency_id', '=', 3),
                            #                                                    ('name', '=',factura.date_invoice)])

                            #_logger.info("#######tasa_moneda######")
                            #_logger.info(tasa_moneda)
                            #if tasa_moneda and tasa_moneda.rate:
                                #round_curr = rec.currency_id.roun
                                #inverse_rate = round_curr(1/tasa_moneda.rate)
                                #rec.diferencia_moneda = rec.price_subtotal / inverse_rate
                            #else:
                                #rec.diferencia_moneda = 0
                        else:
                        #if moneda.id != 3:
                            #rec.diferencia_moneda = rec.price_subtotal
                            _logger.info("#######elif moneda.id######")
                            _logger.info(moneda.id)
                            tasa_moneda = rec.env['res.currency.rate'].search([('currency_id', '=', 3),
                                                                             ('name', '=',factura.date_invoice)])

                            _logger.info("#######tasa_moneda######")
                            _logger.info(tasa_moneda)
                            if tasa_moneda and tasa_moneda.rate:
                                round_curr = rec.currency_id.roun
                                inverse_rate = round_curr(1/tasa_moneda.rate)
                                rec.diferencia_moneda = rec.price_subtotal / inverse_rate
                            else:
                                rec.diferencia_moneda = 0
                    else:
                        rec.diferencia_moneda = 0
                else:
                    rec.diferencia_moneda = 0
            else:
                rec.diferencia_moneda = 0



