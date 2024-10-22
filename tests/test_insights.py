import requests
import pytest

def get_instagram_insights(access_token, instagram_account_id):
    url = f"https://graph.facebook.com/v17.0/{instagram_account_id}/insights"
    params = {
        "metric": "impressions,reach,profile_views",
        "access_token": access_token
    }
    response = requests.get(url, params=params)
    data = response.json()
    return data

def test_get_instagram_insights():
    access_token = 'EAAMZAJEHjSSMBO8TnnKZAbMnKFoIvu6XS0ZCG1bUnLoANXYpRYSj57MctMUsW0uzmH2ZCeDe28RJNbhiJzhErN2di2oj2nR9pZBbf7so3gA6WsmeUqBkfHVDPZCPp6ZArjK32hbrZCwsLnD01JunfRNa0L5oJPyZCZAkY7gftDKZA4o2SjmEkdb4iOC4p2SVCgPINWCwIsTcWLQ0CQDoZB1eYCmkxrWHXAZDZD'  # Replace with your actual access token
    instagram_account_id = '17841470344001904'
    
    insights = get_instagram_insights(access_token, instagram_account_id)
    
    assert 'data' in insights, "No 'data' field in response"
    assert isinstance(insights['data'], list), "'data' field should be a list"
    
    print(insights)
    
    if insights.get('data'):
        assert 'impressions' in insights['data'][0], "'impressions' not found in insights data"
        assert 'reach' in insights['data'][0], "'reach' not found in insights data"

if __name__ == "__main__":
    pytest.main(["-v", "tests/test_insights.py"])
