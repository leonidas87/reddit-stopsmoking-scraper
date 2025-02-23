# Reddit r/stopsmoking Scraper

This tool scrapes posts and comments from r/stopsmoking to help understand smoking addiction narratives.

## Quick Start

1. Clone this repository:
```bash
git clone https://github.com/leonidas87/reddit-stopsmoking-scraper.git
cd reddit-stopsmoking-scraper
```

2. Install required packages:
```bash
pip install praw pandas python-dotenv
```

3. Set up Reddit API credentials:
   - Go to https://www.reddit.com/prefs/apps
   - Click "create another app..."
   - Choose "script"
   - Fill in the details
   - Note down your client_id and client_secret

4. Create a `.env` file with your Reddit API credentials:
```
REDDIT_CLIENT_ID=your_client_id
REDDIT_CLIENT_SECRET=your_client_secret
REDDIT_USER_AGENT=StopSmokingAnalyzer/1.0
```

5. Run the scraper:
```bash
python scraper.py
```

The script will create a `stopsmoking_data.json` file containing the scraped posts and comments.

## Data Format

The scraped data is saved in JSON format with the following structure:

```json
[
  {
    "id": "post_id",
    "title": "post_title",
    "body": "post_content",
    "score": 42,
    "created_utc": "2025-02-23T22:08:31",
    "num_comments": 10,
    "upvote_ratio": 0.95,
    "comments": [
      {
        "id": "comment_id",
        "body": "comment_content",
        "score": 5,
        "created_utc": "2025-02-23T22:09:31"
      }
    ]
  }
]
```

## Using the Data for LLM Training

The scraped data can be used to:
1. Train LLMs to understand smoking addiction patterns
2. Analyze common triggers and coping strategies
3. Study the language people use when discussing their quit journey
4. Identify successful quitting strategies and patterns

Consider preprocessing the data by:
- Removing personally identifiable information
- Cleaning and normalizing text
- Extracting key themes and patterns
- Converting to your LLM's preferred training format