from odoo import fields, models


class PropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Tags of Real Estate Model"

    name = fields.Char(required=True)
