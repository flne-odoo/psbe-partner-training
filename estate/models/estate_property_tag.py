from odoo import fields, models


class PropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Tags of Real Estate Model"
    _sql_constraints = [("unique_tag_name", "unique(name)", "Tag Name should be unique")]

    name = fields.Char(required=True)
