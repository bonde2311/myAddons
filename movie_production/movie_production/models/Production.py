from odoo import models, fields


# Durgesh Bagul & Gaurav Bonde (22/05/2025)

class MovieProduction(models.Model):
    _name = 'movie.production'
    _description = 'Movie Production'

    # Basic Info
    name = fields.Char(string='Title', required=True)
    type = fields.Selection([
        ('movie', 'Movie'),
        ('web_series', 'Web Series'),
        ('short_film', 'Short Film')
    ], string='Type', required=True)
    genre = fields.Char(string="Genre")
    language = fields.Char(string="Language")
    description = fields.Html(string="Description")

    # Schedule
    start_date = fields.Date(string='Start Date')
    end_date = fields.Date(string='End Date')
    release_date = fields.Date(string='Expected Release Date')
    poster = fields.Image(string="Poster")
    trailer_link = fields.Char(string="Trailer Link (YouTube/Vimeo)")
    budget = fields.Float(string="Budget")
    box_office = fields.Float(string="Box Office Collection")
    rating = fields.Float(string="Rating")
    # Relations
    production_house_id = fields.Many2one('movie.production.house', string='Production House')
    actor_ids = fields.Many2many('movie.actor', string='Cast')
    crew_ids = fields.Many2many('movie.crew', string='Crew Members')
    location_ids = fields.Many2many('movie.location', string='Shoot Locations')
    schedule_ids = fields.One2many('movie.schedule', 'production_id', string='Shoot Schedule')
    theatre_ids = fields.Many2many('movie.theatre', string='Theatres')
    ott_platform_ids = fields.Many2many('ott.platform', string='OTT Platforms')
    role_ids = fields.One2many('movie.actor.role', 'production_ids',string='Actor Roles')
    sponsor_ids = fields.Many2many('movie.sponsor', string='Sponsors')

    # Media & Marketing

    # Relation to different partner types
    music_partner_ids = fields.Many2many('partner.music', string='Music Partner')
    tv_partner_ids = fields.Many2many('partner.tv', string='TV Partner')
    otts_partner_ids = fields.Many2many('partner.ott', string='OTT Partner')
    radio_partner_ids = fields.Many2many('partner.radio', string='Radio Partner')
    movie_partner_print_partner_ids = fields.Many2many('partner.print', string='Print Media Partner')
    distribution_partner_ids = fields.Many2many('partner.distribution', string='Distribution Partner')
    legal_partner_ids = fields.Many2many('partner.legal', string='Legal Partner')
    merchandise_partner_ids = fields.Many2many('partner.merchandise', string='Merchandise Partner')
    event_partner_ids = fields.Many2many('partner.event', string='Event Partner')
    vfx_post_partner_ids = fields.Many2many('partner.vfx_post', string='VFX & Post-production Partner')
    talent_agency_partner_ids = fields.Many2many('partner.talent_agency', string='Talent Agency Partner')
    cinema_chain_partner_ids = fields.Many2many('partner.cinema_chain', string='Cinema Chain Partner')
    international_traveling_partner_ids = fields.Many2many('partner.intl_sales', string='International Sales Partner')
    subtitle_dubbing_partner_ids = fields.Many2many('partner.subtitling_dubbing', string='Subtitling & Dubbing Partner')
    food_beverages_partner_ids = fields.Many2many('partner.food_beverage', string='Food & Beverage Partner')
    travel_partner_ids = fields.Many2many('partner.travel_accommodation', string='Travel & Accommodation Partner')
    # Status
    movie_type = fields.Selection([
        ('2d', '2D'),
        ('3d', '3D'),
    ], string="Movie type 2D/3D", default="2d")
    payment_line_ids = fields.One2many('movie.payment.line', 'production_id', string='Actor & Crew Payments')

    is_released = fields.Boolean(string="Is Released?", default=False)
    status = fields.Selection([
        ('planning', 'Planning'),
        ('filming', 'Filming'),
        ('post_production', 'Post Production'),
        ('released', 'Released'),
        ('cancelled', 'Cancelled')
    ], string="Status", default="planning")



    contract_ids = fields.One2many('movie.contract', 'production_id')

    # # Optional: computed field to get contract statuses summary
    # contract_status_summary = fields.Char(
    #     string="Contracts Status",
    #     compute='_compute_contract_status_summary',
    #     store=False
    # )
    #
    # def _compute_contract_status_summary(self):
    #     for rec in self:
    #         statuses = rec.contract_ids.mapped('status')
    #         rec.contract_status_summary = ", ".join(set(statuses)) if statuses else "No Contracts"

