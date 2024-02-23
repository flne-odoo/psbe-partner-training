from odoo import fields, models


class PropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Type of properties"

    name = fields.Char(required=True)
    property_ids = fields.One2many("estate.property", "property_type_id")
