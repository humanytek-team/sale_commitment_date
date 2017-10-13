# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from openerp import api

class sale_order(models.Model):
    _inherit = 'sale.order'


    commitment_date = fields.Datetime('Commitment date')