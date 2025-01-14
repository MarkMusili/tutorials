from odoo import models, fields, api, exceptions
from datetime import timedelta
from odoo.tools.float_utils import float_compare, float_is_zero
from odoo.exceptions import ValidationError
class Property(models.Model):
    """Model for properties"""
    _name = 'estate.property'
    _description = 'Real Estate Properties'
    _id = "id desc"

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
    offer_count = fields.Integer(compute='_compute_offer_count', string='Number of Offers')
    salesperson_id = fields.Many2one('res.users', string='Salesperson' )

    @api.depends('offer_ids')
    def _compute_offer_count(self):
        """Compute the number of offers for each property"""
        for record in self:
            record.offer_count = len(record.offer_ids)
    salesperson_id = fields.Many2one('res.users', string='Salesperson', default=lambda self: self.env.user)
    buyer_id = fields.Many2one('res.partner', string='Buyer', copy=False)
    tag_ids = fields.Many2many('estate.property.tag', string='Tags')
    offer_ids = fields.One2many('estate.property.offer', 'property_id', string='Offers')
    # property_type_id = fields.Many2one('estate.property.type', string='Property Type')

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


    def action_sold(self):
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

    _sql_constraints = [
        ('check_expected_price', 'CHECK(expected_price >= 0)', 'The expected price must be strictly positive'),
        ('check_selling_price', 'CHECK(selling_price >= 0)', 'The selling price must be positive')
    ]

    @api.constrains('expected_price', 'selling_price')
    def _check_selling_price(self):
        """Ensure the offer price is not less than 90% of selling price"""
        for record in self:
            if not float_is_zero(record.selling_price, precision_digits=2):
                expected_90_percent = record.expected_price * 0.9
                if float_compare(record.selling_price, expected_90_percent, precision_digits=2) < 0:
                    raise ValidationError("The selling price cannot be lower than 90% of the expected price. You must lower the expected price if you want to accept this offer.")

    @api.ondelete(at_uninstall=False)
    def _unlink_if_state_not_new_canceled(self):
        """Delete all offers when deleting a property"""
        for record in self:
            if record.state not in ['new', 'canceled']:
                raise exceptions.UserError("You cannot delete a property that is not new or canceled")
            record.offer_ids.unlink()

    @api.model
    def create(self, vals):
        if vals.get['state'] == 'new':
            vals['state'] == 'offer_received'
        return super(Property, self).create(vals)