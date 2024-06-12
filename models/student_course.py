from odoo import fields, models, api


class Student(models.Model):
    _name = "student.course"
    _description = "Student"

    name = fields.Char("Name")
    address = fields.Char("Address")
    personal_file = fields.Char("Personal file")
    tuition_ids = fields.One2many("tuition.course", "student_id", string="Tuitions")
    expenses = fields.Float(compute="_compute_expenses", string="Expenses", store=True)
    total_tuitions = fields.Integer(
        compute="_compute_total_tuitions", string="Tuitions"
    )

    @api.depends("tuition_ids.price")
    def _compute_expenses(self):
        for record in self:
            record.expenses = sum(tuition.price for tuition in record.tuition_ids)

    @api.depends("total_tuitions")
    def _compute_total_tuitions(self):
        total = 0
        for record in self:
            for tuition in record.tuition_ids:
                total += 1
            record.total_tuitions = total
