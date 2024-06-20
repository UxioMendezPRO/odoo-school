from odoo import fields, models, api
from odoo.exceptions import UserError


class SaleOrder(models.Model):
    _inherit = "sale.order"

    _name = "sale.order"
    _description = "Sale order"

    tuition_id = fields.Many2one("tuition.course")

    @api.model
    def create(self, vals):
        this_tuition = self.env["tuition.course"].browse(
            vals.get("tuition_id", False)
        )  # Todavia no tiene la tuition_id asignada pq no se ha creado la venta
        if this_tuition.sale_id:
            raise UserError("A sale for this tuition already exists")
        return super(SaleOrder, self).create(vals)

    def action_confirm(self):
        self.tuition_id.state = "confirmed"
        return super(SaleOrder, self).action_confirm()
