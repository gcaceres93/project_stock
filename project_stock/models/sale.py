# -*- coding: utf-8 -*-
from odoo import fields, models, exceptions, api , _
from datetime import datetime, timedelta
from lxml import etree
from odoo.exceptions import ValidationError


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    project = fields.Boolean(string="Project integration", help="Mark if this sale order have project integration")
    project_type = fields.Selection([('new','Generate new project'),('add','Add to already created project')],default="new")
    project_id = fields.Many2one('project.project','Project')
    project_stock = fields.Boolean(string="Stock Integration",help="Mark if this sale order have integration with stock pickings and a relation with the execution of task material consume",default=True)
    project_task_create = fields.Boolean(string="Create task", help="Mark if this sale order needs to create a task with all material related on the stock picking")

    @api.multi
    def action_confirm(self):
        for rec in self:
            sale =super(SaleOrder, self).action_confirm()
            ######## PROJECT CREATION #######
            if rec.project:
                if rec.project_type == 'new':
                    analytic_account_id = self._create_analytic_account()
                    project_obj = self.env['project.project']
                    data = {
                        'name' : rec.name,
                        'label_tasks' : _('Tasks'),
                        'user_id' :  self.env.user.id,
                        'analytic_account_id' : analytic_account_id.id,
                        'privacy_visibility' : 'portal',
                        'partner_id' : rec.partner_id.id,
                        'alias_contact' : 'everyone',
                        'sale_order_id' : rec.id
                    }
                    project_id = project_obj.create(data)
            ######## PICKING AND PICKING TYPE PROCEDURE CREATION #######
                if rec.project_stock:
                    picking_type_obj = self.env['stock.picking.type']
                    stock_location_obj = self.env['stock.location']
                    stock_picking_obj = self.env['stock.picking']
                    sequence_id = self.generate_reserve_operation_sequence()
                    default_location_src_id = picking_type_obj.search([('code','=','incoming'),('warehouse_id','=',rec.warehouse_id.id)])[0].default_location_dest_id
                    default_location_dest_id = default_location_src_id.copy(default={'name': _('Reserve ') + str(rec.partner_id.name)+ ' ' +str(rec.name)}) #RESERVE LOCATION CREATION
                    partner_location_id = default_location_src_id.copy(default={'name' : _('Project ') + str(rec.partner_id.name)+' ' + str(rec.name)}) #LOCATION FOR  CUSTOMER PROJECT
                    partner_consume_location_id = default_location_src_id.copy(default={'name' : _('Consume ') + str(rec.partner_id.name) + ' ' + str(rec.name),'usage' : 'customer'}) #LOCATION FOR CUSTOMER PROJECT CONSUME
                    project_id.location_src_id = partner_location_id
                    project_id.location_dest_id = partner_consume_location_id

                    data1 = { #DATA FOR CREATION OF PICKING TYPE RESERVE
                        'name' : _('Reserve ') + str(rec.partner_id.name) + ' ' + str(rec.name),
                        'code' : 'internal',
                        'show_reserved' : True,
                        'sequence_id' : sequence_id.id,
                        'default_location_src_id' : default_location_src_id.id,
                        'default_location_dest_id' : default_location_dest_id.id
                    }

                    data2 = {  # DATA FOR CREATION OF PICKING TYPE FOR CUSTOMER PROJECT
                        'name': _('Project ') + str(rec.partner_id.name) + ' ' + str(rec.name),
                        'code': 'internal',
                        'show_reserved': True,
                        'sequence_id': sequence_id.id,
                        'default_location_src_id': default_location_dest_id.id,
                        'default_location_dest_id': partner_location_id.id
                    }

                    picking_type_reserve_id = picking_type_obj.create(data1)
                    picking_type_project_id = picking_type_obj.create(data2)

                    sale_picking_id = stock_picking_obj.search([('sale_id','=',rec.id)]) #search and update the sale picking
                    picking_id= None
                    if len(sale_picking_id) > 1:
                        raise ValidationError(_('Cannot confirm a sale order with project/stock integration with more than one picking associated'))
                    else:
                        if len(sale_picking_id) == 1:
                            picking_id = sale_picking_id[0]
                    if picking_id: #UPDATE THE SALE PICKING
                        picking_id.partner_id = None
                        picking_id.picking_type_id.sequence_id.number_next_actual =  picking_id.picking_type_id.sequence_id.number_next_actual - 1
                        picking_id.picking_type_id = picking_type_reserve_id.id
                        picking_id.location_dest_id = default_location_dest_id.id
                        picking_id.action_assign()
                        stock_move_line_ids = self.env['stock.move.line'].search([('picking_id','=',picking_id.id)])
                        stock_move_ids = self.env['stock.move'].search([('picking_id','=',picking_id.id)])
                        if len(stock_move_ids) > 0:
                            for sm in stock_move_ids:
                                sm.location_dest_id = default_location_dest_id
                        if len(stock_move_line_ids) > 0 :
                            for stml in stock_move_line_ids:
                                stml.location_dest_id = default_location_dest_id
                        picking_id.name = sequence_id._next()
                        if project_id:
                            picking_id.project_id = project_id
                            if rec.project_task_create:
                                materials = list()
                                task_obj = self.env['project.task']
                                material_stock_obj = self.env['project.task.stock']
                                task_data={
                                    'name' : 'First project task',
                                    'user_id' : rec.user_id.id,
                                    'project_id' : project_id.id
                                }
                                task_id = task_obj.create(task_data)
                                for move in picking_id.move_ids_without_package:
                                    if move.product_id:
                                        material_stock_data = {
                                            'task_id' : task_id.id,
                                            'product_id' : move.product_id.id,
                                            'quantity' : 0
                                        }
                                        task_id.material_stock_ids = (0,0, material_stock_data)
            return sale

    @api.multi
    def generate_reserve_operation_sequence(self):
        sequence_obj = self.env['ir.sequence']
        data = {
            'name' : _('Reserve ') + str(self.partner_id.name) + ' Sequence',
            'prefix' : 'RES/'+str(self.partner_id.name)+'/',
            'padding' : 4,
            'code' : _('reserve.') + str(self.partner_id.name) + '.sequence',
            'number_increment' : 1,
            'active': True,
            'implementation' : 'no_gap'
        }
        sequence_id = sequence_obj.create(data)
        if sequence_id:
            return sequence_id

    @api.multi
    def _create_analytic_account(self):
        sequence_obj = self.env['account.analytic.account']
        data = {
            'name' : self.name,
            'partner_id' : self.partner_id.id,
        }
        analytic_account_id = sequence_obj.create(data)
        return analytic_account_id


