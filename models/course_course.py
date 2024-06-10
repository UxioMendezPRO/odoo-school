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
    letter = fields.Selection(
        string="Class", selection=[("a", "A"), ("b", "B"), ("c", "C")], default="a"
    )
    books_id = fields.Many2many("books.course", string="Books")
    tuition_ids = fields.One2many("tuition.course", "course_id", string="Tuitions")

    @api.model
    def get_class_info(self):
        all_courses = self.search([])
        class_info = []
        for course in all_courses:
            class_info.append((course.year, course.letter))
        return class_info

    @api.constrains("year", "letter")
    def check_year_letter(self):
        class_info = self.get_class_info()
        counter = 0
        for record in self:
            this_class = (record.year, record.letter)
            for current_class in class_info:
                if this_class == current_class:
                    counter += 1
                    print(counter)
                    if counter > 1:
                        raise UserError("The course already exist")
