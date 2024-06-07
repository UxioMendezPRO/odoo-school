from odoo import models, fields


class Book(models.Model):
    _name = "books.course"
    _description = "Books"

    title = fields.Char("Title")
    author = fields.Char("Author")
    courses_id = fields.Many2many("course.course", string="Courses")
