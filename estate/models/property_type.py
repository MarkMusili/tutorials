from odoo import fields, models

class PropertyType(models.Model):
    """Model for Property types"""
    _name = "estate.property.type"
    _description = "Real Estate Property Type"
    _order = "name"

    name = fields.Char(required=True)
    property_ids = fields.One2many('estate.property', 'property_type_id', string='Properties')

    _sql_constraints = [
        ('check_type_name_unique', 'UNIQUE(name)', 'Type name must be unique')
    ]