from odoo import fields, models, api
from odoo.exceptions import UserError


class SaleOrder(models.Model):
    _inherit = "sale.order"

    _name = "sale.order"
    _description = "Sale order"

    tuition_id = fields.Many2one("tuition.course")

    @api.model
    def create(self, vals):
        print(self.tuition_id.id)
        if self.tuition_id:
            raise UserError("A sale for this tuition already exists")

        return super(SaleOrder, self).create(vals)
