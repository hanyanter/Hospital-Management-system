from odoo import models, fields, api
from odoo.exceptions import UserError
from datetime import date


class PatientInfo(models.Model):
    _name = "patient"
    _description = 'Patient'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    ref = fields.Char(default="New", readonly=True)
    name = fields.Char(required=1, translate=1)
    birth_date = fields.Date()
    age = fields.Integer(compute='_compute_age', store=1)
    phone = fields.Char(size=11, widget='phone', help='Enter the phone number')
    history = fields.Html(tracking=1)
    cr_ratio = fields.Float(string='CR ratio')
    blood_type = fields.Selection([
        ('o+', 'O+'), ('o-', 'O-'),
        ('a+', 'A+'), ('a-', 'A-'),
        ('b+', 'B+'), ('b-', 'B-')
    ], required=1)
    pcr = fields.Boolean()
    image = fields.Binary()
    address = fields.Text(tracking=1)
    departments_ids = fields.Many2many('department')
    capacity = fields.Integer(related="departments_ids.patients_capacity")
    doctors_ids = fields.Many2many('doctor')
    state = fields.Selection([('undetermined', 'Undetermined'),
                              ('good', 'Good'),
                              ('serious', 'Serious'),
                              ('healthy', 'Healthy')],
                             default='undetermined', readonly=1, tracking=1)
    user_id = fields.Many2one('res.users', readonly=1)
    write_date = fields.Datetime(readonly=1)
    description = fields.Text()

    # log_ids = fields.One2many('log.history', 'patient_id')

    def action_undetermined(self):
        for rec in self:
            rec.create_history_record(rec.state, 'undetermined')
            rec.state = 'undetermined'

    def action_good(self):
        for rec in self:
            rec.create_history_record(rec.state, 'good')
            rec.state = 'good'

    def action_serious(self):
        for rec in self:
            rec.create_history_record(rec.state, 'serious')
            rec.state = 'serious'

    def action_healthy(self):
        for rec in self:
            rec.create_history_record(rec.state, 'healthy')
            rec.state = 'healthy'

    def create_history_record(self, old_state, new_state, reason=""):
        for rec in self:
            rec.env['patient.history'].create({
                'user_id': rec.env.uid,
                'patient_id': rec.id,
                'old_state': old_state,
                'new_state': new_state,
                'reason': reason or ""
            })

    def action_open_change_state_wizard(self):
        action = self.env['ir.actions.actions']._for_xml_id('hospital_ms.change_state_wizard_action')
        action['context'] = {'default_patient_id': self.id}
        return action

    @api.depends('birth_date')
    def _compute_age(self):
        today = date.today()
        for rec in self:
            if rec.birth_date:
                birth_date = fields.Date.from_string(rec.birth_date)
                age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
                rec.age = age
                if rec.age < 30:
                    rec.pcr = True

    # @api.onchange('birth_date')
    # def _onchange_pcr(self):
    #     for rec in self:
    #         if rec.age >= 30:
    #             rec.pcr = False
    #         else:
    #             rec.pcr = True
    #             return {'warning': {'title': 'warning',
    #                                 'message': 'PCR has been checked due to age below 30'}
    #                     }

    @api.constrains('departments_ids')
    def check_departments_ids(self):
        for rec in self:
            department_count = len(rec.departments_ids.patients_ids)
            if department_count > rec.capacity:
                raise UserError(f"{rec.departments_id.name} department is full")

    @api.model
    def create(self, vals):
        res = super(PatientInfo, self).create(vals)
        if res.ref == 'New':
            res.ref = self.env['ir.sequence'].next_by_code('patient_seq')
        return res

# class LogHistory(models.Model):
#     _name = "log.history"
#     _description = "Patient Log History"
#
#     user_id = fields.Many2one('res.users', readonly=1)
#     create_date = fields.Datetime(readonly=1)
#     description = fields.Text()
#     patient_id = fields.Many2one('patient')
