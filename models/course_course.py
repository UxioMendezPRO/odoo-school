from odoo import models, fields


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
    tuition_ids = fields.One2many("tuition.course", "course_id")
