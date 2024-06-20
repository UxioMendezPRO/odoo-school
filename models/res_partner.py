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
    tuition_state = fields.Selection(
        [
            ("new", "New Student"),
            ("requested", "Tuition Requested"),
            ("confirmed", "Tuition Confirmed"),
            ("cancelled", "Tuition Cancelled"),
            ("expired", "Tuition Expired"),
        ],
        compute="_compute_tuition_state",
        readonly=True,
        default="new",
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

    @api.depends("tuition_ids")
    def _compute_tuition_state(self):
        for record in self:
            if not record.tuition_ids:
                record.tuition_state = "new"

            for tuition in record.tuition_ids:
                if tuition.state == "requested":
                    record.tuition_state = "requested"
                if tuition.state == "confirmed":
                    record.tuition_state = "confirmed"
                if tuition.state == "cancelled":
                    record.tuition_state = "cancelled"
                if tuition.state == "expired":
                    record.tuition_state = "expired"
