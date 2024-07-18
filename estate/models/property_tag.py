from odoo import models, fields


class PropertyTag(models.Model):
    """
    Model for property tags
    """
    _name = "estate.property.tag"
    _description = "Real Estate Property Tag"

    name = fields.Char(required=True)