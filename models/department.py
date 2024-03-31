from odoo import models, fields, api
from odoo.exceptions import UserError


class Department(models.Model):
    _name = "department"
    _description = 'Department'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    # _rec_name = "capacity"    # Main record name which will appear in field

    name = fields.Selection([
        ('باطنة', 'باطنة'),
        ('أشعة', 'أشعة'),
        ('أطفال', 'أطفال'),
        ('جراحة', 'جراحة'),
        ('أسنان', 'أسنان')
    ], string='Department')
    doctors_capacity = fields.Integer(tracking=1)
    patients_capacity = fields.Integer(compute='_compute_patients_capacity', tracking=1)
    doctors_ids = fields.One2many('doctor', 'departments_id', readonly=1)
    # is_opened = fields.Boolean(compute='_compute_capacity', readonly=1, tracking=1)
    is_opened = fields.Boolean(tracking=1)
    patients_ids = fields.Many2many('patient')


    @api.depends('doctors_ids')
    def _compute_capacity(self):
        for rec in self:
            if len(rec.doctors_ids) >= rec.doctors_capacity:
                rec.is_opened = False
            else:
                rec.is_opened = True


    @api.depends('doctors_capacity')
    def _compute_patients_capacity(self):
        for rec in self:
            rec.patients_capacity = rec.doctors_capacity * 10


    # @api.constrains('is_opened')
    # def check_is_opened(self):
    #     for rec in self:
    #         department_count = len(rec.doctors_ids)
    #         if department_count >= rec.capacity:
    #             rec.is_opened = False
    #         else:
    #             rec.is_opened = True