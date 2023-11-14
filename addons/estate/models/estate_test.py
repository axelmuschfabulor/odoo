from odoo import api,fields,models
from odoo.tools import date_utils
from odoo.exceptions import UserError
class EstateTest(models.Model):
    _name = "estate.test"
    _description = "Nice description here."

    name = fields.Char(required = True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(copy = False, default = lambda self: fields.date.today() + date_utils.relativedelta(months=3))
    expected_price = fields.Float(required = True)
    selling_price = fields.Float(readonly = True, copy = False)
    bedrooms = fields.Integer(default = 2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        string='Garden Orientation',
        selection=[('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')],
        help="Choose the direction of the garden")
    active = True
    state = fields.Selection(
        string = 'State',
        selection=[('new', 'New'), ('offer_received', 'Offer received'), ('offer_approved', 'offer Approved'), ('sold', 'Sold'),('canceled','Canceled')],
        copy = False,
        default="new",
        )
    property_type_id = fields.Many2one("estate.property.type", string="Property type")
    buyer_id = fields.Many2one("res.partner", string="Buyer")
    salesperson_id = fields.Many2one("res.users", string="Salesperson")
    tag_ids = fields.Many2many("estate.property.tag", string="Tags")
    offer_ids = fields.One2many("estate.property.offer","property_id")
    total_area = fields.Float(compute="_compute_total",string="Total area(m²)")
    best_price = fields.Float(compute="_compute_best_price",string="Best price")

    @api.depends("living_area","garden_area")
    def _compute_total(self):
        for record in self:
            record.total_area =  record.living_area + record.garden_area


    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for record in self:
            best_offer = self.mapped("offer_ids.price")
            if len(best_offer) > 0:
                record.best_price =  max(best_offer)
            else:
                record.best_price =  0

    @api.onchange("garden")
    def _onchange_partner_id(self):
        if self.garden == True:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = ''
            self.garden_orientation = ''



    def estate_property_sold(self):
        for record in self:
            print("sold pressed " + record.state)
            if record.state == "canceled":
                raise UserError("Canceled properties cannot be sold")
            else:
                record.state = "sold"
        return True
    def estate_property_cancel(self):
        for record in self:
            if record.state == "sold":
                raise UserError("Sold properties cannot be canceled")
            else:
                record.state = "canceled"
        return True
    def estate_property_login(self):
        print("Login")
        return True