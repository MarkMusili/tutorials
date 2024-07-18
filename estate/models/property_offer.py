from odoo import models, fields

class PropertyOffer(models.Model):
    """
    Property Offer Model
    """
    _name = "estate.property.offer"
    _description = "Real Estate Property Offer"

    price = fields.Float()
    status = fields.Selection([
        ('accepted', 'Accepted'),
        ('refused', 'Refused'),
    ], string="Status", copy=False)
    partner_id = fields.Many2one('res.partner', string="Partner",required=True)
    property_id = fields.Many2one('estate.property', required=True)