from odoo import models, fields, api


class PatientHistory(models.Model):
    _name = "patient.history"
    _description = 'Patient History'

    write_id = fields.Many2one('res.users', readonly=1)
    user_id = fields.Many2one('res.users', readonly=1)
    patient_id = fields.Many2one('patient')
    write_date = fields.Datetime(readonly=1)
    old_state = fields.Char()
    new_state = fields.Char()
    reason = fields.Text()