#-*- coding: utf-8 -*-

from odoo import models, fields, api


class account_invoice_bi(models.Model):
    _inherit = 'account.invoice.line'

    diferencia_moneda = fields.Monetary(store=True, readonly=True, compute='_compute_diferecia_moneda')

    @api.depends('price_subtotal')
    def _compute_diferecia_moneda(self):

            #campo type o inv
            # in_invoice = Factura de Proveedor
            # out_invoice = Factura de Cliente
            # in_refund = Nota de Credito emitida por Proveedor
            # out_refund = Nota de Credito enviada al cliente
            # if rec.invoice_id.type == 'out_invoice':
            # moneda = rec.env['res.currency'].search([('id','=',3)])
        if self.invoice_id.currency_id:
            if self.invoice_id.currency_id.id == 3:
                self.diferencia_moneda = self.price_subtotal
            elif self.invoice_id.currency_id.id != 3:
                factura = self.env['account.invoice'].search([('id','=',self.invoice_id.id)])
                if factura.date_invoice:
                    moneda = self.env['res.currency.rate'].search([('currency_id', '=', 3),
                                                                         ('name', '=',factura.date_invoice)])
                        # if rec.currency_id.id == 3:
                        #     rec.diferencia_moneda = rec.price_subtotal
                        # else:
                        #     if rec.price_subtotal > 0 and rec.currency_id.rate_bi > 0:
                        # rec.diferencia_moneda = rec.price_subtotal / rec.currency_id.rate_bi
                    if moneda and moneda.inverse_rate:
                        self.diferencia_moneda = self.price_subtotal / moneda.inverse_rate
                    else:
                        self.diferencia_moneda = self.price_subtotal
                else:
                    self.diferencia_moneda = self.price_subtotal
        else:
            self.diferencia_moneda = 0



