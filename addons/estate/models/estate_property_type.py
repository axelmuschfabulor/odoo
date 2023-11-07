from odoo import fields,models

class EstateTest(models.Model):
    _name = "estate.property.type"
    _description = "Nice description here."

    name = fields.Char(required = True)
