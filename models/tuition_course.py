from odoo import models, fields
from dateutil.relativedelta import relativedelta


class Tuition(models.Model):
    _name = "tuition.course"
    _description = "Tuition"

    price = fields.Float("Price")
    validity = fields.Date(
        "Validity date", default=fields.Date.today() + relativedelta(years=1)
    )
    active = fields.Boolean("Is active")
    student_id = fields.Many2one("student.course", string="Student")
    course_id = fields.Many2one("course.course", string="Course")
