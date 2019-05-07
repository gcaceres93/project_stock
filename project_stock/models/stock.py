# -*- coding: utf-8 -*-
from odoo import fields, models, exceptions, api , _
from datetime import datetime, timedelta
from lxml import etree
from odoo.exceptions import ValidationError


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    project_id = fields.Many2one('project.project','Project')