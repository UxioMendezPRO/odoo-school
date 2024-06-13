from odoo import models, fields, api
from odoo.exceptions import UserError
from datetime import datetime


class Tuition(models.Model):
    _name = "tuition.course"
    _description = "Tuition"

    price = fields.Float("Price")
    validity = fields.Date(
        "Validity date",
        default=datetime(day=15, month=6, year=datetime.now().year + 1),
    )
    active = fields.Boolean("Is active", default=True)
    student_id = fields.Many2one("res.partner", string="Student")
    course_id = fields.Many2one("course.course", string="Course", required=True)
    category_id = fields.Char(compute="_compute_category_id")

    # Constrain para no tener más de una matrícula activa
    @api.model
    def create(self, vals):
        student_id = vals.get("student_id", False)
        this_student = self.env["res.partner"].browse(student_id)
        if this_student:
            for tuition in this_student.tuition_ids:
                if tuition.active:
                    raise UserError("There is an active tuition")
        return super(Tuition, self).create(vals)

    @api.onchange("validity")
    def onchange_validity(self):
        for record in self:
            if record.validity < datetime.now().date():
                raise UserError("Invalid date")

    @api.depends("category_id")
    def _compute_category_id(self):
        default_category = self.env["product.category"].search([], limit=1)
        for record in self:
            record.category_id = default_category.id if default_category else False

    def action_create_tuition(self):

        product = self.env["product.product"].create(
            {
                "name": "Tuition",
                "categ_id": self.category_id,
                "list_price": self.price,
                "standard_price": 0,
                "type": "service",
            }
        )
        tuition = self.env["sale.order"].create(
            {
                "partner_id": self.student_id.id,
                "validity_date": self.validity,
                "order_line": [
                    (
                        0,
                        False,
                        {
                            "product_id": product.id,
                            "name": "Tuition",
                            "product_uom_qty": 1,
                            "price_unit": self.price,
                        },
                    ),
                ],
            }
        )
