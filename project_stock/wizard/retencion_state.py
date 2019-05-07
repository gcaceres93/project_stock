# -*- coding: utf-8 -*-
from odoo import fields, models, exceptions, api, _
from datetime import datetime, timedelta
from lxml import etree
from odoo.exceptions import ValidationError,UserError

class retenciones_confirm_action(models.TransientModel):
    """
    This wizard will confirm the all the selected draft invoices
    """

    _name = "tesaka.retenciones.confirm"
    _description = "Vincular las retenciones seleccionadas a las facturas"

    @api.multi
    def retenciones_confirm(self):
        context = dict(self._context or {})
        active_ids = context.get('active_ids', []) or []
        retenciones_list = list()
        aux = ""
        for record in self.env['tesaka.retenciones'].browse(active_ids):
            # if not record.vinculado:
                factura = self.env['account.invoice'].search([['nro_factura', '=', record.factura]])
                proveedor = self.env['res.partner'].search([['ruc', '=', record.ruc]])
                # proveedor = self.env['res.partner'].browse(record.retenido.id)
                if factura and proveedor:
                    record.vinculado = True
                    record.factura_vinculada = factura.id
                    record.retenido = proveedor.id
                    ops = self.env['account.orden.pago'].search([['partner_id', '=', proveedor.id]])
                    for op in ops:
                        op.retenciones_asociadas = [(5,)]
                        for fac in op.orden_pagos_facturas_ids:
                            if ((fac.invoice_id.nro_factura == factura.nro_factura) and (fac.invoice_id.timbrado == record.timbrado)):
                                retenciones_list.append(record.id)
                                # aux += record
                        # raise UserError(_(aux))
                        if len(retenciones_list) > 0:
                            op.retenciones_asociadas = [(6, 0, retenciones_list)]
        return {'type': 'ir.actions.act_window_close'}