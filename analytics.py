
# src/analytics.py
import pandas as pd
import numpy as np
from datetime import datetime

def compute_potential(df):
    """
    df must contain: video_id, views, duration_s, avg_view_duration (if fetched), impressions, ctr, watchTime
    We compute 'lost watch potential' heuristically:
      potential = impressions * avgViewDurationGap (or views * (duration - avg_view_duration))
    """
    df = df.copy()
    if "avgViewDuration" in df.columns:
        df["avgViewDuration"] = pd.to_numeric(df["avgViewDuration"], errors="coerce")
        df["duration_s"] = pd.to_numeric(df["duration_s"], errors="coerce")
        # how much more view seconds if viewers watched extra X seconds?
        df["potential_seconds_per_view"] = (df["duration_s"] - df["avgViewDuration"]).clip(lower=0)
        df["potential_watch_seconds"] = df["views"] * df["potential_seconds_per_view"]
        df = df.sort_values("potential_watch_seconds", ascending=False)
    else:
        # fallback: target videos with high views but low duration
        df["potential_score"] = df["views"] / (df["duration_s"].clip(lower=1))
        df = df.sort_values("potential_score", ascending=False)
    return df

def analyze_single_video(video_data):
    """
    Analyze a single video for watch time optimization potential
    Returns comprehensive analysis with suggestions and action items
    """
    # Extract key metrics
    duration = video_data.get('duration_s', 0)
    views = video_data.get('views', 0)
    likes = video_data.get('likes', 0)
    comments = video_data.get('comments', 0)
    title = video_data.get('title', '')
    tags = video_data.get('tags', [])
    
    # Calculate engagement metrics
    engagement_rate = (likes + comments) / max(views, 1) if views > 0 else 0
    
    # Estimate average watch time (YouTube typically shows ~40-60% retention)
    # This is a rough estimate - actual data would require YouTube Analytics API
    estimated_avg_watch_time = duration * 0.5  # Assume 50% average retention
    
    # Calculate current watch time
    current_watch_time = views * estimated_avg_watch_time
    
    # Calculate optimization potential
    potential_improvement = views * (duration * 0.1)  # 10% improvement potential
    
    # Calculate optimization score (0-100)
    optimization_score = calculate_optimization_score(video_data, engagement_rate)
    
    # Generate suggestions based on video characteristics
    suggestions = generate_suggestions(video_data, engagement_rate, duration, views)
    
    # Generate action items
    action_items = generate_action_items(video_data, optimization_score, suggestions)
    
    analysis = {
        'current_watch_time': int(current_watch_time),
        'estimated_avg_watch_time': int(estimated_avg_watch_time),
        'potential_improvement': int(potential_improvement),
        'optimization_score': optimization_score,
        'engagement_rate': round(engagement_rate * 100, 2),  # as percentage
        'suggestions': suggestions,
        'action_items': action_items,
        'video_metrics': {
            'duration': duration,
            'views': views,
            'likes': likes,
            'comments': comments,
            'like_to_view_ratio': round(likes / max(views, 1) * 100, 2) if views > 0 else 0,
            'comment_to_view_ratio': round(comments / max(views, 1) * 100, 2) if views > 0 else 0
        }
    }
    
    return analysis

def calculate_optimization_score(video_data, engagement_rate):
    """Calculate an optimization score from 0-100 based on various factors"""
    score = 50  # Base score
    
    duration = video_data.get('duration_s', 0)
    views = video_data.get('views', 0)
    likes = video_data.get('likes', 0)
    comments = video_data.get('comments', 0)
    title = video_data.get('title', '')
    
    # Duration optimization (sweet spot is 8-15 minutes for many channels)
    if duration < 120:  # Less than 2 minutes
        score -= 10
    elif 480 <= duration <= 900:  # 8-15 minutes
        score += 10
    elif duration > 1800:  # More than 30 minutes
        score -= 15
    
    # Engagement score
    if engagement_rate > 0.05:  # 5% engagement rate
        score += 15
    elif engagement_rate > 0.02:  # 2% engagement rate
        score += 5
    elif engagement_rate < 0.005:  # 0.5% engagement rate
        score -= 20
    
    # Title analysis
    if len(title) > 60:  # Title too long
        score -= 5
    elif len(title) < 30:  # Title too short
        score -= 5
    
    # View count factor (more views usually means better optimization)
    if views > 100000:  # 100K+ views
        score += 10
    elif views > 10000:  # 10K+ views
        score += 5
    elif views < 1000:  # Less than 1K views
        score -= 10
    
    return max(0, min(100, score))

