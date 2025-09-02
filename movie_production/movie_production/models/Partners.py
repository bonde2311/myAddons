from odoo import models, api,fields




class MoviePartnerMusic(models.Model):
    _name = 'partner.music'
    _description = 'Music Partner'

    name = fields.Char(string='Music Partner Name', required=True)
    owner_name = fields.Char(string='Owner Name')
    logo = fields.Binary(string='Logo')
    production_date = fields.Date(string='Production Date')
    music_rights_type = fields.Selection([
        ('exclusive', 'Exclusive'),
        ('non_exclusive', 'Non-Exclusive')
    ], string='Music Rights Type')
    number_of_tracks = fields.Integer(string='Number of Tracks')
    release_platform = fields.Char(string='Release Platform')




class MoviePartnerTV(models.Model):
    _name = 'partner.tv'
    _description = 'TV Partner'

    name = fields.Char(string='TV Partner Name', required=True)
    channel_name = fields.Char(string='Channel Name')
    logo = fields.Binary(string='Logo')
    license_start_date = fields.Date(string='License Start Date')
    license_duration = fields.Integer(string='License Duration (Months)')
    contact_email = fields.Char(string="Contact Email")
    language = fields.Selection([
        ('hindi', 'Hindi'),
        ('english', 'English'),
        ('marathi', 'Marathi'),
    ], string='Language')


class MoviePartnerOTT(models.Model):
    _name = 'partner.ott'
    _description = 'OTT Partner'

    name = fields.Char(string='OTT Partner Name', required=True)
    platform_url = fields.Char(string='Platform URL')
    app_available = fields.Boolean(string='App Available')
    release_date = fields.Date(string='Release Date')
    logo = fields.Binary(string='Platform Logo')
    exclusive_deal = fields.Boolean(string='Exclusive Deal')
    subscription_type = fields.Selection([
        ('free', 'Free'),
        ('subscription', 'Subscription'),
        ('pay_per_view', 'Pay Per View')
    ], string="Subscription Type")
    contact_email = fields.Char(string="Contact Email")

class MoviePartnerRadio(models.Model):
    _name = 'partner.radio'
    _description = 'Radio Partner'

    name = fields.Char(string='Radio Partner Name', required=True)
    station_name = fields.Char(string='Station Name')
    frequency = fields.Char(string='Frequency (e.g. 98.3 FM)')
    coverage_area = fields.Char(string='Coverage Area')
    advertisement_slot = fields.Char(string='Advertisement Slot')
    city = fields.Char(string='City')


class MoviePartnerPrint(models.Model):
    _name = 'partner.print'
    _description = 'Print Media Partner'

    name = fields.Char(string='Print Media Partner Name', required=True)
    publication_name = fields.Char(string='Publication Name')
    print_date = fields.Date(string='Print Date')
    circulation = fields.Integer(string='Circulation')
    ad_space_size = fields.Char(string='Ad Space Size')
    logo = fields.Binary(string='Publication Logo')



class MoviePartnerDistribution(models.Model):
    _name = 'partner.distribution'
    _description = 'Distribution Partner'

    name = fields.Char(string='Distribution Partner Name', required=True)
    owner_name = fields.Char(string='Owner Name')
    region = fields.Char(string='Region')
    distribution_type = fields.Selection([
        ('theatre', 'Theatre'),
        ('dvd', 'DVD'),
        ('ott', 'OTT')
    ], string='Distribution Type')

    # Used to toggle theatre, ott, dvd fields visibility
    is_theatre = fields.Boolean(compute='_compute_type_flags', store=True)
    is_dvd = fields.Boolean(compute='_compute_type_flags', store=True)
    is_ott = fields.Boolean(compute='_compute_type_flags', store=True)

    # Theatre Fields
    theatre_name = fields.Char("Theatre Name")
    theatre_location = fields.Char("Theatre Location")
    theatre_screen_count = fields.Integer("Number of Screens")
    theatre_seating_capacity = fields.Integer("Seating Capacity")
    theatre_contact_number = fields.Char("Contact Number")
    theatre_email = fields.Char("Email")
    theatre_manager_name = fields.Char("Manager Name")
    theatre_opening_time = fields.Char("Opening Time", help="Format: HH:MM")
    theatre_closing_time = fields.Char("Closing Time", help="Format: HH:MM")
    theatre_has_3d_screen = fields.Boolean("3D Screen Available")
    theatre_has_imax = fields.Boolean("IMAX Enabled")

    # OTT Fields
    platform = fields.Char(string="OTT Platform")
    website = fields.Char(string="Website URL")
    app_available = fields.Boolean(string='App Available')
    contact_email = fields.Char(string="Contact Email")
    ott_logo = fields.Image(string="Platform Logo")
    subscription_type = fields.Selection([
        ('free', 'Free'),
        ('subscription', 'Subscription'),
        ('pay_per_view', 'Pay Per View')
    ], string="Subscription Type")

    # DVD Distribution Fields
    dvd_publisher_name = fields.Char("DVD Publisher")
    dvd_release_date = fields.Date("DVD Release Date")
    dvd_region_code = fields.Selection([
        ('1', 'Region 1 (US & Canada)'),
        ('2', 'Region 2 (Europe, Japan)'),
        ('3', 'Region 3 (SE Asia)'),
        ('4', 'Region 4 (Australia, Latin America)'),
        ('5', 'Region 5 (Russia, Africa)'),
        ('6', 'Region 6 (China)')
    ], string="DVD Region Code")
    dvd_format = fields.Selection([
        ('dvd', 'DVD'),
        ('bluray', 'Blu-ray'),
        ('4k', '4K UHD')
    ], string="DVD Format")
    dvd_packaging_type = fields.Selection([
        ('jewel_case', 'Jewel Case'),
        ('digipak', 'Digipak'),
        ('steelbook', 'Steelbook'),
        ('slim_case', 'Slim Case')
    ], string="Packaging Type")
    dvd_copies_distributed = fields.Integer("Number of Copies Distributed")
    dvd_manufacturer_contact = fields.Char("Manufacturer Contact")
    dvd_manufacturer_phone = fields.Char("Manufacturer Phone")
    dvd_manufacturer_email = fields.Char("Manufacturer Email")
    dvd_distribution_region = fields.Char("Distribution Region")
    dvd_notes = fields.Text("Additional Notes")

    @api.depends('distribution_type')
    def _compute_type_flags(self):
        for rec in self:
            rec.is_theatre = rec.distribution_type == 'theatre'
            rec.is_ott = rec.distribution_type == 'ott'
            rec.is_dvd = rec.distribution_type == 'dvd'


