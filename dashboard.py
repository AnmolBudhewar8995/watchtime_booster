

# src/dashboard.py
import streamlit as st
from src.yt_fetch import fetch_video_by_url
from src.analytics import analyze_single_video
from src.recommender import get_optimization_suggestions
import re

st.title("Watch-Time Booster Dashboard")
st.info("Analyze and optimize watch time for individual YouTube videos.")

# Initialize session state
if 'video_data' not in st.session_state:
    st.session_state['video_data'] = None

if 'analysis' not in st.session_state:
    st.session_state['analysis'] = None

# Function to extract video ID from URL
def extract_video_id(url):
    """Extract video ID from various YouTube URL formats"""
    patterns = [
        r'(?:youtube\.com/watch\?v=|youtu\.be/|youtube\.com/embed/)([^&\n?#]+)',
        r'youtube\.com/v/([^&\n?#]+)',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None

# Main input section
st.header("🎥 Enter YouTube Video URL")
url = st.text_input(
    "Paste your YouTube video URL here:",
    placeholder="https://www.youtube.com/watch?v=dQw4w9WgXcQ",
    help="Supports all YouTube URL formats: youtube.com, youtu.be, embed links"
)

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    analyze_button = st.button("🚀 Analyze Video", type="primary", use_container_width=True)

# Analyze button logic
if analyze_button and url:
    video_id = extract_video_id(url)
    
    if not video_id:
        st.error("❌ Invalid YouTube URL. Please check the URL format.")
    else:
        try:
            with st.spinner("🔍 Fetching video data and analyzing watch time potential..."):
                # Fetch video data
                video_data = fetch_video_by_url(video_id)
                st.session_state['video_data'] = video_data
                
                # Perform analysis
                analysis = analyze_single_video(video_data)
                st.session_state['analysis'] = analysis
                
                st.success("✅ Analysis complete!")
                st.rerun()
                
        except Exception as e:
            st.error(f"❌ Error analyzing video: {str(e)}")
            st.info("Please ensure you have set up your YouTube API credentials properly in client_secrets.json")

# Display results if available
if st.session_state['video_data'] is not None:
    video_data = st.session_state['video_data']
    
    st.header("📊 Video Information")
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown(f"**Title:** {video_data.get('title', 'N/A')}")
        st.markdown(f"**Channel:** {video_data.get('channel_title', 'N/A')}")
        st.markdown(f"**Duration:** {video_data.get('duration_formatted', 'N/A')}")
        st.markdown(f"**Published:** {video_data.get('published_at', 'N/A')}")
    
    with col2:
        st.metric("Views", f"{video_data.get('views', 0):,}")
        st.metric("Likes", f"{video_data.get('likes', 0):,}")
        st.metric("Duration (sec)", video_data.get('duration_s', 0))
    
    # Video thumbnail
    if video_data.get('thumbnail_url'):
        st.image(video_data['thumbnail_url'], width=400)
    
    st.header("⏱️ Watch Time Analysis")
    if st.session_state['analysis'] is not None:
        analysis = st.session_state['analysis']
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Current Watch Time", f"{analysis.get('current_watch_time', 0):,} seconds")
        with col2:
            st.metric("Potential Improvement", f"+{analysis.get('potential_improvement', 0):,} seconds")
        with col3:
            st.metric("Optimization Score", f"{analysis.get('optimization_score', 0)}/100")
        
        st.header("💡 Optimization Suggestions")
        suggestions = analysis.get('suggestions', [])
        if suggestions:
            for i, suggestion in enumerate(suggestions, 1):
                st.markdown(f"{i}. {suggestion}")
        else:
            st.info("No specific suggestions available for this video.")
        
        st.header("🎯 Action Items")
        action_items = analysis.get('action_items', [])
        if action_items:
            for item in action_items:
                st.markdown(f"• {item}")
        else:
            st.info("Video is well optimized for watch time.")
    
    # Clear session state button
    if st.button("🔄 Analyze Another Video"):
        st.session_state['video_data'] = None
        st.session_state['analysis'] = None
        st.rerun()

# Sidebar with tips
with st.sidebar:
    st.header("💡 Tips for Better Watch Time")
    st.markdown("""
    **Key Factors:**
    • Strong opening hook (first 15 seconds)
    • Clear value proposition
    • Consistent pacing
    • Engaging thumbnails
    • Strategic end screens
    • Audience retention optimization
    """)
    
    st.markdown("---")
    st.header("🔧 Setup Instructions")
    st.markdown("""
    1. **Create YouTube API Project**: [Google Cloud Console](https://console.cloud.google.com/)
    2. **Enable APIs**: YouTube Data API v3
    3. **Create Credentials**: OAuth 2.0 Client ID (Desktop App)
    4. **Download**: Save as `client_secrets.json`
    5. **Place**: Put in project root directory
    """)
    
    st.markdown("---")
    st.markdown("**Current Status**:")
    if st.session_state['video_data'] is None:
        st.warning("No video analyzed")
    else:
        st.success(f"Analyzed: {video_data.get('title', 'Unknown')[:30]}...")
