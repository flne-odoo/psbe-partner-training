from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare
from dateutil.relativedelta import relativedelta

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Property Model"
    _sql_constraints = [
        ('check_expected_price_positive', 'CHECK(expected_price > 0)', 'The Expected Price has to be greater than 0.'),
        ('check_selling_price_positive', 'CHECK(selling_price >= 0)', 'The Selling Price has to be positive.'),
    ]

    def _default_date_availability(self):
        return fields.Date.today() + relativedelta(months=3)

    active = fields.Boolean(default=True)
    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(default=_default_date_availability, copy=False)
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        [
            ("north", "North"),
            ("south", "South"),
            ("east", "East"),
            ("west", "West"),
        ],
    )
    state = fields.Selection(
        [
            ("new", "New"),
            ("received", "Offer Received"),
            ("accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("canceled", "Canceled"),
        ],
        default="new",
        required=True,
        copy=False,
    )
    property_type_id = fields.Many2one("estate.property.type")
    buyer_id = fields.Many2one("res.partner", copy=False)
    salesperson_id = fields.Many2one("res.users", default=lambda self: self.env.user)
    offer_ids = fields.One2many("estate.property.offer", "property_id")
    tag_ids = fields.Many2many("estate.property.tag")
    total_area = fields.Integer(compute="_compute_total_area")
    best_price = fields.Float(compute="_compute_best_price")

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for estate in self:
            estate.total_area = estate.living_area + estate.garden_area

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for estate in self:
            estate.best_price = estate.offer_ids and max(estate.offer_ids.mapped("price"))

    @api.onchange("garden")
    def _onchange_garden(self):
        for estate in self:
            if estate.garden:
                estate.garden_area = 10
                estate.garden_orientation = "north"
            else:
                estate.garden_area = 0
                estate.garden_orientation = False

    @api.onchange("date_availability")
    def _onchange_date_availability(self):
        if self.date_availability < fields.Date.today():
            return {
                "warning": {
                    "title": _("Warning"),
                    "message": _("Date is in the past")
                }
            }

    def action_sold(self):
        self.ensure_one()
        if self.state == "canceled":
            raise UserError(_("A cancelled property can not be sold."))
        self.state = "sold"
        return True

    def action_cancel(self):
        self.ensure_one()
        if self.state == "sold":
            raise UserError(_("A sold property can not be canceled."))
        self.state = "canceled"
        return True

    @api.constrains("selling_price")
    def _check_selling_price(self):
        for estate in self.filtered(lambda e: e.selling_price != 0):
            if float_compare(estate.selling_price, estate.expected_price * 0.9, precision_digits=2) < 0:
                raise ValidationError(_("The selling price cannot be lower than 90% of the expected price."))
