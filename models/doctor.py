from odoo import models, fields, api
from odoo.exceptions import UserError
from datetime import date


class DoctorInfo(models.Model):
    _name = "doctor"
    _description = 'Doctor'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(required=True)
    email = fields.Char(compute='_compute_email', readonly=True, store=1)
    birth_date = fields.Date(compute='_compute_info', store=True)
    age = fields.Integer(compute='_compute_info', store=True)
    gender = fields.Selection([
        ('m', 'Male'),
        ('f', 'Female')
    ], compute='_compute_gender', store=1)
    joining_date = fields.Date(required=1)
    phone = fields.Char(string='Phone Number', size=11, widget='phone', help='Enter the phone number')
    national_id = fields.Char(string='National ID', size=14, required=True)
    departments_id = fields.Many2one('department')
    is_opened = fields.Boolean(related='departments_id.is_opened')
    capacity = fields.Integer(related="departments_id.doctors_capacity")
    patients_ids = fields.Many2many('patient', tracking=1)
    image = fields.Binary()
    salary = fields.Float(compute='_compute_info', store=True, tracking=1)
    address = fields.Text()


    @api.depends("name")
    def _compute_email(self):
        for rec in self:
            if rec.name:
                # Generate the email using the first and last names
                # You may need to customize the email format based on your requirements
                rec.email = f'{(rec.name.lower().split())[0][0]}_{(rec.name.lower().split())[1]}@org.com'
            else:
                rec.email = False


    @api.depends('national_id')
    def _compute_info(self):
        today = date.today()
        for rec in self:
            if rec.national_id and len(rec.national_id) == 14:
                if int(rec.national_id[3:5]) > 12 or int(rec.national_id[5:7]) > 31:
                    raise UserError("You entered wrong ID!")

                if rec.national_id[0] == '2':
                    year = int(f"19{rec.national_id[1:3]}")
                else:
                    year = int(f"20{rec.national_id[1:3]}")
                month = int(rec.national_id[3:5])
                day = int(rec.national_id[5:7])
                rec.birth_date = fields.Date.from_string(f"{year:04d}-{month:02d}-{day:02d}")
            else:
                rec.birth_date = False

            if rec.birth_date:
                birth_date = fields.Date.from_string(rec.birth_date)
                age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
                rec.age = age
            else:
                rec.age = 0  # or any default value if birth_date is not set

            if rec.age > 60:
                raise UserError("This person older than 60!!")
            if rec.age >= 30:
                rec.salary = 5000
            else:
                rec.salary = 2500


    @api.depends('national_id')
    def _compute_gender(self):
        for record in self:
            national_id = record.national_id
            if national_id and len(national_id) == 14:
                # Extract the 13th digit (index 12)
                gender_digit = int(national_id[12])

                # Determine gender based on the 13th digit
                if gender_digit % 2 == 0:
                    record.gender = 'f'
                else:
                    record.gender = 'm'
            else:
                record.gender = False

    @api.constrains('departments_id')
    def check_departments_id(self):
        for rec in self:
            department_count = len(rec.departments_id.doctors_ids)
            if department_count > rec.capacity:
                raise UserError(f"{rec.departments_id.name} department is full")


    # @api.model
    # def search(self):
    #     res = super(DoctorInfo, self).search()
    #     search_email = self.search([('email', '=', 'res.email')])
    #     if search_email:
    #         raise UserError("Email already exist")
    #     return res
    #
    # def write(self, vals):
    #     if "name" in vals:
    #         res_split = vals['name'].lower().split()
    #         vals['email'] = f"{res_split[0][0]}_{res_split[1]}@yahoo.com"
    #     return super().write(vals)
