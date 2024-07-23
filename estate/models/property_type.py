from odoo import fields, models

class PropertyType(models.Model):
    """Model for Property types"""
    _name = "estate.property.type"
    _description = "Real Estate Property Type"

    name = fields.Char(required=True)

    _sql_constraints = [
        ('check_type_name_unique', 'UNIQUE(name)', 'Type name must be unique')
    ]