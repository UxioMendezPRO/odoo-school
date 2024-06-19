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
    category_id = fields.Many2one("product.category")
    product_id = fields.Many2one("product.product")

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

    # La fecha debe ser posterior a la actual
    @api.onchange("validity")
    def onchange_validity(self):
        for record in self:
            if record.validity < datetime.now().date():
                raise UserError("Invalid date")

    # Crea la categoría del producto
    @api.depends("category_id")
    def assign_category_id(self):
        category = self.env["product.category"].search(
            [("name", "=", "Services")], limit=1
        )
        print("la encuentra")
        if not category:
            print("no la encuentra")
            category = self.env["product.category"].create(
                {
                    "name": "Services",
                }
            )
        for record in self:
            record.category_id = category

    # Crea la id del producto
    @api.depends("product_id")
    def create_product_id(self):
        if not self.category_id:
            self.assign_category_id()
        product = self.env["product.product"].create(
            {
                "name": "Tuition",
                "categ_id": self.category_id.id,
                "list_price": self.price,
                "standard_price": 0,
                "type": "service",
            }
        )
        for record in self:
            record.product_id = product

    # Crea la matrícula
    def action_create_tuition(self):

        if not self.product_id:
            self.create_product_id()

        tuition = self.env["sale.order"].create(
            {
                "partner_id": self.student_id.id,
                "validity_date": self.validity,
                "order_line": [
                    (
                        0,
                        False,
                        {
                            "product_id": self.product_id.id,
                            "name": "Tuition",
                            "product_uom_qty": 1,
                            "price_unit": self.price,
                        },
                    ),
                ],
            }
        )
        return {
            "type": "ir.actions.act_window",
            "name": "Sales",
            "view_mode": "form",
            "res_model": "sale.order",
            "res_id": tuition.id,
            "target": "current",
        }
