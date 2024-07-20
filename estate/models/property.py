from odoo import models, fields, api, exceptions
from datetime import timedelta
class Property(models.Model):
    """Model for properties"""
    _name = 'estate.property'
    _description = 'Real Estate Properties'

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(copy=False, default=fields.Date.today() + timedelta(days=30))
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection([
        ('north', 'North'),
        ('south', 'South'),
        ('east', 'East'),
        ('west', 'West')
    ])
    active = fields.Boolean(default=True)
    state = fields.Selection([
        ('new', 'New'),
        ('offer_received', 'Offer Received'),
        ('offer_accepted', 'Offer Accepted'),
        ('sold', 'Sold'),
        ('canceled', 'Canceled')
    ], default='new', copy=False)

    property_type_id = fields.Many2one('estate.property.type', string='Property Type')
    salesperson_id = fields.Many2one('res.users', string='Salesperson', default=lambda self: self.env.user)
    buyer_id = fields.Many2one('res.partner', string='Buyer', copy=False)
    tag_ids = fields.Many2many('estate.property.tag', string='Tags')
    offer_ids = fields.One2many('estate.property.offer', 'property_id', string='Offers')

    total_area = fields.Float(compute='_compute_total_area')

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        """Find the area of the whole property"""
        for record in self:
            record.total_area = record.living_area + record.garden_area

    best_price = fields.Float(compute="_compute_best_price")

    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        """Find the highest price offer"""
        for record in self:
            if len(record.offer_ids) > 0:
                record.best_price = max(record.offer_ids.mapped('price'))
            else:
                record.best_price = 0

    #onchange for garden
    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = 0
            self.garden_orientation = False

    def action_sell_property(self):
        """Change state to sold and set selling price"""
        for record in self:
            if record.state == 'canceled':
                raise exceptions.UserError("You cannot sell a canceled property")
            record.state = 'sold'
        return True

    def action_cancel_property(self):
        """Change state to canceled"""
        for record in self:
            if record.state == 'sold':
                raise exceptions.UserError("You cannot cancel a sold property")
            record.state = 'canceled'
        return True
