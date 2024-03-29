# -*- coding: utf-8 -*-
from odoo import fields, models, exceptions, api , _
from datetime import datetime, timedelta
from lxml import etree
from odoo.exceptions import ValidationError


class Project(models.Model):
    _inherit = 'project.project'

    location_src_id = fields.Many2one('stock.location','Source Location')
    location_dest_id = fields.Many2one('stock.location','Destination location')

class ProjectTaskType(models.Model):
    _inherit = 'project.task.type'

    consume_material = fields.Boolean(string="Consume material", help="Mark if this stage consume material stock")

class Task(models.Model):
    _inherit = 'project.task'


    @api.depends('material_stock_ids.stock_move_id')
    def _compute_stock_move(self):
        for task in self:
            task.stock_move_ids = task.mapped('material_stock_ids.stock_move_id')

    @api.depends('material_stock_ids.analytic_line_id')
    def _compute_analytic_line(self):
        for task in self:
            task.analytic_line_ids = task.mapped(
                'material_stock_ids.analytic_line_id')

    @api.depends('stock_move_ids.state')
    def _compute_stock_state(self):
        for task in self:
            if not task.stock_move_ids:
                task.stock_state = 'pending'
            else:
                states = task.mapped("stock_move_ids.state")
                for state in ("confirmed", "assigned", "done"):
                    if state in states:
                        task.stock_state = state
                        break

    stock_move_ids = fields.Many2many(
        comodel_name='stock.move',
        compute='_compute_stock_move',
        string='Stock Moves',
    )
    analytic_account_id = fields.Many2one(
        comodel_name='account.analytic.account',
        string='Analytic Account',
        help='Move created will be assigned to this analytic account',
    )
    analytic_line_ids = fields.Many2many(
        comodel_name='account.analytic.line',
        compute='_compute_analytic_line',
        string='Analytic Lines',
    )
    consume_material = fields.Boolean(
        related='stage_id.consume_material',
    )
    stock_state = fields.Selection(
        selection=[
            ('pending', 'Pending'),
            ('confirmed', 'Confirmed'),
            ('assigned', 'Assigned'),
            ('done', 'Done')],
        compute='_compute_stock_state',
    )
    location_source_id = fields.Many2one(
        comodel_name='stock.location',
        string='Source Location',
        index=True,
        related='project_id.location_src_id',
        help='Default location from which materials are consumed.',
    )
    location_dest_id = fields.Many2one(
        comodel_name='stock.location',
        string='Destination Location',
        index=True,
        related='project_id.location_dest_id',
        help='Default location to which materials are consumed.',
    )

    material_stock_ids = fields.One2many('project.task.stock','task_id',copy=True)


    def unlink_stock_move(self):
        res = False
        moves = self.mapped('stock_move_ids')
        moves_done = moves.filtered(lambda r: r.state == 'done')
        if not moves_done:
            moves.filtered(lambda r: r.state == 'assigned')._do_unreserve()
            moves.filtered(
                lambda r: r.state in {'waiting', 'confirmed', 'assigned'}
            ).write({'state': 'draft'})
            res = moves.unlink()
        return res

    def write(self, vals):
        res = super(Task, self).write(vals)
        for task in self:
            if 'stage_id' in vals:
                if task.stage_id.consume_material:
                    if not task.stock_move_ids:
                        task.material_stock_ids.create_stock_move()
                        task.material_stock_ids.create_analytic_line()
                else:
                    if task.unlink_stock_move():
                        if task.material_stock_ids.mapped(
                                'analytic_line_id'):
                            raise exceptions.Warning(
                                _("You can't move to a not consume stage if "
                                  "there are already analytic lines")
                            )
                    task.material_stock_ids.mapped('analytic_line_id').unlink()
        return res

    def unlink(self):
        self.unlink_stock_move()
        self.mapped('analytic_line_ids').unlink()
        return super(Task, self).unlink()

    def action_assign(self):
        self.mapped('stock_move_ids')._action_assign()

    def action_done(self):
        for move in self.mapped('stock_move_ids'):
            move.quantity_done = move.product_uom_qty
        self.mapped('stock_move_ids')._action_done()

class ProjectTaskStock(models.Model):

    _name = 'project.task.stock'

    task_id = fields.Many2one('project.task','Task')
    product_id = fields.Many2one('product.product', 'Product')
    quantity = fields.Integer(string="Quantity")
    stock_move_id = fields.Many2one(
        comodel_name='stock.move',
        string='Stock Move',
    )
    analytic_line_id = fields.Many2one(
        comodel_name='account.analytic.line',
        string='Analytic Line',
    )
    product_uom_id = fields.Many2one(
        comodel_name='product.uom',
        oldname="product_uom",
        string='Unit of Measure',
    )

    @api.onchange('product_id')
    def _onchange_product_id(self):
        self.product_uom_id = self.product_id.uom_id.id
        return {'domain': {'product_uom_id': [
            ('category_id', '=', self.product_id.uom_id.category_id.id)]}}

    def _prepare_stock_move(self):
        product = self.product_id
        res = {
            'product_id': product.id,
            'name': product.partner_ref,
            'state': 'confirmed',
            'product_uom': self.product_uom_id.id or product.uom_id.id,
            'product_uom_qty': self.quantity,
            'origin': self.task_id.name,
            'location_id':
                self.task_id.location_source_id.id or
                self.task_id.project_id.location_source_id.id or
                self.env.ref('stock.stock_location_stock').id,
            'location_dest_id':
                self.task_id.location_dest_id.id or
                self.task_id.project_id.location_dest_id.id or
                self.env.ref('stock.stock_location_customers').id,
        }
        return res

    def create_stock_move(self):
        for line in self:
            move_id = self.env['stock.move'].create(
                line._prepare_stock_move())
            line.stock_move_id = move_id.id

    def _prepare_analytic_line(self):
        product = self.product_id
        company_id = self.env['res.company']._company_default_get(
            'account.analytic.line')
        analytic_account = getattr(self.task_id, 'analytic_account_id', False) \
                           or self.task_id.project_id.analytic_account_id
        res = {
            'name': self.task_id.name + ': ' + product.name,
            'ref': self.task_id.name,
            'product_id': product.id,
            'unit_amount': self.quantity,
            'account_id': analytic_account.id,
            'user_id': self._uid,
            'product_uom_id': self.product_uom_id.id,
        }
        amount_unit = self.product_id.standard_price
        amount = amount_unit * self.quantity or 0.0
        result = round(amount, company_id.currency_id.decimal_places) * -1
        res.update({'amount': result})
        return res

    def create_analytic_line(self):
        for line in self:
            move_id = self.env['account.analytic.line'].sudo().create(
                line._prepare_analytic_line())
            move_id.amount = (line.product_id.standard_price * line.quantity or 0.0) * -1
            line.analytic_line_id = move_id.id
