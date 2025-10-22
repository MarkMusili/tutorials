from odoo import models, fields, api
from odoo.exceptions import ValidationError

class PropertyTag(models.Model):
    """
    Model for property tags
    """
    _name = "estate.property.tag"
    _description = "Real Estate Property Tag"
    _order = "name"

    name = fields.Char(required=True)
    color = fields.Integer()

    @api.constrains('name')
    def _check_tag_name_unique(self):
        for record in self:
            if self.env['estate.property.type'].search([('name', '=', record.name), ('id', '!=', record.id)]):
                raise ValidationError("Tag name must be unique")