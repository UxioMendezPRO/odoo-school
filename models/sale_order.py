from odoo import fields, models, api
from odoo.exceptions import UserError


class SaleOrder(models.Model):
    _inherit = "sale.order"

    _name = "sale.order"
    _description = "Sale order inheritance"

    tuition_id = fields.Many2one("tuition.course")

    def action_confirm(self):
        self.tuition_id.state = "confirmed"
        return super(SaleOrder, self).action_confirm()

    def action_cancel(self):
        self.tuition_id.state = "cancelled"
        return super(SaleOrder, self).action_cancel()
