from unittest.mock import patch

from fastapi import requests
from app.services.instagram_insights import InstagramInsightsService

class MockResponse:
    def __init__(self, json_data, status_code):
        self.json_data = json_data
        self.status_code = status_code

    def json(self):
        return self.json_data

    def raise_for_status(self):
        if self.status_code != 200:
            raise requests.HTTPError(f"{self.status_code} Error")

@patch('app.services.instagram_insights.requests.get')
def test_get_top_posts(mock_get):
    mock_media_response = {
        "data": [
            {
                "id": "1",
                "like_count": 100,
                "comments_count": 20,
                "media_type": "IMAGE",
                "caption": "First post",
                "media_url": "http://example.com/image1.jpg",
                "permalink": "http://instagram.com/p/1",
                "timestamp": "2023-01-15T12:34:56Z"
            },
            {
                "id": "2",
                "like_count": 150,
                "comments_count": 30,
                "media_type": "VIDEO",
                "caption": "Second post",
                "media_url": "http://example.com/video1.mp4",
                "permalink": "http://instagram.com/p/2",
                "timestamp": "2023-01-16T12:34:56Z"
            },
            {
                "id": "3",
                "like_count": 50,
                "comments_count": 10,
                "media_type": "IMAGE",
                "caption": "Third post",
                "media_url": "http://example.com/image2.jpg",
                "permalink": "http://instagram.com/p/3",
                "timestamp": "2023-01-17T12:34:56Z"
            },
        ]
    }
    mock_get.return_value = MockResponse(mock_media_response, 200)

    service = InstagramInsightsService()
    top_posts = service.get_top_posts(limit=2)
    assert len(top_posts) == 2
    assert top_posts[0]['id'] == "2"
    assert top_posts[1]['id'] == "1"
