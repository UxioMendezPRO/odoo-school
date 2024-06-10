from odoo import models, fields, api
from odoo.exceptions import UserError


class Course(models.Model):
    _name = "course.course"
    _description = "Course"

    year = fields.Selection(
        string="Year",
        selection=[("1", "First"), ("2", "Second"), ("3", "Third")],
        default="1",
    )
    classes = fields.Selection(
        string="Class", selection=[("a", "A"), ("b", "B"), ("c", "C")], default="a"
    )
    books_id = fields.Many2many("books.course", string="Books")
    tuition_ids = fields.One2many("tuition.course", "course_id", string="Tuitions")

    @api.constrains("classes")
    def check_classes(self):
        print("comprueba la clase")
        for class_data in self:
            class_data = {
                "year": self.year,
                "class": self.clasess,
            }
        for record in self:
            for key in class_data:
                if record.year == key.year and record.classes == key.classes:
                    raise UserError("No puede repetirse la clase")
