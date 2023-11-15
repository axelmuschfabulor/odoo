from odoo import fields,models

class EstateTest(models.Model):
    _name = "estate.property.type"
    _description = "Nice description here."

    name = fields.Char(required = True)

    line_ids = fields.One2many("estate.property.type.line", "model_id")

    _sql_constraints = [
            (
                'unique_name',
                'UNIQUE(name)',
                'name needs to be unique',
            ),
        ]
    
class EstateTestLine(models.Model):
    _name = "estate.property.type.line"
    _description = "Test Model Line"

    model_id = fields.Many2one("estate.property.type")
    field_1 = fields.Char()
    field_2 = fields.Char()
    field_3 = fields.Char()