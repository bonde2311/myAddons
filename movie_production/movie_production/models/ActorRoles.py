
from odoo import models, fields, api

# Durgesh Bagul & Gaurav Bonde (20/05/2025)
class ActorRole(models.Model):
    _name = 'movie.actor.role'
    _description = 'Actor Role'

    name = fields.Char(string="Role Name", required=True)
    desc = fields.Text(string="Role Description", required=True)
    actor_ids = fields.Many2one('movie.actor',string="Actors")
    production_ids = fields.Many2one('movie.production', string="Movie")

    def action_check_in(self):
        for actor in self.actor_ids:
            self.env['actor.attendance'].create({
                'actor_id': actor.id,
                'check_in': fields.Datetime.now()
            })

    def action_check_out(self):
        for actor in self.actor_ids:
            last_attendance = self.env['actor.attendance'].search([
                ('actor_id', '=', actor.id),
                ('check_out', '=', False)
            ], order="check_in desc", limit=1)
            if last_attendance:
                last_attendance.check_out = fields.Datetime.now()

