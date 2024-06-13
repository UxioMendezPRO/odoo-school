from odoo import models, fields, api


class ResPartner(models.Model):
    _inherit = "res.partner"

    _name = "res.partner"
    _description = "res.partner inheritance"

    personal_file = fields.Char("Personal file")
    tuition_ids = fields.One2many("tuition.course", "student_id")
    expenses = fields.Float(compute="_compute_expenses", string="Expenses", store=True)
    total_tuitions = fields.Integer(
        compute="_compute_total_tuitions", string="Tuitions"
    )

    @api.depends("tuition_ids.price")
    def _compute_expenses(self):
        for record in self:
            record.expenses = sum(tuition.price for tuition in record.tuition_ids)

    @api.depends("total_tuitions")
    def _compute_total_tuitions(self):
        total = 0
        for record in self:
            for tuition in record.tuition_ids:
                total += 1
            record.total_tuitions = total
