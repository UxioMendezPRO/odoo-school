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
        "res.users", default=lambda self: self.env.user, readonly=True
    )
    team_id = fields.Many2one(
        "crm.team",
        default=lambda self: self.env.ref("sales_team.team_sales_department"),
        readonly=True,
    )
    company_name = fields.Char(
        string="Company Name",
        related="company_id.name",
        readonly=True,
        default=lambda self: self.env.user.company_id.name,
    )

    @api.depends("total_tuitions")
    def _compute_total_tuitions(self):
        total = 0
        for record in self:
            for tuition in record.tuition_ids:
                total += 1
            record.total_tuitions = total
