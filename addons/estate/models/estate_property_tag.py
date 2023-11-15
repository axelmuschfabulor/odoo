from odoo import fields,models

class EstateTest(models.Model):
    _name = "estate.property.tag"
    _description = "Property tags"

    name = fields.Char(required = True)


    _sql_constraints = [
        (
            'unique_name',
            'UNIQUE(name)',
            'name needs to be unique',
        ),
    ]
