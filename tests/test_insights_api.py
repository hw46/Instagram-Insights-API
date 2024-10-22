import pytest
from unittest.mock import patch
from fastapi.testclient import TestClient
from app.main import app
from app.core.config import settings

client = TestClient(app)

# Mocked data
mock_account_insights = {
    "follower_count": 1500,
    "reach": 5000,
    "impressions": 7000,
    "profile_views": 3000,
    "website_clicks": 150,
    "date_range": {"since": "2023-01-01", "until": "2023-01-31"}
}

mock_top_posts = {
    "top_posts": [
        {
            "post_id": "2",
            "caption": "Second post",
            "media_type": "VIDEO",
            "media_url": "http://example.com/video1.mp4",
            "permalink": "http://instagram.com/p/2",
            "timestamp": "2023-01-16T12:34:56Z",
            "like_count": 150,
            "comment_count": 30,
            "engagement": 180
        },
        {
            "post_id": "1",
            "caption": "First post",
            "media_type": "IMAGE",
            "media_url": "http://example.com/image1.jpg",
            "permalink": "http://instagram.com/p/1",
            "timestamp": "2023-01-15T12:34:56Z",
            "like_count": 100,
            "comment_count": 20,
            "engagement": 120
        }
    ]
}

mock_audience_demographics = {
    "gender": {"male": 60, "female": 40},
    "age_ranges": {"18-24": 25, "25-34": 30},
    "countries": {"US": 50, "CA": 20}
}

mock_growth_trends = {
    "follower_growth_rate": 11.11,
    "engagement_rate_change": -2.78,
    "date_range": {"since": "2023-01-01", "until": "2023-01-31"}
}

@patch('app.services.instagram_insights.InstagramInsightsService.get_account_insights')
def test_get_account_insights_endpoint(mock_get_insights):
    mock_get_insights.return_value = {
        "follower_count": 1500,
        "reach": 5000,
        "impressions": 7000,
        "profile_views": 3000,
        "website_clicks": 150
    }

    response = client.get("/insights/account?since=2023-01-01&until=2023-01-31")
    assert response.status_code == 200
    assert response.json() == mock_account_insights

@patch('app.services.instagram_insights.InstagramInsightsService.get_top_posts')
def test_get_top_posts_endpoint(mock_get_top_posts):
    mock_get_top_posts.return_value = [
        {
            "id": "2",
            "like_count": 150,
            "comments_count": 30,
            "media_type": "VIDEO",
            "caption": "Second post",
            "media_url": "http://example.com/video1.mp4",
            "permalink": "http://instagram.com/p/2",
            "timestamp": "2023-01-16T12:34:56Z",
            "engagement": 180
        },
        {
            "id": "1",
            "like_count": 100,
            "comments_count": 20,
            "media_type": "IMAGE",
            "caption": "First post",
            "media_url": "http://example.com/image1.jpg",
            "permalink": "http://instagram.com/p/1",
            "timestamp": "2023-01-15T12:34:56Z",
            "engagement": 120
        }
    ]

    response = client.get("/insights/top-posts?limit=2")
    assert response.status_code == 200
    assert response.json() == mock_top_posts

@patch('app.services.instagram_insights.InstagramInsightsService.get_audience_demographics')
def test_get_audience_demographics_endpoint(mock_get_demographics):
    mock_get_demographics.return_value = mock_audience_demographics

    response = client.get("/insights/audience")
    assert response.status_code == 200
    assert response.json() == mock_audience_demographics

@patch('app.services.instagram_insights.InstagramInsightsService.calculate_growth_trends')
def test_get_growth_trends_endpoint(mock_calculate_trends):
    mock_calculate_trends.return_value = mock_growth_trends

    response = client.get("/insights/growth-trends?since=2023-01-01&until=2023-01-31")
    assert response.status_code == 200
    assert response.json() == mock_growth_trends

def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the Instagram Insights API!"}
