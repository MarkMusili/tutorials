from odoo import models, fields, api
from datetime import timedelta, date


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
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(compute="_compute_date_deadline", inverse="_inverse_date_deadline")

    @api.depends('create_date', 'validity')
    def _compute_date_deadline(self):
        for record in self:
            record.date_deadline = (record.create_date if record.create_date else date.today()) + timedelta(days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            record.validity = (record.date_deadline - record.create_date.date()).days

    #Not sure if its working
    def _refuse_other_offers(self, property_id):
        """Refuse all other offers for the property."""
        for record in property_id.offer_ids:
            if record.status == 'accepted' and record.property_id != property_id:
                record.status = 'refused'

    def action_accept_offer(self):
        """Change state to Accepted"""
        for record in self:
            record.status = 'accepted'
            if record.property_id:
                self._refuse_other_offers(record.property_id)
                record.property_id.selling_price = record.price
                record.property_id.buyer_id = record.partner_id
        return True

    def action_refuse_offer(self):
        """Change state to Refused"""
        for record in self:
            record.status = 'refused'
        return True

    _sql_constraints = [
        ('check_price_positive', 'CHECK(price >= 0)', 'Offer Price must be strictly positive')
    ]
