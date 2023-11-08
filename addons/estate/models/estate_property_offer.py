from odoo import api,fields,models
from odoo.tools import date_utils

class EstateTest(models.Model):
    _name = "estate.property.offer"
    _description = "Nice offer here."

    price = fields.Float()
    status = fields.Selection(
        string = 'Status',
        selection=[('accepted', 'Accepted'), ('offer_received', 'Offer received')],
        copy = False,
        )

    salesperson_id = fields.Many2one("res.users", string="Salesperson", required = True)
    property_id = fields.Many2one("estate.test", string="Property", required = True)
    validity = fields.Integer(default="7")
    date_deadline = fields.Date(compute="_compute_date_deadline",inverse="_inverse_date_deadline",readonly=False)


    @api.depends("validity")
    def _compute_date_deadline(self):
            for record in self:
                record.date_deadline =  record.create_date+ date_utils.relativedelta(days=record.validity)
    @api.depends("date_deadline")
    def _inverse_date_deadline(self):
            for record in self:
                delta = record.date_deadline - record.create_date.date()  
                record.validity =  delta.days
                 