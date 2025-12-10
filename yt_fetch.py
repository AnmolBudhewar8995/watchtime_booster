
# src/yt_fetch.py
import pandas as pd
from src.yt_auth import build_youtube_clients
import math
from datetime import datetime

def fetch_videos(channel_id=None, max_results=50):
    youtube, analytics = build_youtube_clients()
    # If channel_id None, fetch for the authorized user's channel
    if channel_id is None:
        resp = youtube.channels().list(part="contentDetails", mine=True).execute()
        uploads_id = resp["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]
        # get videos from the uploads playlist
        playlist = youtube.playlistItems().list(playlistId=uploads_id, part="contentDetails", maxResults=50).execute()
        items = playlist.get("items", [])
        video_ids = [it["contentDetails"]["videoId"] for it in items]
    else:
        # list videos by search
        resp = youtube.search().list(part="id", channelId=channel_id, maxResults=max_results, type="video").execute()
        video_ids = [it["id"]["videoId"] for it in resp.get("items",[])]
    # fetch stats
    stats = []
    for i in range(0, len(video_ids), 50):
        chunk = video_ids[i:i+50]
        r = youtube.videos().list(part="snippet,statistics,contentDetails", id=",".join(chunk)).execute()
        for v in r.get("items", []):
            sid = v["id"]
            snip = v["snippet"]
            stat = v.get("statistics", {})
            # contentDetails may include duration ISO8601 — parse to seconds
            dur = v.get("contentDetails", {}).get("duration")
            # parse ISO 8601 duration simple helper:
            duration_seconds = parse_iso8601_duration(dur) if dur else None
            stats.append({
                "video_id": sid,
                "title": snip.get("title"),
                "publishedAt": snip.get("publishedAt"),
                "views": int(stat.get("viewCount",0)),
                "likes": int(stat.get("likeCount",0)) if "likeCount" in stat else None,
                "comments": int(stat.get("commentCount",0)) if "commentCount" in stat else None,
                "duration_s": duration_seconds
            })
    df = pd.DataFrame(stats)
    return df

def fetch_video_by_url(video_id):
    """Fetch detailed information for a single video by ID"""
    youtube, analytics = build_youtube_clients()
    
    # Fetch video details
    r = youtube.videos().list(
        part="snippet,statistics,contentDetails",
        id=video_id
    ).execute()
    
    if not r.get("items"):
        raise ValueError(f"Video with ID {video_id} not found")
    
    v = r["items"][0]
    snip = v["snippet"]
    stat = v.get("statistics", {})
    content_details = v.get("contentDetails", {})
    
    # Parse duration
    duration_iso = content_details.get("duration")
    duration_seconds = parse_iso8601_duration(duration_iso) if duration_iso else 0
    duration_formatted = format_duration(duration_seconds)
    
    # Format published date
    published_at = snip.get("publishedAt", "")
    if published_at:
        try:
            pub_date = datetime.fromisoformat(published_at.replace('Z', '+00:00'))
            published_formatted = pub_date.strftime("%B %d, %Y")
        except:
            published_formatted = published_at
    else:
        published_formatted = "Unknown"
    
    # Get video ID from various URL formats (for display)
    video_url = f"https://www.youtube.com/watch?v={video_id}"
    
    # Extract thumbnail URL (high quality)
    thumbnails = snip.get("thumbnails", {})
    thumbnail_url = thumbnails.get("high", {}).get("url") or thumbnails.get("medium", {}).get("url") or thumbnails.get("default", {}).get("url", "")
    
    video_data = {
        "video_id": video_id,
        "title": snip.get("title", "Unknown Title"),
        "description": snip.get("description", ""),
        "channel_title": snip.get("channelTitle", "Unknown Channel"),
        "published_at": published_formatted,
        "published_at_raw": published_at,
        "views": int(stat.get("viewCount", 0)),
        "likes": int(stat.get("likeCount", 0)) if "likeCount" in stat else 0,
        "dislikes": int(stat.get("dislikeCount", 0)) if "dislikeCount" in stat else 0,
        "comments": int(stat.get("commentCount", 0)) if "commentCount" in stat else 0,
        "duration_s": duration_seconds,
        "duration_iso": duration_iso,
        "duration_formatted": duration_formatted,
        "thumbnail_url": thumbnail_url,
        "video_url": video_url,
        "tags": snip.get("tags", []),
        "category_id": snip.get("categoryId", ""),
        "default_language": snip.get("defaultLanguage", ""),
        "default_audio_language": snip.get("defaultAudioLanguage", "")
    }
    
    return video_data

def format_duration(seconds):
    """Format duration in seconds to human readable format"""
    if not seconds or seconds == 0:
        return "0:00"
    
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    secs = seconds % 60
    
    if hours > 0:
        return f"{hours}:{minutes:02d}:{secs:02d}"
    else:
        return f"{minutes}:{secs:02d}"

def parse_iso8601_duration(d):
    # simple parser for PT#M#S or PT#H#M#S
    if not d: return None
    import isodate
    try:
        td = isodate.parse_duration(d)
        return int(td.total_seconds())
    except:
        return None
