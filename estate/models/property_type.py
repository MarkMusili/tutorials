from odoo import fields, models, api

class PropertyType(models.Model):
    """Model for Property types"""
    _name = "estate.property.type"
    _description = "Real Estate Property Type"
    _order = "sequence, name"

    name = fields.Char(required=True)
    property_ids = fields.One2many('estate.property', 'property_type_id', string='Properties')
    sequence = fields.Integer()
    offer_ids = fields.One2many('estate.property.offer', 'property_type_id', string='Offers')
    offer_count = fields.Integer(compute='_compute_offer_count')

    @api.depends('offer_ids')
    def _compute_offer_count(self):
        """Compute the number of offers for each type"""
        for record in self:
            record.offer_count = len(record.offer_ids)

    _sql_constraints = [
        ('check_type_name_unique', 'UNIQUE(name)', 'Type name must be unique')
    ]