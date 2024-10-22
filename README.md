# Instagram Insights API Integration

## Overview
This project is a FastAPI-based service that integrates with the Instagram Graph API to retrieve and analyze insights from an Instagram Business or Creator account. The service provides several endpoints to fetch account insights, top-performing posts, audience demographics, and growth trends.

## Features
- **Account Insights**: Retrieve follower count, reach, and impressions for a specified time range.
- **Top Posts**: Fetch top-performing posts based on engagement metrics such as likes and comments.
- **Audience Demographics**: Analyze the demographics of your Instagram audience (if available).
- **Growth Trends**: Calculate growth trends, including follower growth rate and engagement rate changes.

## Project Structure
```plaintext
Instagram_Insights_API/
├── app/
│   ├── core/               # Core configurations like rate limiting
│   ├── routers/            # FastAPI routes (API endpoints)
│   ├── services/           # Service layer that interacts with Instagram Graph API
│   ├── models/             # Pydantic models and schemas for API responses
│   └── main.py             # Main FastAPI application entry point
├── tests/                  # Unit and integration tests
├── .env                    # Environment variables (not included in version control)
├── README.md               # Project documentation
├── requirements.txt        # Python dependencies

## Testing
use uvicorn app.main:app --reload to run the applicationk
use http://127.0.0.1:8000/docs to run the interface