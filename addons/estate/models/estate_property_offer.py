from odoo import api,fields,models
from odoo.tools import date_utils
from odoo.exceptions import UserError

class EstateTest(models.Model):
    _name = "estate.property.offer"
    _description = "Nice offer here."

    price = fields.Float()
    status = fields.Selection(
        string = 'Status',
        selection=[('accepted', 'Accepted'), ('offer_received', 'Offer received'), ('refused', 'Refused')],
        copy = False,
        )

    buyer_id = fields.Many2one("res.partner", string="Buyer")
    salesperson_id = fields.Many2one("res.users", string="Salesperson", required = True)
    property_id = fields.Many2one("estate.test", string="Property", required = True)
    validity = fields.Integer(default="7")
    date_deadline = fields.Date(compute="_compute_date_deadline",inverse="_inverse_date_deadline",readonly=False)

    _sql_constraints = [
            ('check_price', 'CHECK(price >= 0)',
            'The price needs to be possitive.')
        ]

    @api.depends("validity")
    def _compute_date_deadline(self):
            for record in self:
                if record.create_date:
                    record.date_deadline =  record.create_date+ date_utils.relativedelta(days=record.validity)
    @api.depends("date_deadline")
    def _inverse_date_deadline(self):
            for record in self:
                delta = record.date_deadline - record.create_date.date()  
                record.validity =  delta.days



    def estate_offer_accept(self):
        #set price buyer, etc only if there is no other accepted
        for record in self:
            has_accepted = False
            for offer in record.property_id.offer_ids:
                print(offer.price)
                if offer.status == "accepted":
                     has_accepted = True

            if has_accepted == True:
                 raise UserError("Property already has an accepted offer")
            else:
                record.status = 'accepted'
                record.property_id.selling_price = record.price
                record.property_id.buyer_id = record.buyer_id
                record.property_id.salesperson_id = record.salesperson_id
        return True     
     
    def estate_offer_refuse(self):
        #set status
        for record in self:
             record.status = 'refused'
        return True      