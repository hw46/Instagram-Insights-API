# app/routers/insights.py

from fastapi import APIRouter, Depends, Request, HTTPException, Query
from typing import Optional
from app.services.instagram_insights import InstagramInsightsService
from app.models.schemas import (
    AccountInsights,
    TopPostsResponse,
    AudienceDemographics,
    GrowthTrends,
)
from slowapi import Limiter
from slowapi.util import get_remote_address
from app.core.config import limiter

router = APIRouter(prefix="/insights", tags=["Insights"])

# Dependency to get the service instance
def get_insights_service():
    return InstagramInsightsService()

@router.get("/account", response_model=AccountInsights)
@limiter.limit("10/minute")
async def get_account_insights(
    request: Request,
    since: Optional[str] = Query(None, description="Start date in YYYY-MM-DD"),
    until: Optional[str] = Query(None, description="End date in YYYY-MM-DD"),
    service: InstagramInsightsService = Depends(get_insights_service),
):
    """
    Retrieve account-level insights such as follower count, reach, and impressions for a specified time range.
    """
    try:
        data = service.get_account_insights(since=since, until=until)
        # Parse the data according to the AccountInsights schema
        # Adjust parsing based on actual API response structure
        insights = AccountInsights(
            follower_count=data.get("follower_count", 0),
            reach=data.get("reach", 0),
            impressions=data.get("impressions", 0),
            profile_views=data.get("profile_views", 0),
            website_clicks=data.get("website_clicks", 0),
            date_range={"since": since, "until": until},
        )
        return insights
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/top-posts", response_model=TopPostsResponse)
@limiter.limit("10/minute")
async def get_top_posts(
    request: Request,
    limit: int = Query(5, ge=1, le=100, description="Number of top posts to retrieve"),
    service: InstagramInsightsService = Depends(get_insights_service),
):
    """
    Retrieve top-performing posts based on engagement metrics.
    """
    try:
        top_posts_data = service.get_top_posts(limit=limit)
        top_posts = [
            {
                "post_id": post["id"],
                "caption": post.get("caption"),
                "media_type": post.get("media_type"),
                "media_url": post.get("media_url"),
                "permalink": post.get("permalink"),
                "timestamp": post.get("timestamp"),
                "like_count": post.get("like_count", 0),
                "comment_count": post.get("comments_count", 0),
                "engagement": post.get("engagement", 0),
            }
            for post in top_posts_data
        ]
        return TopPostsResponse(top_posts=top_posts)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/audience", response_model=AudienceDemographics)
@limiter.limit("10/minute")
async def get_audience_demographics(
    request: Request,
    service: InstagramInsightsService = Depends(get_insights_service),
):
    """
    Analyze audience demographics such as age, gender, and location.
    """
    try:
        demographics = service.get_audience_demographics()
        return AudienceDemographics(**demographics)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/growth-trends", response_model=GrowthTrends)
@limiter.limit("10/minute")
async def get_growth_trends(
    request: Request,
    since: Optional[str] = Query(None, description="Start date in YYYY-MM-DD"),
    until: Optional[str] = Query(None, description="End date in YYYY-MM-DD"),
    service: InstagramInsightsService = Depends(get_insights_service),
):
    """
    Calculate and return growth trends such as follower growth rate and engagement rate changes over time.
    """
    try:
        trends = service.calculate_growth_trends(since=since, until=until)
        return GrowthTrends(**trends)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
