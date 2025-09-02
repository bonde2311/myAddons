from odoo import models, fields, api

class MovieAttendance(models.Model):
    _name = 'movie.attendance'
    _description = 'Unified Attendance for Actor and Crew'
    _order = 'check_in desc'

    name = fields.Char(string="Name", compute="_compute_name", store=True)

    participant_type = fields.Selection([
        ('actor', 'Actor'),
        ('crew', 'Crew')
    ], string="Participant Type", required=True)
    check_in = fields.Datetime(string="Check In")
    check_out = fields.Datetime(string="Check Out")
    duration = fields.Float(string="Duration (Hours)", compute="_compute_duration", store=True)

    state = fields.Selection([
        ('draft', 'Draft'),
        ('checked_in', 'Checked In'),
        ('checked_out', 'Checked Out')
    ], string="Status", default='draft', tracking=True)


    actor_id = fields.Many2one('movie.actor', string="Actor")
    crew_id = fields.Many2one('movie.crew', string="Crew")


    @api.depends('participant_type', 'actor_id', 'crew_id')
    def _compute_name(self):
        for rec in self:
            if rec.participant_type == 'actor' and rec.actor_id:
                rec.name = rec.actor_id.name
            elif rec.participant_type == 'crew' and rec.crew_id:
                rec.name = rec.crew_id.name
            else:
                rec.name = 'Unknown'

    @api.depends('check_in', 'check_out')
    def _compute_duration(self):
        for record in self:
            if record.check_in and record.check_out:
                delta = record.check_out - record.check_in
                record.duration = round(delta.total_seconds() / 3600.0, 2)
            else:
                record.duration = 0.0

    @api.onchange('participant_type')
    def _onchange_participant_type(self):
        self.actor_id = False
        self.crew_id = False

    def action_check_in(self):
        self.write({
            'check_in': fields.Datetime.now(),
            'state': 'checked_in'
        })

    def action_check_out(self):
        self.write({
            'check_out': fields.Datetime.now(),
            'state': 'checked_out'
        })
