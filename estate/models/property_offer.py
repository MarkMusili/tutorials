from odoo import models, fields, api, exceptions
from datetime import timedelta, date


class PropertyOffer(models.Model):
    """
    Property Offer Model
    """
    _name = "estate.property.offer"
    _description = "Real Estate Property Offer"

    price = fields.Float()
    _order = 'price desc'
    status = fields.Selection([
        ('accepted', 'Accepted'),
        ('refused', 'Refused'),
    ], string="Status", copy=False)
    partner_id = fields.Many2one('res.partner', string="Partner",required=True)
    property_id = fields.Many2one('estate.property', required=True)
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(compute="_compute_date_deadline", inverse="_inverse_date_deadline")
    property_type_id = fields.Many2one(related="property_id.property_type_id", store=True)

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
        other_offers = self.env['estate.property.offer'].search([
            ('property_id', '=', property_id.id),
            ('status', '=', False)
        ])
        other_offers.write({'status': 'refused'})

    def action_accept_offer(self):
        """Change state to Accepted"""
        for record in self:
            record.status = 'accepted'
            if record.property_id:
                self._refuse_other_offers(record.property_id)
                record.property_id.selling_price = record.price
                record.property_id.buyer_id = record.partner_id
                record.property_id.state = 'offer_accepted'
        return True

    def action_refuse_offer(self):
        """Change state to Refused"""
        for record in self:
            record.status = 'refused'
        return True

    @api.model
    def create(self, vals):
        property_id = self.env['estate.property'].browse(vals.get('property_id'))
        if property_id.offer_ids and any(offer.price > vals['price'] for offer in property_id.offer_ids):
            raise exceptions.UserError("You cannot create an offer with a lower amount than an existing offer.")
        property_id.state = 'offer_received'
        return super(PropertyOffer, self).create(vals)

    _sql_constraints = [
        ('check_price_positive', 'CHECK(price >= 0)', 'Offer Price must be strictly positive')
    ]
