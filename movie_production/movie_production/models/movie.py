# Python models for Movie Production ERP (Odoo 16)
from odoo import models, fields

# Durgesh Bagul & Gaurav Bonde (21/05/2025)

# 4. Movie Location
class MovieLocation(models.Model):
    _name = 'movie.location'
    _description = 'Location'

    name = fields.Char()
    address = fields.Text()
    city = fields.Char()
    available_from = fields.Date()
    available_to = fields.Date()



# 6. Movie Schedule
class MovieSchedule(models.Model):
    _name = 'movie.schedule'
    _description = 'Shoot Schedule'


    production_id = fields.Many2one('movie.production')
    date = fields.Date()
    start_time = fields.Datetime()
    end_time = fields.Datetime()
    scene_description = fields.Text()


    location_id = fields.Many2one('movie.location')
    actor_ids = fields.Many2many('movie.actor')
    crew_ids = fields.Many2many('movie.crew')
