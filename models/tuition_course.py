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
    state = fields.Selection(
        [
            ("new", "New"),
            ("requested", "Requested"),
            ("confirmed", "Confirmed"),
            ("cancelled", "Cancelled"),
            ("expired", "Expired"),
        ],
        default="new",
        readonly=True,
    )
    student_id = fields.Many2one("res.partner", string="Student")
    course_id = fields.Many2one("course.course", string="Course", required=True)
    category_id = fields.Many2one("product.category")
    product_id = fields.Many2one("product.product")
    tax_id = fields.Many2one("account.tax", compute="_compute_tax_id")
    sale_id = fields.Many2one("sale.order")
    curdate = fields.Date(compute="_compute_curdate")

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

    @api.depends("curdate")
    def _compute_curdate(self):
        for record in self:
            record.curdate = datetime.now().date()

    # La fecha debe ser posterior a la actual
    @api.onchange("validity")
    def onchange_validity(self):
        for record in self:
            if record.validity < record.curdate:
                raise UserError("Invalid date")

    @api.onchange("curdate")
    def _check_validity_date(self):
        for record in self:
            if record.curdate > record.validity:
                record.state = "expired"

    # Crea la categoría del producto
    @api.depends("category_id")
    def assign_category_id(self):
        category = self.env["product.category"].search(
            [("name", "=", "Services")], limit=1
        )
        if not category:
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

    @api.depends("tax_id")
    def _compute_tax_id(self):
        tax_id = self.env["account.tax"].create(
            {
                "name": "VAT 21%",
                "amount": 21,
                "type_tax_use": "sale",
                "amount_type": "percent",
            }
        )
        for record in self:
            record.tax_id = tax_id

    # Crea la matrícula
    def action_create_tuition(self):

        product = self.env["product.product"].search(
            [("name", "=", "Tuition")], limit=1
        )
        if not product:
            self.create_product_id()
        for record in self:
            record.product_id = product

        sale_order = self.env["sale.order"].create(
            {
                "partner_id": self.student_id.id,
                "validity_date": self.validity,
                "order_line": [
                    (
                        0,
                        False,
                        {
                            "product_id": self.product_id.id,
                            "name": f"{self.student_id.name}, {self.course_id.name}",
                            "product_uom_qty": 1,
                            "price_unit": self.price,
                            "tax_id": self.tax_id,
                        },
                    ),
                ],
            }
        )
        for record in self:
            record.sale_id = sale_order
            record.state = "requested"

        sale_order.tuition_id = self.id

        return {
            "type": "ir.actions.act_window",
            "name": "Sales",
            "view_mode": "form",
            "res_model": "sale.order",
            "res_id": sale_order.id,
            "target": "current",
        }
