from odoo import fields, models, api


class Student(models.Model):
    _name = "student.course"
    _description = "Student"

    name = fields.Char("Name")
    address = fields.Char("Address")
    personal_file = fields.Char("Personal file")
    tuition_id = fields.One2many("tuition.course", "student_id", string="Tuitions")
