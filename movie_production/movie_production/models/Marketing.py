from odoo import models, fields

class MovieMarketing(models.Model):
    _name = 'movie.marketing'
    _description = 'Movie Marketing Activity'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    movie_id = fields.Many2one('movie.production', string="Movie", required=True)
    name = fields.Char(string="Title", required=True)
    marketing_type = fields.Selection([
        ('social_media', 'Social Media'),
        ('influencer', 'Influencer Collaboration'),
        ('event', 'Event / Launch'),
        ('pr', 'PR / News'),
        ('email', 'Email / WhatsApp Campaign'),
        ('seo', 'SEO / SEM'),
        ('partnership', 'Partnership'),
        ('video', 'Trailer / Promo'),
    ], string="Marketing Type", required=True)

    date = fields.Date(string="Marketing Date", required=True)
    budget = fields.Float(string="Estimated Budget")
    actual_cost = fields.Float(string="Actual Cost")
    status = fields.Selection([
        ('planned', 'Planned'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    ], default='planned')
    responsible_user = fields.Many2one('res.users', string="Handled By", default=lambda self: self.env.user)
    description = fields.Text(string="Details")

    # ----------- Social Media
    social_platform = fields.Selection([
        ('instagram', 'Instagram'),
        ('facebook', 'Facebook'),
        ('twitter', 'Twitter'),
        ('youtube', 'YouTube'),
    ], string="Platform")
    post_link = fields.Char(string="Post Link")
    # -- Social Media Extended Fields
    post_content = fields.Text(string="Post Caption / Content")
    post_image = fields.Binary(string="Post Image")
    media_type = fields.Selection([
        ('image', 'Image'),
        ('video', 'Video'),
        ('carousel', 'Carousel'),
    ], string="Media Type")
    post_date = fields.Date(string="Post Date")
    scheduled_date = fields.Date(string="Scheduled Date")


    # ----------- Influencer
    influencer_name = fields.Char(string="Influencer Name")
    influencer_handle = fields.Char(string="Handle")
    followers = fields.Integer(string="Followers")
    influencer_platform = fields.Selection([
        ('instagram', 'Instagram'),
        ('youtube', 'YouTube'),
        ('facebook', 'Facebook'),
    ], string="Platform")

    # ----------- Event
    event_name = fields.Char(string="Event Name")
    event_date = fields.Datetime(string="Event Date")
    venue = fields.Char(string="Venue")
    city = fields.Char(string="City")
    attendees = fields.Integer(string="Attendees")

    # ----------- PR
    media_outlet = fields.Char(string="Media Outlet")
    coverage_type = fields.Selection([
        ('interview', 'Interview'),
        ('article', 'Article'),
        ('press_release', 'Press Release'),
    ], string="Coverage Type")
    published_link = fields.Char(string="Link")

    # ----------- Email Campaign
    campaign_name = fields.Char(string="Campaign Name")
    recipients = fields.Integer(string="Recipients")
    open_rate = fields.Float(string="Open Rate (%)")
    click_rate = fields.Float(string="Click Rate (%)")

    # ----------- SEO/SEM
    keywords_targeted = fields.Text(string="Keywords")
    seo_platform = fields.Selection([
        ('google', 'Google'),
        ('youtube', 'YouTube'),
    ], string="Platform")
    impressions = fields.Integer(string="Impressions")
    clicks = fields.Integer(string="Clicks")

    # ----------- Partnership
    partner_brand = fields.Char(string="Brand")
    collaboration_type = fields.Selection([
        ('cross_promo', 'Cross Promotion'),
        ('sponsored', 'Sponsored Content'),
        ('merch', 'Merchandise'),
    ], string="Collaboration Type")
    benefits = fields.Text(string="Benefits")

    # ----------- Video / Trailer
    video_title = fields.Char(string="Video Title")
    video_platform = fields.Selection([
        ('youtube', 'YouTube'),
        ('instagram', 'Instagram'),
        ('theatre', 'In Theatres'),
    ], string="Platform")
    views = fields.Integer(string="Views")
    shares = fields.Integer(string="Shares")
