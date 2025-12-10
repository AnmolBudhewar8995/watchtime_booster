
# src/recommender.py
from sentence_transformers import SentenceTransformer
from sklearn.cluster import AgglomerativeClustering
import numpy as np
import pandas as pd
import re
from datetime import datetime, timedelta

embed_model = SentenceTransformer("all-MiniLM-L6-v2")

def cluster_videos(df, n_clusters=8):
    texts = (df['title'].fillna("") + " " + df.get('description', pd.Series([""]*len(df)))).tolist()
    embs = embed_model.encode(texts, convert_to_numpy=True)
    # simple clustering
    n_clusters = min(n_clusters, len(df))
    cl = AgglomerativeClustering(n_clusters=n_clusters).fit(embs)
    df['cluster'] = cl.labels_
    return df

def suggest_playlists(df, topk_per_cluster=5):
    playlists = {}
    for c in df['cluster'].unique():
        top = df[df['cluster']==c].sort_values("views", ascending=False).head(topk_per_cluster)
        playlists[f"cluster_{c}"] = top['video_id'].tolist()
    return playlists

def get_optimization_suggestions(video_data, analysis_data):
    """
    Generate advanced optimization suggestions for a single video
    Combines content analysis with best practices for watch time optimization
    """
    suggestions = {
        'content_strategy': [],
        'technical_optimization': [],
        'engagement_tactics': [],
        'competitive_insights': [],
        'posting_strategy': []
    }
    
    # Content Strategy Suggestions
    suggestions['content_strategy'] = generate_content_strategy_suggestions(video_data)
    
    # Technical Optimization
    suggestions['technical_optimization'] = generate_technical_suggestions(video_data)
    
    # Engagement Tactics
    suggestions['engagement_tactics'] = generate_engagement_tactics(video_data, analysis_data)
    
    # Competitive Insights
    suggestions['competitive_insights'] = generate_competitive_insights(video_data)
    
    # Posting Strategy
    suggestions['posting_strategy'] = generate_posting_strategy_suggestions(video_data)
    
    return suggestions

def generate_content_strategy_suggestions(video_data):
    """Generate content-related optimization suggestions"""
    suggestions = []
    
    title = video_data.get('title', '')
    description = video_data.get('description', '')
    duration = video_data.get('duration_s', 0)
    tags = video_data.get('tags', [])
    
    # Title optimization
    if not any(keyword in title.lower() for keyword in ['how to', 'tutorial', 'guide', 'tips', 'review']):
        suggestions.append("Consider adding action-oriented keywords like 'How to', 'Tutorial', 'Tips', or 'Guide' to improve searchability.")
    
    if len(title.split()) < 5:
        suggestions.append("Your title could be more descriptive. Add specific details about what viewers will learn or gain.")
    

    # Description analysis
    if len(description) < 100:
        suggestions.append("Your video description is quite short. YouTube descriptions should be 150-300 words for better SEO.")
        suggestions.append("Add timestamps, key points, and relevant keywords to your description.")
    
    # Tags analysis
    if len(tags) < 5:
        suggestions.append("Consider adding more relevant tags (10-15 tags) to improve discoverability across different search queries.")
    
    # Duration-specific content suggestions
    if duration < 300:  # Under 5 minutes
        suggestions.append("For short videos, focus on one specific value proposition. Deliver it quickly and clearly.")
    elif duration > 1200:  # Over 20 minutes
        suggestions.append("Long-form content works well if it maintains engagement. Consider breaking into chapters or series.")
    
    return suggestions

def generate_technical_suggestions(video_data):
    """Generate technical and production optimization suggestions"""
    suggestions = []
    
    duration = video_data.get('duration_s', 0)
    views = video_data.get('views', 0)
    published_at = video_data.get('published_at_raw', '')
    
    # Audio/Visual quality indicators
    if views < 1000:
        suggestions.append("Focus on improving audio quality first - it's often more important than video quality for retention.")
        suggestions.append("Ensure good lighting and clear visuals, especially in the first 15 seconds.")
    
    # Engagement timing
    if duration > 600:  # Videos longer than 10 minutes
        suggestions.append("Add pattern interrupts every 2-3 minutes: graphics, questions, or topic changes to maintain attention.")
        suggestions.append("Include visual cues and on-screen text to help viewers follow along.")
    
    # Upload timing analysis
    if published_at:
        try:
            pub_date = datetime.fromisoformat(published_at.replace('Z', '+00:00'))
            day_of_week = pub_date.weekday()
            hour = pub_date.hour
            
            if day_of_week in [5, 6]:  # Weekend
                suggestions.append("Consider testing weekday uploads as well - many channels perform better Tuesday-Thursday.")
            
            if 0 <= hour <= 6 or hour >= 22:  # Very early or late
                suggestions.append("Your upload time might not be optimal. Test posting during peak hours for your audience.")
        except:
            pass
    
    return suggestions

