from odoo import models, fields


class PropertyTag(models.Model):
    """
    Model for property tags
    """
    _name = "estate.property.tag"
    _description = "Real Estate Property Tag"
    _order = "name"

    name = fields.Char(required=True)
    color = fields.Integer()

    _sql_constraints = [
        ('check_name_unique', 'UNIQUE(name)', 'Tag name must be unique')
    ]