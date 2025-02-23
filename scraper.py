import praw
import pandas as pd
from datetime import datetime
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def initialize_reddit():
    """Initialize Reddit API connection"""
    return praw.Reddit(
        client_id=os.getenv('REDDIT_CLIENT_ID'),
        client_secret=os.getenv('REDDIT_CLIENT_SECRET'),
        user_agent=os.getenv('REDDIT_USER_AGENT', 'StopSmokingAnalyzer/1.0')
    )

def scrape_posts(subreddit_name='stopsmoking', limit=15, post_type='hot'):
    """
    Scrape posts from specified subreddit
    post_type can be 'hot', 'top', or 'new'
    """
    reddit = initialize_reddit()
    subreddit = reddit.subreddit(subreddit_name)
    
    # Select the type of posts to fetch
    if post_type == 'hot':
        posts = subreddit.hot(limit=limit)
    elif post_type == 'top':
        posts = subreddit.top(limit=limit)
    else:
        posts = subreddit.new(limit=limit)
    
    post_data = []
    for post in posts:
        # Skip stickied posts
        if post.stickied:
            continue
            
        # Get post data
        post_info = {
            'id': post.id,
            'title': post.title,
            'body': post.selftext,
            'score': post.score,
            'created_utc': datetime.fromtimestamp(post.created_utc).isoformat(),
            'num_comments': post.num_comments,
            'upvote_ratio': post.upvote_ratio,
            'comments': []
        }
        
        # Get comments (excluding mod comments)
        post.comments.replace_more(limit=0)  # Expand comment forest
        for comment in post.comments:
            if not hasattr(comment, 'body') or comment.stickied:
                continue
                
            comment_info = {
                'id': comment.id,
                'body': comment.body,
                'score': comment.score,
                'created_utc': datetime.fromtimestamp(comment.created_utc).isoformat()
            }
            post_info['comments'].append(comment_info)
        
        post_data.append(post_info)
    
    return post_data

def save_to_json(data, filename='stopsmoking_data.json'):
    """Save scraped data to JSON file"""
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def main():
    # Scrape both hot and top posts to get a good mix
    hot_posts = scrape_posts(post_type='hot', limit=10)
    top_posts = scrape_posts(post_type='top', limit=5)
    
    all_posts = hot_posts + top_posts
    
    # Save data
    save_to_json(all_posts)
    
    print(f"Successfully scraped {len(all_posts)} posts with their comments")

if __name__ == "__main__":
    main()