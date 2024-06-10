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
    student_id = fields.Many2one("student.course", string="Student")
    course_id = fields.Many2one("course.course", string="Course")

    @api.model
    def create(self, vals):
        tuitions = self.search([])
        if tuitions is not None:
            for tuition in tuitions:
                if tuition.active:
                    raise UserError("There is an active tuition")
        return super(Tuition, self).create(vals)

    @api.onchange("validity")
    def onchange_validity(self):
        for record in self:
            if record.validity < datetime.now().date():
                raise UserError("Invalid date")