def generate_suggestions(video_data, engagement_rate, duration, views):
    """Generate specific optimization suggestions for the video"""
    suggestions = []
    
    # Duration-based suggestions
    if duration < 120:
        suggestions.append("Consider making longer, more detailed content. Videos under 2 minutes often have lower watch time retention.")
    elif duration > 1800:
        suggestions.append("Your video is quite long (30+ minutes). Consider breaking it into a series or adding chapter markers to improve retention.")
    elif duration < 300:
        suggestions.append("Short videos (under 5 minutes) can perform well if they're engaging. Focus on delivering value quickly.")
    else:
        suggestions.append("Your video length is in a good range. Focus on maintaining viewer engagement throughout.")
    
    # Engagement-based suggestions
    if engagement_rate < 0.01:
        suggestions.append("Low engagement detected. Consider improving your hook in the first 15 seconds to capture attention immediately.")
    elif engagement_rate > 0.05:
        suggestions.append("Great engagement rate! Your content resonates well with viewers.")
    
    # Title and description suggestions
    title = video_data.get('title', '')
    if len(title) > 60:
        suggestions.append("Your title is quite long. Consider making it more concise while keeping key keywords (under 60 characters).")
    elif len(title) < 20:
        suggestions.append("Your title might be too short. Consider adding more descriptive keywords to improve discoverability.")
    
    # Content structure suggestions
    if duration > 600:  # Videos longer than 10 minutes
        suggestions.append("Add chapter markers or timestamps to help viewers navigate to specific sections they're interested in.")
        suggestions.append("Consider adding pattern interrupts every 2-3 minutes to maintain attention.")
    
    # Call-to-action suggestions
    if views < 1000:
        suggestions.append("Focus on building audience retention. Ask questions or create curiosity gaps to encourage continued viewing.")
    
    # Technical suggestions
    suggestions.append("Ensure your thumbnail and title work together to create a compelling promise that the video delivers on.")
    
    return suggestions

def generate_action_items(video_data, optimization_score, suggestions):
    """Generate actionable items based on analysis"""
    action_items = []
    
    if optimization_score < 30:
        action_items.append("🔴 High Priority: Major optimization needed. Focus on improving retention in the first 30 seconds.")
        action_items.append("🔴 High Priority: Review your title and thumbnail for clarity and appeal.")
    elif optimization_score < 60:
        action_items.append("🟡 Medium Priority: Moderate optimization opportunities. Focus on engagement improvements.")
    else:
        action_items.append("🟢 Good: Your video is well-optimized. Focus on maintaining current strategies.")
    
    # Specific action items based on suggestions
    duration = video_data.get('duration_s', 0)
    if duration < 120:
        action_items.append("📈 Test longer format content (8-15 minutes) to increase watch time potential.")
    elif duration > 1800:
        action_items.append("✂️ Consider creating a condensed version or adding chapter markers.")
    
    engagement_rate = (video_data.get('likes', 0) + video_data.get('comments', 0)) / max(video_data.get('views', 1), 1)
    if engagement_rate < 0.02:
        action_items.append("💬 Add more interactive elements: questions, polls, or calls-to-action to boost engagement.")
    
    action_items.append("📊 Monitor audience retention graphs in YouTube Analytics to identify drop-off points.")
    action_items.append("🎯 A/B test different thumbnails for future videos based on what works best.")
    
    return action_items
