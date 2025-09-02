from odoo import models, fields

# Durgesh Bagul & Gaurav Bonde (19/05/2025)

class ActorPortfolio(models.Model):
    _name = 'actor.portfolio'
    _description = 'Actor Portfolio'
    _inherit=['mail.thread']

    name = fields.Char(string='Portfolio Title', required=True)
    actor_id = fields.Many2one('movie.actor', string='Actor', required=True )
    description = fields.Text(string='About Actor')
    achievements = fields.Text(string='Achievements')
    video_link = fields.Char(string='Showreel/Video Link')
    external_profile_url = fields.Char(string='External Portfolio URL')
    skills = fields.Char(string='Skills')
    languages = fields.Char(string='Languages Known')
    image_ids = fields.One2many('portfolio.image', 'portfolio_id', string='Portfolio Images')



class PortfolioImage(models.Model):
    _name = 'portfolio.image'
    _description = 'Portfolio Image'

    portfolio_id = fields.Many2one('actor.portfolio', string='Portfolio', required=True, ondelete='cascade')
    image = fields.Binary(string='Image', attachment=True)
    description = fields.Char(string='Image Description')