class LegalPartner(models.Model):
    _name = 'partner.legal'
    _description = 'Legal Partner'

    name = fields.Char(string='Partner Name', required=True)
    logo = fields.Binary(string='Logo')
    lawyer_name = fields.Char(string='Lawyer Name')
    contact_email = fields.Char(string='Contact Email')
    phone_number = fields.Char(string='Phone Number')
    services_provided = fields.Text(string='Services Provided')


class MerchandisePartner(models.Model):
    _name = 'partner.merchandise'
    _description = 'Merchandise Partner'


    name = fields.Char(string='Merchandise Partner Name', required=True)
    brand_name = fields.Char(string='Brand Name')
    logo = fields.Binary(string='Brand Logo')
    product_categories = fields.Char(string='Product Categories')  # e.g. T-Shirts, Mugs, Posters
    contact_person = fields.Char(string='Contact Person')
    contact_email = fields.Char(string='Contact Email')
    phone_number = fields.Char(string='Phone Number')
    partnership_start_date = fields.Date(string='Partnership Start Date')
    exclusive_merchandise = fields.Boolean(string='Exclusive Merchandise Deal')


class EventPartner(models.Model):
    _name = 'partner.event'
    _description = 'Event Partner'

    name = fields.Char(string='Partner Name', required=True)
    logo = fields.Binary(string='Logo')
    event_type = fields.Selection([
        ('premiere', 'Premiere'),
        ('press_meet', 'Press Meet'),
        ('fan_meet', 'Fan Meet'),
        ('other', 'Other'),
    ], string='Event Type')
    contact_person = fields.Char(string='Contact Person')
    contact_email = fields.Char(string='Contact Email')
    phone_number = fields.Char(string='Phone Number')


class VFXPostPartner(models.Model):
    _name = 'partner.vfx_post'
    _description = 'VFX & Post-production Partner'

    name = fields.Char(string='Partner Name', required=True)
    logo = fields.Binary(string='Logo')
    specialization = fields.Char(string='Specialization')
    project_count = fields.Integer(string='Number of Projects Completed')
    contact_email = fields.Char(string='Contact Email')
    phone_number = fields.Char(string='Phone Number')


class TalentAgencyPartner(models.Model):
    _name = 'partner.talent_agency'
    _description = 'Talent Agency Partner'

    name = fields.Char(string='Agency Name', required=True)
    logo = fields.Binary(string='Logo')
    talent_types = fields.Char(string='Types of Talent')
    contact_person = fields.Char(string='Contact Person')
    contact_email = fields.Char(string='Contact Email')
    phone_number = fields.Char(string='Phone Number')


class CinemaChainPartner(models.Model):
    _name = 'partner.cinema_chain'
    _description = 'Cinema Chain Partner'

    name = fields.Char(string='Cinema Chain Name', required=True)
    logo = fields.Binary(string='Logo')
    number_of_screens = fields.Integer(string='Number of Screens')
    regions_covered = fields.Char(string='Regions Covered')
    contact_email = fields.Char(string='Contact Email')
    phone_number = fields.Char(string='Phone Number')


class InternationalSalesPartner(models.Model):
    _name = 'partner.intl_sales'
    _description = 'International Sales Partner'

    name = fields.Char(string='Partner Name', required=True)
    logo = fields.Binary(string='Logo')
    regions_covered = fields.Char(string='Regions Covered')
    contact_person = fields.Char(string='Contact Person')
    contact_email = fields.Char(string='Contact Email')
    phone_number = fields.Char(string='Phone Number')


class SubtitlingDubbingPartner(models.Model):
    _name = 'partner.subtitling_dubbing'
    _description = 'Subtitling & Dubbing Partner'

    name = fields.Char(string='Partner Name', required=True)
    logo = fields.Binary(string='Logo')
    services_offered = fields.Char(string='Services Offered')  # e.g. subtitling, dubbing
    languages_supported = fields.Char(string='Languages Supported')
    contact_person = fields.Char(string='Contact Person')
    contact_email = fields.Char(string='Contact Email')
    phone_number = fields.Char(string='Phone Number')


class FoodBeveragePartner(models.Model):
    _name = 'partner.food_beverage'
    _description = 'Food & Beverage Partner'

    name = fields.Char(string='Partner Name', required=True)
    logo = fields.Binary(string='Logo')
    product_categories = fields.Char(string='Product Categories')
    contact_email = fields.Char(string='Contact Email')
    phone_number = fields.Char(string='Phone Number')


class TravelAccommodationPartner(models.Model):
    _name = 'partner.travel_accommodation'
    _description = 'Travel & Accommodation Partner'

    name = fields.Char(string='Partner Name', required=True)
    logo = fields.Binary(string='Logo')
    services_offered = fields.Char(string='Services Offered')
    contact_email = fields.Char(string='Contact Email')
    phone_number = fields.Char(string='Phone Number')

