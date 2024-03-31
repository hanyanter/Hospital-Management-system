from odoo import fields, models, api
from odoo.exceptions import ValidationError, UserError


class ChangeState(models.TransientModel):
    _name = "change.state"

    patient_id = fields.Many2one('patient')
    state = fields.Selection([
        ('undetermined', 'Undetermined'),
        ('serious', 'Serious')
    ], default='undetermined')
    reason = fields.Text()

    def action_confirm(self):
        if self.patient_id.state == 'healthy':
            self.patient_id.state = self.state
            self.patient_id.create_history_record('healthy', self.state, self.reason)