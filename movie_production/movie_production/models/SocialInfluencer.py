import requests
from odoo import models, fields, api
from datetime import datetime

class SocialInfluencer(models.Model):
    _name = 'movie.social.influencer'
    _description = 'Social Media Influencer'

    name = fields.Char("Influencer Name", required=True)
    platform = fields.Selection([('instagram', 'Instagram'), ('facebook', 'Facebook')], required=True)
    social_id = fields.Char("Instagram ID / Facebook Page ID", required=True)
    access_token = fields.Char("Access Token", required=True)
    followers = fields.Integer("Followers", default=0)
    total_posts = fields.Integer("Total Posts/Reels", default=0)
    avg_likes = fields.Float("Average Likes", default=0.0)
    avg_comments = fields.Float("Average Comments", default=0.0)
    engagement_score = fields.Float("Engagement Score", compute="_compute_engagement", store=True)
    last_updated = fields.Datetime("Last Synced", readonly=True)

    @api.depends('followers', 'avg_likes', 'avg_comments')
    def _compute_engagement(self):
        for rec in self:
            rec.engagement_score = (rec.avg_likes + rec.avg_comments) * 0.5 + rec.followers * 0.01

    def fetch_influencer_data(self):
        for rec in self:
            if not rec.access_token or not rec.social_id:
                continue

            try:
                if rec.platform == 'instagram':
                    url = (
                        f"https://graph.facebook.com/v17.0/{rec.social_id}"
                        f"?fields=followers_count,media.limit(10){{like_count,comments_count}}"
                        f"&access_token={rec.access_token}"
                    )
                else:  # facebook
                    url = (
                        f"https://graph.facebook.com/v17.0/{rec.social_id}"
                        f"?fields=fan_count,posts.limit(10){{likes.summary(true),comments.summary(true)}}"
                        f"&access_token={rec.access_token}"
                    )

                response = requests.get(url, timeout=10)
                response.raise_for_status()
                data = response.json()

                if rec.platform == 'instagram':
                    rec.followers = data.get("followers_count", 0)
                    media = data.get("media", {}).get("data", [])
                    if media:
                        rec.total_posts = len(media)
                        total_likes = sum(m.get('like_count', 0) for m in media)
                        total_comments = sum(m.get('comments_count', 0) for m in media)
                        rec.avg_likes = total_likes / len(media)
                        rec.avg_comments = total_comments / len(media)
                    else:
                        rec.total_posts = 0
                        rec.avg_likes = 0
                        rec.avg_comments = 0

                else:  # facebook
                    rec.followers = data.get("fan_count", 0)
                    posts = data.get("posts", {}).get("data", [])
                    total_likes = 0
                    total_comments = 0
                    for post in posts:
                        post_id = post.get('id')
                        if not post_id:
                            continue
                        stats_url = (
                            f"https://graph.facebook.com/v17.0/{post_id}"
                            f"?fields=likes.summary(true),comments.summary(true)"
                            f"&access_token={rec.access_token}"
                        )
                        stats_response = requests.get(stats_url, timeout=10)
                        stats_response.raise_for_status()
                        stats = stats_response.json()
                        total_likes += stats.get("likes", {}).get("summary", {}).get("total_count", 0)
                        total_comments += stats.get("comments", {}).get("summary", {}).get("total_count", 0)

                    if posts:
                        rec.total_posts = len(posts)
                        rec.avg_likes = total_likes / len(posts)
                        rec.avg_comments = total_comments / len(posts)
                    else:
                        rec.total_posts = 0
                        rec.avg_likes = 0
                        rec.avg_comments = 0

                rec.last_updated = datetime.now()

            except requests.RequestException as e:
                _logger = self.env['ir.logging']
                _logger.sudo().create({
                    'name': 'Social Influencer API Error',
                    'type': 'server',
                    'dbname': self._cr.dbname,
                    'level': 'error',
                    'message': f"Error fetching data for {rec.name}: {str(e)}",
                    'path': 'movie.social.influencer',
                    'func': 'fetch_influencer_data',
                    'line': 'N/A',
                })
                continue

    def action_fetch_data(self):
        self.fetch_influencer_data()
