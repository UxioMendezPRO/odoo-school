from odoo import fields, models, api
from odoo.exceptions import UserError


class SaleOrder(models.Model):
    _inherit = "sale.order"

    _name = "sale.order"
    _description = "Sale order"

    tuition_id = fields.Many2one("tuition.course")

    @api.model
    def create(self, vals):
        tuition_id = vals.get("tuition_id", False)
        if tuition_id:
            tuition = self.env["tuition.course"].browse(tuition_id)
            tuitions = self.env["tuition.course"].search([("id", "=", tuition.id)])
            if tuitions:
                raise UserError("A sale for this tuition already exists")
            vals["tuition_id"] = tuition.id
        return super(SaleOrder, self).create(vals)

    def action_confirm(self):
        this_tuition = self.tuition_id
        if this_tuition:
            this_tuition.state = "confirmed"
        return super(SaleOrder, self).action_confirm()
