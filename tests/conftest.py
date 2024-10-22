import pytest
from unittest.mock import patch

@pytest.fixture(scope="session", autouse=True)
def mock_settings():
    with patch('app.core.config.settings') as mock_settings:
        mock_settings.instagram_access_token = 'test_instagram_access_token'
        mock_settings.instagram_account_id = 'test_instagram_account_id'
        mock_settings.facebook_app_id = 'test_facebook_app_id'
        mock_settings.facebook_app_secret = 'test_facebook_app_secret'
        yield mock_settings