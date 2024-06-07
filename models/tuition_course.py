from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError
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
        if self.student_id is not None:
            this_student = self.env["student.course"].browse(self.student_id)
            if this_student.tuition_id.active == True:
                raise UserError("Matrícula en activo")
        return super(Tuition, self).create(vals)
