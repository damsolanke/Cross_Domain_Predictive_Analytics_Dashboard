"""
Social media API client for Twitter API integration.
Provides social media data retrieval and processing functionality.
"""

from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta
from .base_client import BaseAPIClient

class SocialMediaAPIClient(BaseAPIClient):
    def __init__(self, api_key: str, api_secret: str, access_token: str, access_token_secret: str,
                 cache_dir: str = "cache/social"):
        """
        Initialize the Social Media API client.
        
        Args:
            api_key (str): Twitter API key
            api_secret (str): Twitter API secret
            access_token (str): Twitter access token
            access_token_secret (str): Twitter access token secret
            cache_dir (str): Directory for caching social media data
        """
        super().__init__(
            base_url="https://api.twitter.com/2",
            api_key=api_key,
            cache_dir=cache_dir
        )
        self.api_secret = api_secret
        self.access_token = access_token
        self.access_token_secret = access_token_secret
        
        # Configure OAuth1 authentication
        self.session.auth = requests_oauthlib.OAuth1(
            api_key,
            api_secret,
            access_token,
            access_token_secret
        )
    
    def search_tweets(self, query: str, max_results: int = 100,
                     start_time: Optional[datetime] = None,
                     end_time: Optional[datetime] = None) -> Dict[str, Any]:
        """
        Search for tweets matching a query.
        
        Args:
            query (str): Search query
            max_results (int): Maximum number of results to return
            start_time (Optional[datetime]): Start time for search
            end_time (Optional[datetime]): End time for search
            
        Returns:
            Dict[str, Any]: Search results
        """
        params = {
            'query': query,
            'max_results': max_results,
            'tweet.fields': 'created_at,public_metrics,entities',
            'expansions': 'author_id,geo.place_id',
            'user.fields': 'name,username,public_metrics'
        }
        
        if start_time:
            params['start_time'] = start_time.isoformat()
        if end_time:
            params['end_time'] = end_time.isoformat()
        
        return self.get('tweets/search/recent', params=params)
    
    def get_trending_topics(self, woeid: int = 1) -> Dict[str, Any]:
        """
        Get trending topics for a location.
        
        Args:
            woeid (int): Where On Earth ID for location
            
        Returns:
            Dict[str, Any]: Trending topics
        """
        params = {
            'id': woeid
        }
        
        return self.get('trends/place', params=params)
    
    def get_user_tweets(self, user_id: str, max_results: int = 100) -> Dict[str, Any]:
        """
        Get tweets from a specific user.
        
        Args:
            user_id (str): Twitter user ID
            max_results (int): Maximum number of results to return
            
        Returns:
            Dict[str, Any]: User tweets
        """
        params = {
            'max_results': max_results,
            'tweet.fields': 'created_at,public_metrics,entities',
            'expansions': 'geo.place_id'
        }
        
        return self.get(f'users/{user_id}/tweets', params=params)
    
    def process_tweet_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process raw tweet data into a standardized format.
        
        Args:
            data (Dict[str, Any]): Raw tweet data from API
            
        Returns:
            Dict[str, Any]: Processed tweet data
        """
        if 'data' not in data:
            return data
        
        processed_data = {
            'tweets': [],
            'users': {},
            'places': {}
        }
        
        # Process tweets
        for tweet in data['data']:
            processed_tweet = {
                'id': tweet['id'],
                'text': tweet['text'],
                'created_at': tweet['created_at'],
                'metrics': tweet['public_metrics'],
                'entities': tweet.get('entities', {}),
                'author_id': tweet.get('author_id'),
                'place_id': tweet.get('geo', {}).get('place_id')
            }
            processed_data['tweets'].append(processed_tweet)
        
        # Process users
        if 'includes' in data and 'users' in data['includes']:
            for user in data['includes']['users']:
                processed_data['users'][user['id']] = {
                    'name': user['name'],
                    'username': user['username'],
                    'metrics': user['public_metrics']
                }
        
        # Process places
        if 'includes' in data and 'places' in data['includes']:
            for place in data['includes']['places']:
                processed_data['places'][place['id']] = {
                    'name': place['name'],
                    'country': place['country'],
                    'country_code': place['country_code']
                }
        
        return processed_data
    
    def get_sentiment_analysis(self, tweets: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Perform sentiment analysis on a list of tweets.
        
        Args:
            tweets (List[Dict[str, Any]]): List of tweets to analyze
            
        Returns:
            Dict[str, Any]: Sentiment analysis results
        """
        # This is a placeholder for actual sentiment analysis implementation
        # In a real implementation, you would use a sentiment analysis library
        # or service like TextBlob, NLTK, or a cloud service
        
        sentiments = {
            'positive': 0,
            'neutral': 0,
            'negative': 0,
            'tweets': []
        }
        
        for tweet in tweets:
            # Placeholder sentiment calculation
            # In reality, you would use proper sentiment analysis here
            sentiment = 'neutral'  # This would be calculated
            
            sentiments[sentiment] += 1
            sentiments['tweets'].append({
                'id': tweet['id'],
                'text': tweet['text'],
                'sentiment': sentiment
            })
        
        return sentiments 