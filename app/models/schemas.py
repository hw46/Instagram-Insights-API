# app/models/schemas.py

from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

# Schema for Account Insights
class AccountInsights(BaseModel):
    follower_count: int
    reach: int
    impressions: int
    profile_views: int
    website_clicks: int
    date_range: dict

# Schema for Top-Performing Posts
class TopPost(BaseModel):
    post_id: str
    caption: Optional[str]
    media_type: str
    media_url: str
    permalink: str
    timestamp: datetime
    like_count: int
    comment_count: int
    engagement: int  # Sum of likes and comments

class TopPostsResponse(BaseModel):
    top_posts: List[TopPost]

# Schema for Audience Demographics
class AudienceDemographics(BaseModel):
    gender: dict  # e.g., {"male": 60, "female": 40}
    age_ranges: dict  # e.g., {"13-17": 5, "18-24": 25, ...}
    countries: dict  # e.g., {"US": 50, "CA": 20, ...}

# Schema for Growth Trends
class GrowthTrends(BaseModel):
    follower_growth_rate: float  # Percentage
    engagement_rate_change: float  # Percentage
    date_range: dict
