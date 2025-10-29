from odoo import models, fields


class UsersModel(models.Model):
    _inherit = "res.users"

    property_ids = fields.One2many('estate.property', 'salesperson_id', string='Salesperson', domain=[('state', '=', 'available')])