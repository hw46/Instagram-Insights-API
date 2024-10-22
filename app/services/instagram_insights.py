# app/services/instagram_insights.py

import os
import requests
from typing import Optional, List
from datetime import datetime, timedelta, timezone
from app.core.config import settings
import requests
from typing import Dict
from app.core.config import settings
from app.core.config import settings
import requests
from typing import Dict, List

class InstagramInsightsService:
    def __init__(self):
        self.access_token = settings.instagram_access_token
        self.instagram_account_id = settings.instagram_account_id
        self.facebook_app_id = settings.facebook_app_id
        self.facebook_app_secret = settings.facebook_app_secret
        self.base_url = "https://graph.instagram.com"

    def get_account_insights(self, since: str, until: str) -> Dict[str, int]:
        metrics = "follower_count,reach,impressions,profile_views,website_clicks"
        params = {
            "metric": metrics,
            "period": "day",
            "since": since,
            "until": until,
            "access_token": self.access_token
        }
        response = requests.get(f"{self.base_url}/{self.instagram_account_id}/insights", params=params)
        response.raise_for_status()
        data = response.json()

        insights = {}
        for metric in data.get("data", []):
            name = metric.get("name")
            value = metric.get("values", [{}])[0].get("value")
            if name and value is not None:
                insights[name] = value

        return insights

    def get_top_posts(self, limit: int = 5) -> List[Dict]:
        media_endpoint = f"{self.base_url}/{self.instagram_account_id}/media"
        params = {
            "fields": "id,like_count,comments_count,media_type,caption,media_url,permalink,timestamp",
            "access_token": self.access_token,
            "limit": limit
        }
        response = requests.get(media_endpoint, params=params)
        response.raise_for_status()
        media_data = response.json()

        posts = media_data.get("data", [])
        # Calculate engagement and sort
        for post in posts:
            post['engagement'] = post.get('like_count', 0) + post.get('comments_count', 0)
        
        sorted_posts = sorted(posts, key=lambda x: x['engagement'], reverse=True)
        return sorted_posts[:limit]

    def get_audience_demographics(self):
        """
        Fetch audience demographics.
        Note: Instagram Graph API's access to audience demographics may be limited.
        """
        # Placeholder implementation
        # Replace with actual API call if available
        demographics = {
            "gender": {"male": 60, "female": 40},
            "age_ranges": {"13-17": 5, "18-24": 25, "25-34": 30, "35-44": 20, "45-54": 10, "55-64": 5, "65+": 5},
            "countries": {"US": 50, "CA": 20, "GB": 15, "AU": 10, "DE": 5},
        }
        return demographics

    def calculate_growth_trends(self, since: str, until: str) -> Dict[str, float]:
        current_insights = self.get_account_insights(since=since, until=until)
        previous_since = (datetime.now(timezone.utc) - timedelta(days=60)).strftime("%Y-%m-%d")
        previous_until = (datetime.now(timezone.utc) - timedelta(days=30)).strftime("%Y-%m-%d")
        previous_insights = self.get_account_insights(since=previous_since, until=previous_until)

        trends = {}

        # Calculate follower growth rate
        current_followers = current_insights.get("follower_count", 0)
        previous_followers = previous_insights.get("follower_count", 0)
        if previous_followers > 0:
            growth_rate = ((current_followers - previous_followers) / previous_followers) * 100
        else:
            growth_rate = 0.0
        trends["follower_growth_rate"] = round(growth_rate, 2)

        return trends
