# Watch-Time Booster Dashboard

A comprehensive Streamlit-based web application for analyzing and optimizing YouTube video watch time performance. This tool provides detailed insights, optimization suggestions, and actionable recommendations to help content creators maximize their video engagement and watch time.

![Dashboard Preview](https://img.shields.io/badge/Status-Active-brightgreen) ![Python](https://img.shields.io/badge/Python-3.14-blue) ![Streamlit](https://img.shields.io/badge/Streamlit-1.52-red)

## 🚀 Features

### Core Functionality
- **Single Video Analysis**: Enter any YouTube video URL to get comprehensive analysis
- **Watch Time Optimization**: Detailed metrics and suggestions for improving viewer retention
- **Engagement Analysis**: Like-to-view ratios, comment engagement, and optimization scoring
- **Content Strategy Recommendations**: Tailored suggestions based on video characteristics
- **Competitive Insights**: Category-specific optimization strategies

### Analytics & Insights
- **Current Watch Time Calculation**: Estimate total watch time based on views and retention
- **Optimization Score (0-100)**: Comprehensive scoring based on multiple factors
- **Engagement Metrics**: Detailed breakdown of likes, comments, and engagement rates
- **Potential Improvement**: Calculate potential watch time gains with optimization

### Optimization Categories
1. **Content Strategy**: Title optimization, description enhancement, tag suggestions
2. **Technical Optimization**: Audio/visual quality, upload timing, duration optimization
3. **Engagement Tactics**: Hook optimization, call-to-action strategies, interactive elements
4. **Competitive Insights**: Market positioning, category-specific recommendations
5. **Posting Strategy**: Upload frequency, cross-platform promotion, community building

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.14 or higher
- Google Cloud Console account
- YouTube Data API v3 access

### Step 1: Clone and Setup
```bash
git clone <repository-url>
cd watchtime_booster
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### Step 2: Install Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Step 3: YouTube API Setup
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Enable YouTube Data API v3
4. Create OAuth 2.0 credentials (Desktop Application)
5. Download the credentials as `client_secrets.json`
6. Place the file in the project root directory

### Step 4: Run the Application
```bash
source .venv/bin/activate
streamlit run src/dashboard.py
```

The dashboard will be available at `http://localhost:8501`

## 📁 Project Structure

```
watchtime_booster/
├── src/
│   ├── __init__.py              # Package initialization
│   ├── dashboard.py             # Main Streamlit application
│   ├── yt_auth.py               # YouTube OAuth authentication
│   ├── yt_fetch.py              # Video data fetching functions
│   ├── analytics.py             # Watch time analysis algorithms
│   ├── recommender.py           # Optimization suggestions engine
│   └── clipper.py               # Video clipping utilities
├── client_secrets.json          # YouTube API credentials
├── setup.py                     # Package setup configuration
├── requirements.txt             # Python dependencies
└── README.md                    # This file
```

## 🎯 How to Use

### 1. Analyze a Video
1. Copy the YouTube video URL you want to analyze
2. Paste it into the input field on the dashboard
3. Click "🚀 Analyze Video"
4. Wait for the analysis to complete

### 2. Review Results
The analysis provides:
- **Video Information**: Title, channel, duration, publication date
- **Key Metrics**: Views, likes, comments, engagement rates
- **Watch Time Analysis**: Current watch time, potential improvements
- **Optimization Score**: Overall performance rating (0-100)

### 3. Implement Suggestions
Based on the analysis, you'll receive:
- **Immediate Actions**: Quick wins for better performance
- **Content Strategy**: Long-term optimization approaches
- **Technical Improvements**: Production quality enhancements
- **Engagement Tactics**: Audience interaction strategies

## 🔧 API Configuration

### Required YouTube APIs
- **YouTube Data API v3**: For video metadata and statistics
- **YouTube Analytics API**: For detailed performance metrics (optional)

### OAuth Scopes Used
```
https://www.googleapis.com/auth/youtube.readonly
https://www.googleapis.com/auth/yt-analytics.readonly
https://www.googleapis.com/auth/youtube
```

## 📊 Understanding the Analysis

### Optimization Score Breakdown
- **90-100**: Excellent optimization, maintain current strategies
- **70-89**: Good performance, minor improvements possible
- **50-69**: Moderate optimization, several areas for improvement
- **30-49**: Below average, significant optimization needed
- **0-29**: Poor optimization, major changes required

### Key Metrics Explained
- **Engagement Rate**: (Likes + Comments) / Views
- **Watch Time Potential**: Views × Estimated Retention × Duration
- **Optimization Score**: Weighted algorithm considering multiple factors
- **Like-to-View Ratio**: Likes per 100 views
- **Comment-to-View Ratio**: Comments per 100 views

## 🎨 Features & Capabilities

### URL Format Support
The tool supports all YouTube URL formats:
- `https://www.youtube.com/watch?v=VIDEO_ID`
- `https://youtu.be/VIDEO_ID`
- `https://youtube.com/embed/VIDEO_ID`
- `https://youtube.com/v/VIDEO_ID`

### Video Information Extracted
- Video title and description
- Channel information
- Publication date and metadata
- View count, likes, comments
- Video duration (formatted and raw)
- Thumbnail URLs
- Video tags and category

### Analysis Algorithms
- **Retention Estimation**: Based on video length and engagement patterns
- **Optimization Scoring**: Multi-factor algorithm considering duration, engagement, and metadata
- **Recommendation Engine**: Context-aware suggestions based on video characteristics
- **Competitive Analysis**: Category-specific optimization strategies

## 🔍 Troubleshooting

### Common Issues

**Authentication Errors**
- Verify `client_secrets.json` is properly configured
- Ensure OAuth credentials are set up for Desktop Application
- Check that YouTube Data API v3 is enabled

**API Quota Limits**
- YouTube Data API has daily quota limits
- Consider implementing caching for repeated analyses
- Monitor usage in Google Cloud Console

**Missing Video Data**
- Some videos may not have public statistics
- Private or deleted videos will return errors
- Verify the video URL is correct and accessible

### Support
For issues and questions:
1. Check the troubleshooting section above
2. Verify API setup and credentials
3. Ensure all dependencies are installed correctly
4. Check the terminal output for detailed error messages

## 📈 Performance Tips

### For Best Results
1. **Use Public Videos**: Analysis requires publicly available video data
2. **Consider Video Age**: Newer videos may have incomplete analytics
3. **Check Engagement**: Videos with very low engagement may have limited insights
4. **Multiple Analyses**: Compare different video types for comprehensive understanding

### Optimization Strategies
- Focus on videos with high view counts for reliable data
- Analyze competitor videos for benchmarking
- Track improvements over time with regular analyses
- Use insights to inform future content creation

## 🔒 Privacy & Security

- All API calls are made directly to YouTube's official APIs
- Video data is fetched in real-time and not stored locally
- OAuth credentials are handled securely through Google's official flow
- No personal or sensitive data is collected or stored

## 📝 License

This project is open source and available under the MIT License.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit issues and enhancement requests.

---

**Happy optimizing! 📺✨**
