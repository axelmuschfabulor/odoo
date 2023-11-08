from odoo import api,fields,models
from odoo.tools import date_utils
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
            record.best_price =  max(self.mapped("offer_ids.price"))