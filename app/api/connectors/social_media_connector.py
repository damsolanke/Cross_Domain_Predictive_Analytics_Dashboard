"""
Social Media data API connector
"""
import os
import time
import json
import hashlib
import random
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta
from app.api.connectors.base_connector import BaseConnector

class SocialMediaConnector(BaseConnector):
    """Connector for social media trend data"""
    
    def __init__(self):
        """Initialize the social media connector"""
        super().__init__(
            name="Social Media Trends",
            description="Provides trending topics, sentiment analysis, and engagement metrics from social media platforms",
            cache_ttl=900  # 15 minutes cache (trends change quickly)
        )
        # API configuration
        self.api_key = os.environ.get('SOCIAL_MEDIA_API_KEY', 'demo_key')
        self.base_url = "https://api.socialmediatrends.com"  # Placeholder URL
        
        # Default platform if none provided
        self.default_platform = "twitter"
    
    def fetch_data(self, params: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Fetch social media data based on parameters

        Args:
            params: Parameters for the social media data request
                - platform: Social media platform (twitter, facebook, instagram, etc.) or 'news' for news API
                - data_type: Type of data (trends, sentiment, engagement)
                - topic: Topic filter (optional)
                - timeframe: Time period (hour, day, week)
                - location: Geographic region (global, country code, etc.)

        Returns:
            Dictionary of social media data
        """
        if params is None:
            params = {}

        # Get request parameters
        platform = params.get('platform', self.default_platform)
        data_type = params.get('data_type', 'trends')
        topic = params.get('topic', None)
        timeframe = params.get('timeframe', 'day')
        location = params.get('location', 'global')

        # Create cache key based on parameters
        cache_key = self._create_cache_key(platform, data_type, topic, timeframe, location)

        # Check cache first
        cached_data = self._check_cache(cache_key)
        if cached_data:
            return cached_data

        try:
            self._update_status("fetching")

            # Use News API for real-time trend and sentiment data (used as proxy for social media)
            if platform.lower() == 'news':
                # News API is a good proxy for social media trends and sentiment
                if data_type == 'trends':
                    data = self._get_real_news_trends(topic, timeframe, location)
                elif data_type == 'sentiment':
                    data = self._get_real_news_sentiment(topic, timeframe, location)
                else:
                    # Engagement doesn't have a direct News API equivalent, use simulation
                    data = self._get_simulated_engagement(platform, timeframe, location, topic)
            else:
                # For specific social platforms, fallback to simulated data
                # (Direct social media API access requires OAuth and complex permissions)
                if data_type == 'trends':
                    data = self._get_simulated_trends(platform, timeframe, location, topic)
                elif data_type == 'sentiment':
                    data = self._get_simulated_sentiment(platform, timeframe, location, topic)
                elif data_type == 'engagement':
                    data = self._get_simulated_engagement(platform, timeframe, location, topic)
                else:
                    raise ValueError(f"Unsupported data type: {data_type}")

            # Cache the results
            self._update_cache(cache_key, data)

            self._update_status("success")
            return data

        except Exception as e:
            self._update_status("error", e)
            print(f"Social media API error: {str(e)}")

            # Fallback to simulated data
            try:
                if data_type == 'trends':
                    data = self._get_simulated_trends(platform, timeframe, location, topic)
                elif data_type == 'sentiment':
                    data = self._get_simulated_sentiment(platform, timeframe, location, topic)
                elif data_type == 'engagement':
                    data = self._get_simulated_engagement(platform, timeframe, location, topic)
                else:
                    raise ValueError(f"Unsupported data type: {data_type}")

                # Cache the fallback results
                self._update_cache(cache_key, data)

                self._update_status("using fallback data")
                return data
            except Exception as fallback_error:
                self._update_status("error", fallback_error)
                return {
                    'error': str(e),
                    'fallback_error': str(fallback_error),
                    'status': 'error'
                }

    def _get_real_news_trends(self, topic: Optional[str], timeframe: str, location: str) -> Dict[str, Any]:
        """
        Get real trending news topics using News API as a proxy for social media trends
        """
        import requests
        from datetime import datetime, timedelta

        # News API key - use demo if not set
        api_key = self.api_key if self.api_key != 'demo_key' else '20ce415fb7e84e18a9ee5c340f6b8f0b'  # Sample key, limited usage

        # Calculate date range based on timeframe
        end_date = datetime.now()
        if timeframe == 'hour':
            # News API doesn't support hourly, use day
            start_date = end_date - timedelta(days=1)
        elif timeframe == 'day':
            start_date = end_date - timedelta(days=1)
        elif timeframe == 'week':
            start_date = end_date - timedelta(days=7)
        else:
            # Default to day
            start_date = end_date - timedelta(days=1)

        # Format dates for API
        from_date = start_date.strftime('%Y-%m-%d')
        to_date = end_date.strftime('%Y-%m-%d')

        # Map location to country code for News API
        country_mappings = {
            'global': None,  # No country filter
            'us': 'us',
            'uk': 'gb',
            'canada': 'ca',
            'australia': 'au',
            'germany': 'de',
            'france': 'fr',
            'japan': 'jp',
            'brazil': 'br',
            'india': 'in',
            'mexico': 'mx'
        }

        # Convert location to appropriate country code
        country = country_mappings.get(location.lower(), None)

        try:
            api_url = "https://newsapi.org/v2/top-headlines"

            # Prepare parameters
            params = {
                'apiKey': api_key,
                'pageSize': 100,  # Maximum articles per request
                'language': 'en',
            }

            # Add optional parameters
            if country:
                params['country'] = country

            if topic:
                params['q'] = topic

            # Make the API request
            response = requests.get(api_url, params=params, timeout=10)

            if response.status_code == 200:
                data = response.json()

                # Process articles to extract trends
                articles = data.get('articles', [])

                # Group and count by categories/topics
                topics_count = {}

                for article in articles:
                    # Extract categories from title and description
                    title = article.get('title', '')
                    description = article.get('description', '')
                    source = article.get('source', {}).get('name', '')

                    # Simple topic extraction (in a real app, we'd use NLP)
                    keywords = self._extract_keywords(f"{title} {description}")

                    for keyword in keywords:
                        if keyword in topics_count:
                            topics_count[keyword]['count'] += 1
                            topics_count[keyword]['sources'].add(source)
                        else:
                            topics_count[keyword] = {
                                'count': 1,
                                'sources': {source},
                                'category': self._categorize_keyword(keyword)
                            }

                # Convert to trend format
                trending_topics = []
                for keyword, data in topics_count.items():
                    # Calculate basic growth rate (random for demo)
                    growth_rate = random.uniform(-20, 100)

                    trending_topics.append({
                        'topic': keyword,
                        'category': data['category'],
                        'volume': data['count'],
                        'growth_rate': round(growth_rate, 1),
                        'sources': len(data['sources']),
                        'rank': 0  # Will be set after sorting
                    })

                # Sort by volume
                trending_topics.sort(key=lambda x: x['volume'], reverse=True)

                # Add ranks
                for i, trend in enumerate(trending_topics):
                    trend['rank'] = i + 1

                # Limit to top 20
                trending_topics = trending_topics[:20]

                # Return in our standard format
                return {
                    'platform': 'news',
                    'timestamp': datetime.now().isoformat(),
                    'location': location,
                    'timeframe': timeframe,
                    'trending_topics': trending_topics
                }
            else:
                raise Exception(f"News API returned status code: {response.status_code} - {response.text}")

        except Exception as e:
            raise Exception(f"News API fetch error: {str(e)}")

    def _get_real_news_sentiment(self, topic: Optional[str], timeframe: str, location: str) -> Dict[str, Any]:
        """
        Get real news sentiment using News API and basic sentiment analysis
        """
        import requests
        from datetime import datetime, timedelta

        # News API key - use demo if not set
        api_key = self.api_key if self.api_key != 'demo_key' else '20ce415fb7e84e18a9ee5c340f6b8f0b'  # Sample key, limited usage

        # Set up default topic if none provided
        query = topic if topic else "technology OR business OR politics OR sports OR entertainment"

        # Calculate date range based on timeframe
        end_date = datetime.now()
        if timeframe == 'hour':
            # News API doesn't support hourly, use day
            start_date = end_date - timedelta(days=1)
        elif timeframe == 'day':
            start_date = end_date - timedelta(days=1)
        elif timeframe == 'week':
            start_date = end_date - timedelta(days=7)
        else:
            # Default to day
            start_date = end_date - timedelta(days=1)

        # Format dates for API
        from_date = start_date.strftime('%Y-%m-%d')
        to_date = end_date.strftime('%Y-%m-%d')

        try:
            api_url = "https://newsapi.org/v2/everything"

            # Prepare parameters
            params = {
                'apiKey': api_key,
                'q': query,
                'from': from_date,
                'to': to_date,
                'language': 'en',
                'sortBy': 'popularity',
                'pageSize': 100  # Maximum articles per request
            }

            # Make the API request
            response = requests.get(api_url, params=params, timeout=10)

            if response.status_code == 200:
                data = response.json()

                # Process articles to analyze sentiment
                articles = data.get('articles', [])

                # Simple sentiment analysis
                positive_words = ['good', 'great', 'excellent', 'positive', 'success', 'improve', 'benefit', 'advantage',
                                'growth', 'increase', 'progress', 'innovation', 'solution', 'opportunity', 'profitable']

                negative_words = ['bad', 'poor', 'negative', 'fail', 'loss', 'decline', 'decrease', 'problem', 'risk',
                                'threat', 'crisis', 'danger', 'difficult', 'challenging', 'concern']

                # Initialize counters
                positive_count = 0
                negative_count = 0
                neutral_count = 0

                # Create sentiment timeline data
                sentiment_data = []
                date_sentiment = {}

                for article in articles:
                    # Extract text
                    title = article.get('title', '').lower()
                    description = article.get('description', '').lower()
                    full_text = f"{title} {description}"

                    # Count positive and negative words
                    pos = sum(1 for word in positive_words if word in full_text)
                    neg = sum(1 for word in negative_words if word in full_text)

                    # Determine sentiment
                    if pos > neg:
                        positive_count += 1
                        sentiment = 'positive'
                    elif neg > pos:
                        negative_count += 1
                        sentiment = 'negative'
                    else:
                        neutral_count += 1
                        sentiment = 'neutral'

                    # Extract date for timeline
                    published_at = article.get('publishedAt', '')
                    if published_at:
                        try:
                            date = published_at.split('T')[0]  # Get just the date part

                            if date not in date_sentiment:
                                date_sentiment[date] = {'positive': 0, 'negative': 0, 'neutral': 0, 'total': 0}

                            date_sentiment[date][sentiment] += 1
                            date_sentiment[date]['total'] += 1
                        except Exception:
                            pass

                # Calculate overall sentiment
                total = positive_count + negative_count + neutral_count
                if total > 0:
                    positive_ratio = positive_count / total
                    negative_ratio = negative_count / total
                    neutral_ratio = neutral_count / total
                else:
                    positive_ratio = 0.33
                    negative_ratio = 0.33
                    neutral_ratio = 0.34

                # Create timeline data
                for date, counts in sorted(date_sentiment.items()):
                    total = counts['total']
                    if total > 0:
                        sentiment_data.append({
                            'timestamp': f"{date}T12:00:00Z",  # Use noon as default time
                            'sentiment': {
                                'positive': round(counts['positive'] / total, 3),
                                'negative': round(counts['negative'] / total, 3),
                                'neutral': round(counts['neutral'] / total, 3)
                            },
                            'volume': total
                        })

                return {
                    'platform': 'news',
                    'topic': topic if topic else 'general',
                    'timestamp': datetime.now().isoformat(),
                    'location': location,
                    'timeframe': timeframe,
                    'sentiment_data': sentiment_data,
                    'overall_sentiment': {
                        'positive': round(positive_ratio, 3),
                        'negative': round(negative_ratio, 3),
                        'neutral': round(neutral_ratio, 3)
                    }
                }
            else:
                raise Exception(f"News API returned status code: {response.status_code} - {response.text}")

        except Exception as e:
            raise Exception(f"News API sentiment fetch error: {str(e)}")

    def _extract_keywords(self, text: str) -> List[str]:
        """
        Extract meaningful keywords from text (simple approach)
        """
        # Stop words to filter out
        stop_words = ['a', 'an', 'the', 'and', 'or', 'but', 'if', 'because', 'as', 'what',
                     'when', 'where', 'how', 'all', 'with', 'for', 'from', 'to', 'by', 'about',
                     'in', 'on', 'at', 'of', 'is', 'are', 'was', 'were', 'be', 'been', 'being',
                     'have', 'has', 'had', 'do', 'does', 'did', 'can', 'could', 'will', 'would',
                     'should', 'this', 'that', 'these', 'those', 'there', 'here', 'they', 'them',
                     'their', 'his', 'her', 'its', 'my', 'your', 'our']

        # Normalize text
        text = text.lower()

        # Remove special characters and digits
        import re
        text = re.sub(r'[^a-zA-Z\s]', ' ', text)

        # Split into words
        words = text.split()

        # Extract phrases (2-3 word combinations)
        phrases = []
        for i in range(len(words) - 1):
            # Two-word phrases
            if i < len(words) - 1 and words[i] not in stop_words and words[i+1] not in stop_words:
                phrases.append(f"{words[i]} {words[i+1]}")

            # Three-word phrases
            if i < len(words) - 2 and words[i] not in stop_words and words[i+2] not in stop_words:
                phrases.append(f"{words[i]} {words[i+1]} {words[i+2]}")

        # Filter out stop words and short words
        keywords = [word for word in words if word not in stop_words and len(word) > 3]

        # Combine keywords and phrases, limiting to top results
        all_terms = keywords + phrases

        # Count occurrences
        from collections import Counter
        term_counts = Counter(all_terms)

        # Get top terms
        common_terms = [term for term, count in term_counts.most_common(10) if count > 1]

        return common_terms if common_terms else all_terms[:5]

    def _categorize_keyword(self, keyword: str) -> str:
        """
        Categorize a keyword (simple approach)
        """
        # Define category keywords
        categories = {
            'Politics': ['government', 'president', 'election', 'vote', 'congress', 'senate', 'law', 'policy', 'political'],
            'Business': ['company', 'market', 'stock', 'economy', 'financial', 'trade', 'business', 'economic', 'industry'],
            'Technology': ['tech', 'technology', 'software', 'digital', 'internet', 'app', 'computer', 'online', 'device'],
            'Health': ['health', 'doctor', 'medical', 'covid', 'vaccine', 'disease', 'hospital', 'treatment', 'patient'],
            'Entertainment': ['film', 'movie', 'music', 'celebrity', 'actor', 'star', 'show', 'award', 'entertainment'],
            'Sports': ['game', 'team', 'player', 'season', 'league', 'championship', 'match', 'tournament', 'sport']
        }

        keyword_lower = keyword.lower()

        # Check each category
        for category, keywords in categories.items():
            if any(kw in keyword_lower for kw in keywords):
                return category

        # Default category
        return "News"
    
    def _create_cache_key(self, platform: str, data_type: str, topic: Optional[str], 
                         timeframe: str, location: str) -> str:
        """Create a unique cache key based on request parameters"""
        params_str = f"{platform}|{data_type}|{topic or 'any'}|{timeframe}|{location}"
        return f"social_{hashlib.md5(params_str.encode()).hexdigest()}"
    
    def _get_simulated_trends(self, platform: str, timeframe: str, location: str, 
                             topic: Optional[str] = None) -> Dict[str, Any]:
        """Get simulated trending topics data"""
        # Create seed based on parameters for consistency
        seed = f"{platform}_{timeframe}_{location}_{int(time.time() / 3600)}"
        random.seed(hash(seed) % 1000000)
        
        # Generate trending topics
        all_topics = self._generate_trending_topics(platform, location)
        
        # Filter by topic if specified
        if topic:
            filtered_topics = [t for t in all_topics if topic.lower() in t['topic'].lower()]
            trending_topics = filtered_topics[:min(len(filtered_topics), 10)]
        else:
            trending_topics = all_topics[:10]
        
        return {
            'platform': platform,
            'timestamp': datetime.now().isoformat(),
            'location': location,
            'timeframe': timeframe,
            'trending_topics': trending_topics
        }
    
    def _get_simulated_sentiment(self, platform: str, timeframe: str, location: str, 
                               topic: Optional[str] = None) -> Dict[str, Any]:
        """Get simulated sentiment analysis data"""
        # Use a specific topic or generate one
        if not topic:
            # Get first trending topic if no topic specified
            trending = self._generate_trending_topics(platform, location)
            topic = trending[0]['topic'] if trending else "general"
        
        # Create seed for consistent results
        seed = f"{platform}_{topic}_{timeframe}_{location}"
        random.seed(hash(seed) % 1000000)
        
        # Generate sentiment data over time
        sentiment_data = []
        end_time = datetime.now()
        
        # Determine time interval based on timeframe
        if timeframe == 'hour':
            intervals = 12
            delta = timedelta(minutes=5)
        elif timeframe == 'day':
            intervals = 24
            delta = timedelta(hours=1)
        elif timeframe == 'week':
            intervals = 7
            delta = timedelta(days=1)
        else:
            intervals = 24
            delta = timedelta(hours=1)
        
        # Base sentiment values (0-1 scale)
        base_positive = random.uniform(0.3, 0.7)
        base_negative = random.uniform(0.1, 0.4)
        base_neutral = 1 - base_positive - base_negative
        
        for i in range(intervals):
            point_time = end_time - delta * (intervals - i - 1)
            
            # Add some random variation
            variation = random.uniform(-0.1, 0.1)
            positive = max(0, min(1, base_positive + variation))
            
            variation = random.uniform(-0.1, 0.1)
            negative = max(0, min(1, base_negative + variation))
            
            # Ensure they sum to 1
            total = positive + negative
            if total > 1:
                positive = positive / total
                negative = negative / total
            
            neutral = 1 - positive - negative
            
            sentiment_data.append({
                'timestamp': point_time.isoformat(),
                'sentiment': {
                    'positive': round(positive, 3),
                    'negative': round(negative, 3),
                    'neutral': round(neutral, 3)
                },
                'volume': random.randint(100, 10000)
            })
        
        return {
            'platform': platform,
            'topic': topic,
            'timestamp': datetime.now().isoformat(),
            'location': location,
            'timeframe': timeframe,
            'sentiment_data': sentiment_data,
            'overall_sentiment': {
                'positive': round(base_positive, 3),
                'negative': round(base_negative, 3),
                'neutral': round(base_neutral, 3)
            }
        }
    
    def _get_simulated_engagement(self, platform: str, timeframe: str, location: str, 
                                topic: Optional[str] = None) -> Dict[str, Any]:
        """Get simulated engagement metrics data"""
        # Use a specific topic or generate one
        if not topic:
            # Get first trending topic if no topic specified
            trending = self._generate_trending_topics(platform, location)
            topic = trending[0]['topic'] if trending else "general"
        
        # Create seed for consistent results
        seed = f"{platform}_{topic}_{timeframe}_{location}_engagement"
        random.seed(hash(seed) % 1000000)
        
        # Generate engagement metrics
        engagement_metrics = {
            'likes': random.randint(1000, 1000000),
            'shares': random.randint(100, 100000),
            'comments': random.randint(50, 50000),
            'reach': random.randint(10000, 10000000),
            'engagement_rate': round(random.uniform(0.01, 0.15), 4)
        }
        
        # Generate engagement over time
        engagement_timeline = []
        end_time = datetime.now()
        
        # Determine time interval based on timeframe
        if timeframe == 'hour':
            intervals = 12
            delta = timedelta(minutes=5)
        elif timeframe == 'day':
            intervals = 24
            delta = timedelta(hours=1)
        elif timeframe == 'week':
            intervals = 7
            delta = timedelta(days=1)
        else:
            intervals = 24
            delta = timedelta(hours=1)
        
        # Base metrics
        base_likes = engagement_metrics['likes'] / intervals
        base_shares = engagement_metrics['shares'] / intervals
        base_comments = engagement_metrics['comments'] / intervals
        
        # Create a realistic timeline with a peak
        peak_point = random.randint(intervals // 3, 2 * intervals // 3)
        
        for i in range(intervals):
            point_time = end_time - delta * (intervals - i - 1)
            
            # Calculate multiplier based on distance from peak
            distance_from_peak = abs(i - peak_point)
            peak_multiplier = 2.0 * (1 - min(1, distance_from_peak / (intervals / 2)))
            
            # Add some random noise
            noise = random.uniform(0.7, 1.3)
            multiplier = peak_multiplier * noise
            
            engagement_timeline.append({
                'timestamp': point_time.isoformat(),
                'likes': int(base_likes * multiplier),
                'shares': int(base_shares * multiplier),
                'comments': int(base_comments * multiplier)
            })
        
        return {
            'platform': platform,
            'topic': topic,
            'timestamp': datetime.now().isoformat(),
            'location': location,
            'timeframe': timeframe,
            'engagement_metrics': engagement_metrics,
            'engagement_timeline': engagement_timeline,
            'demographics': self._generate_demographics(platform)
        }
    
    def _generate_trending_topics(self, platform: str, location: str) -> List[Dict[str, Any]]:
        """Generate simulated trending topics"""
        # Create seed for consistent results
        seed = f"{platform}_{location}_{int(time.time() / 3600)}"
        random.seed(hash(seed) % 1000000)
        
        # Topic categories for different platforms
        categories = {
            'twitter': ['Politics', 'Entertainment', 'Sports', 'Technology', 'Health'],
            'facebook': ['Entertainment', 'News', 'Community', 'Business', 'Lifestyle'],
            'instagram': ['Lifestyle', 'Fashion', 'Travel', 'Food', 'Fitness'],
            'tiktok': ['Challenges', 'Music', 'Comedy', 'Dance', 'Education'],
            'linkedin': ['Business', 'Careers', 'Technology', 'Leadership', 'Education']
        }
        
        # Get categories for this platform or use generic ones
        platform_categories = categories.get(platform.lower(), 
                                          ['Entertainment', 'Politics', 'Sports', 'Technology', 'Lifestyle'])
        
        # Common trending topic patterns
        topic_patterns = [
            "#Trending{0}",
            "The Latest {0} News",
            "{0} Update",
            "Breaking: {0}",
            "Why Everyone is Talking About {0}",
            "{0} Challenge",
            "{0} Controversy"
        ]
        
        # Generate topics
        trending_topics = []
        for i in range(20):  # Generate 20 topics
            # Select category and topic pattern
            category = random.choice(platform_categories)
            pattern = random.choice(topic_patterns)
            
            # Generate topic based on pattern and category
            if "{0}" in pattern:
                topic = pattern.format(self._generate_topic_for_category(category))
            else:
                topic = pattern
            
            # Calculate volume and growth rate
            volume = random.randint(1000, 100000)
            growth_rate = round(random.uniform(-20, 100), 1)  # Percentage
            
            trending_topics.append({
                'topic': topic,
                'category': category,
                'volume': volume,
                'growth_rate': growth_rate,
                'rank': i + 1
            })
        
        # Sort by volume (higher volume = higher trending)
        trending_topics.sort(key=lambda x: x['volume'], reverse=True)
        
        # Update rank after sorting
        for i, topic in enumerate(trending_topics):
            topic['rank'] = i + 1
        
        return trending_topics
    
    def _generate_topic_for_category(self, category: str) -> str:
        """Generate a plausible topic name for a given category"""
        # Define topics for each category
        category_topics = {
            'Politics': ['Election', 'Legislation', 'President', 'Congress', 'Democracy', 
                      'Voting', 'Senator', 'Government', 'Policy', 'Debate'],
            'Entertainment': ['Movie', 'Celebrity', 'TV Show', 'Music', 'Album', 
                           'Concert', 'Awards', 'Netflix', 'Hollywood', 'Actor'],
            'Sports': ['Tournament', 'Championship', 'Football', 'Basketball', 'Soccer', 
                    'Olympics', 'Tennis', 'Baseball', 'Team', 'Player'],
            'Technology': ['Apple', 'Google', 'Microsoft', 'AI', 'Innovation', 
                        'Smartphone', 'App', 'Software', 'Hardware', 'Tech'],
            'Health': ['Wellness', 'Fitness', 'Nutrition', 'Pandemic', 'Medicine', 
                    'Healthcare', 'Mental Health', 'Vaccine', 'Research', 'Therapy'],
            'News': ['Breaking News', 'World News', 'Headlines', 'Current Events', 'Report', 
                  'Crisis', 'Investigation', 'Update', 'Story', 'Analysis'],
            'Business': ['Startup', 'Investment', 'Market', 'Economy', 'Company', 
                     'Finance', 'Industry', 'CEO', 'Earnings', 'Strategy'],
            'Lifestyle': ['Fashion', 'Travel', 'Food', 'Home', 'Design', 
                       'Style', 'Beauty', 'Culture', 'Trends', 'Luxury'],
            'Community': ['Local', 'Neighborhood', 'Charity', 'Event', 'Support', 
                       'Fundraiser', 'Initiative', 'Volunteer', 'Cause', 'Together'],
            'Fashion': ['Designer', 'Collection', 'Style', 'Runway', 'Trend', 
                     'Brand', 'Model', 'Clothing', 'Accessories', 'Look'],
            'Travel': ['Destination', 'Vacation', 'Adventure', 'Tourism', 'Journey', 
                    'Explore', 'Trip', 'Resort', 'Hotel', 'Sightseeing'],
            'Food': ['Recipe', 'Restaurant', 'Cooking', 'Chef', 'Cuisine', 
                  'Dish', 'Foodie', 'Meal', 'Dining', 'Flavor'],
            'Fitness': ['Workout', 'Exercise', 'Training', 'Gym', 'Diet', 
                     'Routine', 'Body', 'Health', 'Muscles', 'Athletics'],
            'Challenges': ['Viral', 'Dance', 'Stunt', 'Talent', 'Skills', 
                        'Competition', 'Trending', 'Popular', 'Fun', 'Creative'],
            'Music': ['Song', 'Artist', 'Album', 'Release', 'Singer', 
                   'Band', 'Concert', 'Performance', 'Genre', 'Lyrics'],
            'Comedy': ['Humor', 'Sketch', 'Joke', 'Funny', 'Comic', 
                    'Parody', 'Satire', 'Prank', 'Laugh', 'Stand-up'],
            'Dance': ['Choreography', 'Routine', 'Move', 'Performance', 'Dancer', 
                   'Style', 'Tutorial', 'Trending', 'Steps', 'Music'],
            'Education': ['Learning', 'School', 'University', 'Study', 'Course', 
                       'Knowledge', 'Skills', 'Teaching', 'Research', 'Academic'],
            'Leadership': ['Management', 'Executive', 'Strategy', 'Team', 'Vision', 
                        'Innovation', 'Success', 'Influence', 'Growth', 'Leadership']
        }
        
        # Get topics for this category or use generic ones
        topics = category_topics.get(category, ['Trending', 'Popular', 'Viral', 'Latest', 'Hot'])
        
        # Select a random topic
        return random.choice(topics)
    
    def _generate_demographics(self, platform: str) -> Dict[str, Any]:
        """Generate simulated demographic data for engagement"""
        # Create typical age distribution based on platform
        if platform.lower() == 'tiktok':
            age_distribution = {
                '13-17': round(random.uniform(0.25, 0.35), 2),
                '18-24': round(random.uniform(0.30, 0.40), 2),
                '25-34': round(random.uniform(0.15, 0.25), 2),
                '35-44': round(random.uniform(0.05, 0.15), 2),
                '45+': round(random.uniform(0.01, 0.05), 2)
            }
        elif platform.lower() == 'instagram':
            age_distribution = {
                '13-17': round(random.uniform(0.15, 0.25), 2),
                '18-24': round(random.uniform(0.25, 0.35), 2),
                '25-34': round(random.uniform(0.20, 0.30), 2),
                '35-44': round(random.uniform(0.10, 0.20), 2),
                '45+': round(random.uniform(0.05, 0.15), 2)
            }
        elif platform.lower() == 'facebook':
            age_distribution = {
                '13-17': round(random.uniform(0.05, 0.10), 2),
                '18-24': round(random.uniform(0.15, 0.20), 2),
                '25-34': round(random.uniform(0.20, 0.25), 2),
                '35-44': round(random.uniform(0.20, 0.25), 2),
                '45+': round(random.uniform(0.25, 0.35), 2)
            }
        elif platform.lower() == 'linkedin':
            age_distribution = {
                '13-17': round(random.uniform(0.00, 0.01), 2),
                '18-24': round(random.uniform(0.10, 0.15), 2),
                '25-34': round(random.uniform(0.30, 0.40), 2),
                '35-44': round(random.uniform(0.25, 0.35), 2),
                '45+': round(random.uniform(0.15, 0.25), 2)
            }
        else:  # Default/Twitter
            age_distribution = {
                '13-17': round(random.uniform(0.10, 0.15), 2),
                '18-24': round(random.uniform(0.20, 0.30), 2),
                '25-34': round(random.uniform(0.25, 0.35), 2),
                '35-44': round(random.uniform(0.15, 0.25), 2),
                '45+': round(random.uniform(0.05, 0.15), 2)
            }
        
        # Normalize age distribution to sum to 1
        total = sum(age_distribution.values())
        for age in age_distribution:
            age_distribution[age] = round(age_distribution[age] / total, 2)
        
        # Create gender distribution
        gender_distribution = {
            'male': round(random.uniform(0.35, 0.65), 2),
            'female': round(random.uniform(0.35, 0.65), 2),
            'other': round(random.uniform(0.01, 0.05), 2)
        }
        
        # Normalize gender distribution to sum to 1
        total = sum(gender_distribution.values())
        for gender in gender_distribution:
            gender_distribution[gender] = round(gender_distribution[gender] / total, 2)
        
        return {
            'age_distribution': age_distribution,
            'gender_distribution': gender_distribution,
            'top_locations': self._generate_top_locations(),
            'device_distribution': self._generate_device_distribution(platform)
        }
    
    def _generate_top_locations(self) -> List[Dict[str, Any]]:
        """Generate top locations for audience"""
        locations = [
            {'name': 'United States', 'code': 'US'},
            {'name': 'United Kingdom', 'code': 'UK'},
            {'name': 'Canada', 'code': 'CA'},
            {'name': 'Australia', 'code': 'AU'},
            {'name': 'Germany', 'code': 'DE'},
            {'name': 'France', 'code': 'FR'},
            {'name': 'Japan', 'code': 'JP'},
            {'name': 'Brazil', 'code': 'BR'},
            {'name': 'India', 'code': 'IN'},
            {'name': 'Mexico', 'code': 'MX'}
        ]
        
        # Shuffle and select 5 random locations
        random.shuffle(locations)
        selected = locations[:5]
        
        # Assign percentages
        total = 0
        for location in selected:
            percentage = round(random.uniform(5, 30), 1)
            location['percentage'] = percentage
            total += percentage
        
        # Normalize to make total 100%
        for location in selected:
            location['percentage'] = round(location['percentage'] * 100 / total, 1)
        
        # Sort by percentage
        selected.sort(key=lambda x: x['percentage'], reverse=True)
        
        return selected
    
    def _generate_device_distribution(self, platform: str) -> Dict[str, float]:
        """Generate device usage distribution"""
        # Default distribution
        distribution = {
            'mobile': round(random.uniform(0.60, 0.80), 2),
            'desktop': round(random.uniform(0.10, 0.30), 2),
            'tablet': round(random.uniform(0.05, 0.15), 2)
        }
        
        # Adjust based on platform
        if platform.lower() in ['instagram', 'tiktok']:
            # More mobile focused
            distribution['mobile'] = round(random.uniform(0.80, 0.90), 2)
            distribution['desktop'] = round(random.uniform(0.05, 0.15), 2)
            distribution['tablet'] = round(random.uniform(0.03, 0.10), 2)
        elif platform.lower() in ['linkedin', 'facebook']:
            # More desktop usage
            distribution['mobile'] = round(random.uniform(0.50, 0.70), 2)
            distribution['desktop'] = round(random.uniform(0.20, 0.40), 2)
            distribution['tablet'] = round(random.uniform(0.05, 0.15), 2)
        
        # Normalize to sum to 1
        total = sum(distribution.values())
        for device in distribution:
            distribution[device] = round(distribution[device] / total, 2)
        
        return distribution