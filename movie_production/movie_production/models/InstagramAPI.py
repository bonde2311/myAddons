# import requests
# import logging
# from odoo import models, api
#
# _logger = logging.getLogger(__name__)
#
#
# class SocialAPI(models.AbstractModel):
#     _name = 'movie.social.api'
#     _description = 'Instagram + Facebook API Integration'
#
#     BASE_URL = 'https://graph.facebook.com/v19.0'
#
#     @api.model
#     def get_access_token(self):
#         return self.env['ir.config_parameter'].sudo().get_param('social.access_token')
#
#     def _make_request(self, url):
#         try:
#             response = requests.get(url, timeout=10)
#             response.raise_for_status()
#             return response.json()
#         except requests.RequestException as e:
#             _logger.error("API request failed: %s", e)
#             return {}
#
#     @api.model
#     def fetch_instagram_data(self, influencer):
#         token = self.get_access_token()
#         ig_user_id = influencer.instagram_user_id
#
#         if not ig_user_id:
#             _logger.warning("No Instagram User ID found for influencer: %s", influencer.name)
#             influencer.recent_reel_data = "No data"
#             influencer.followers_count = 0
#             return
#
#         user_url = f"{self.BASE_URL}/{ig_user_id}?fields=username,followers_count&access_token={token}"
#         user_data = self._make_request(user_url)
#
#         influencer.followers_count = user_data.get('followers_count', 0)
#
#         reels_url = f"{self.BASE_URL}/{ig_user_id}/media?fields=id,media_type,media_url,like_count,comments_count,view_count,caption,timestamp&access_token={token}"
#         reels_data = self._make_request(reels_url)
#
#         reels = reels_data.get('data', [])
#         formatted = ""
#         for item in reels:
#             if item.get('media_type') == 'VIDEO':
#                 formatted += (
#                     f"\n📹 {item.get('caption') or 'No caption'}"
#                     f"\n❤️ {item.get('like_count', 0)}  👁 {item.get('view_count', 0)}  💬 {item.get('comments_count', 0)}"
#                     f"\n🔗 {item.get('media_url')}\n"
#                 )
#         influencer.recent_reel_data = formatted or "No data"
#
#     @api.model
#     def fetch_facebook_data(self, influencer):
#         token = self.get_access_token()
#         page_id = influencer.facebook_page_id
#
#         if not page_id:
#             _logger.warning("No Facebook Page ID for influencer: %s", influencer.name)
#             influencer.fb_followers = 0
#             influencer.recent_fb_posts = "No posts"
#             return
#
#         fb_url = f"{self.BASE_URL}/{page_id}?fields=followers_count&access_token={token}"
#         fb_data = self._make_request(fb_url)
#
#         influencer.fb_followers = fb_data.get('followers_count', 0)
#
#         posts_url = f"{self.BASE_URL}/{page_id}/posts?fields=message,permalink_url,created_time&access_token={token}"
#         posts_data = self._make_request(posts_url).get('data', [])
#
#         post_log = ""
#         for post in posts_data[:5]:
#             post_log += (
#                 f"\n📝 {post.get('message', 'No content')}"
#                 f"\n🔗 {post.get('permalink_url')}"
#                 f"\n🕒 {post.get('created_time')}\n"
#             )
#
#         influencer.recent_fb_posts = post_log or "No posts"