def generate_engagement_tactics(video_data, analysis_data):
    """Generate engagement and retention optimization suggestions"""
    suggestions = []
    
    engagement_rate = analysis_data.get('engagement_rate', 0) if analysis_data else 0
    duration = video_data.get('duration_s', 0)
    views = video_data.get('views', 0)
    
    # Hook optimization
    if duration > 300:  # Videos longer than 5 minutes
        suggestions.append("Strengthen your opening hook. The first 15 seconds determine if viewers stay or leave.")
        suggestions.append("Promise specific value in the first 30 seconds: 'By the end of this video, you'll know exactly how to...'")
    
    # Call-to-action optimization
    if views > 1000:
        suggestions.append("Add mid-video call-to-actions: 'If this is helpful, hit the like button' to boost engagement signals.")
        suggestions.append("Ask specific questions in the comments to encourage discussion.")
    
    # Engagement rate based suggestions
    if engagement_rate < 2:  # Less than 2%
        suggestions.append("Low engagement detected. Try adding more interactive elements: polls, questions, or challenges.")
        suggestions.append("Create controversy or debate to encourage comments (while staying within YouTube guidelines).")
    elif engagement_rate > 5:  # High engagement
        suggestions.append("Great engagement! Consider creating follow-up content based on viewer feedback and questions.")
    
    return suggestions

def generate_competitive_insights(video_data):
    """Generate competitive analysis and market positioning suggestions"""
    suggestions = []
    
    title = video_data.get('title', '')
    category_id = video_data.get('category_id', '')
    
    # Category-based insights
    category_suggestions = {
        '1': "Film & Animation: Focus on trending topics and seasonal content for better discoverability.",
        '2': "Autos & Vehicles: Create comparison videos and 'vs' content for high engagement.",
        '10': "Music: Consider lyric videos, covers, or music production tutorials.",
        '15': "Pets & Animals: Create heartwarming or funny compilations with storytelling elements.",
        '17': "Sports: Focus on highlights, analysis, and prediction content.",
        '19': "Travel & Events: Use location-based keywords and seasonal content strategies.",
        '20': "Gaming: Stream highlights, create tutorials, or review new games.",
        '22': "People & Blogs: Focus on storytelling and personal experiences.",
        '23': "Comedy: Create trending comedy formats and collaborate with other creators.",
        '24': "Entertainment: Stay current with pop culture and entertainment news.",
        '25': "News & Politics: Focus on timely, accurate reporting with clear sources.",
        '26': "Howto & Style: Create step-by-step tutorials and before/after content.",
        '27': "Education: Use clear explanations with visual aids and examples.",
        '28': "Science & Technology: Focus on explaining complex topics in simple terms."
    }
    
    if category_id in category_suggestions:
        suggestions.append(category_suggestions[category_id])
    
    # General competitive insights
    suggestions.append("Research top-performing videos in your niche and analyze their structure and hooks.")
    suggestions.append("Consider collaborating with creators in your field to cross-promote and gain new audiences.")
    
    return suggestions

def generate_posting_strategy_suggestions(video_data):
    """Generate posting schedule and promotional strategy suggestions"""
    suggestions = []
    
    published_at = video_data.get('published_at_raw', '')
    views = video_data.get('views', 0)
    
    # Upload frequency suggestions
    if views < 500:
        suggestions.append("Focus on consistency over frequency. Upload regularly (weekly or bi-weekly) to build audience expectation.")
        suggestions.append("Promote your videos on social media platforms to drive initial views.")
    
    # Cross-platform promotion
    suggestions.append("Share your video on relevant Reddit communities, Facebook groups, and Discord servers.")
    suggestions.append("Create short clips or teasers for TikTok/Instagram Reels to drive traffic to the full video.")
    
    # Community building
    if views > 1000:
        suggestions.append("Respond to comments within the first few hours to boost engagement and algorithmic performance.")
        suggestions.append("Create community posts to keep your audience engaged between video uploads.")
    
    # SEO optimization
    suggestions.append("Use YouTube's search suggestions to optimize your title and description for better discoverability.")
    suggestions.append("Create custom thumbnails that create curiosity gaps - show something that makes people want to click.")
    
    return suggestions
