from odoo import fields, models, api

class Property(models.Model):
    """Inherits from the real estate model"""
    _inherit = 'estate.property'

    def action_sold(self):
        """Overriding the sold action"""
        print('This is the sold action successfully overridden')

        commission = self.selling_price * 0.06
        admin_fee = 100.00

        self.env['account.move'].create({
            'partner_id': self.buyer_id.id,
            'move_type': 'out_invoice',
            'invoice_line_ids': [(0, 0, {
                'name': 'Commssion (6% of selling price)',
                'quantity': 1,
                'price_unit': commission,
            }),
            (0, 0, {
                'name': 'Admin Fee',
                'quantity': 1,
                'price_unit': admin_fee,
            })
            ],
        })

        return super(Property, self).action_sold()