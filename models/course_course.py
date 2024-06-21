from odoo import models, fields, api
from odoo.exceptions import UserError


class Course(models.Model):
    _name = "course.course"
    _description = "Course"

    name = fields.Char(compute="_compute_name")
    year = fields.Selection(
        string="Year",
        selection=[("First", "First"), ("Second", "Second"), ("Third", "Third")],
    )
    letter = fields.Selection(
        string="Class", selection=[("A", "A"), ("B", "B"), ("C", "C")]
    )
    books_id = fields.Many2many("books.course", string="Books")
    tuition_ids = fields.One2many("tuition.course", "course_id", string="Tuitions")
    total_students = fields.Integer(
        compute="_compute_total_students", string="Total students", store=True
    )

    @api.model
    def _compute_name(self):
        for record in self:
            record.name = f"{record.year} {record.letter}"

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
                    if counter > 1:
                        raise UserError("The course already exist")

    @api.depends("total_students", "tuition_ids")
    def _compute_total_students(self):
        for record in self:
            record.total_students = len(record.tuition_ids)

    def unlink(self):
        for record in self:
            if record.total_students > 0:
                raise UserError("You can not delete a course with students in it")
        return super(Course, self).unlink()
