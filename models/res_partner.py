from odoo import models, fields, api


class ResPartner(models.Model):
    _inherit = "res.partner"

    _name = "res.partner"
    _description = "res.partner inheritance"

    personal_file = fields.Char("Personal file")
    tuition_ids = fields.One2many("tuition.course", "student_id")
    total_tuitions = fields.Integer(
        compute="_compute_total_tuitions", string="Tuitions"
    )
    user_id = fields.Many2one(
        "res.users", string="User", default=lambda self: self.env.user
    )

    @api.depends("total_tuitions")
    def _compute_total_tuitions(self):
        total = 0
        for record in self:
            for tuition in record.tuition_ids:
                total += 1
            record.total_tuitions = total
