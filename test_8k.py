#!/usr/bin/env python3
"""
Test script to check 8K video detection
"""

from core.youtube_handler import YouTubeHandler

def test_8k_video():
    """Test 8K video quality detection"""
    
    print("🔍 Testing 8K Video Quality Detection")
    print("=" * 50)
    
    # Common 8K test videos (replace with your 8K video URL)
    test_urls = [
        "https://youtube.com/watch?v=Te78AQ4OY0w",  # Your video
        # Add more 8K video URLs here for testing
    ]
    
    handler = YouTubeHandler()
    
    for url in test_urls:
        print(f"\n🎬 Testing: {url}")
        print("-" * 30)
        
        try:
            # Load video
            video = handler.load_video(url)
            
            if video:
                print(f"📹 Title: {video.title}")
                print(f"⏱️ Duration: {video.length}s")
                
                # Get quality options
                print("\n🎯 Getting quality options...")
                qualities = handler.get_quality_options(video)
                
                print(f"\n📊 Found {len(qualities)} quality options:")
                for i, quality in enumerate(qualities, 1):
                    marker = "🎯" if "8K" in quality or "4320p" in quality else "📱"
                    print(f"   {marker} {i}. {quality}")
                
                # Check for 8K specifically
                has_8k = any("8K" in q or "4320p" in q for q in qualities)
                if has_8k:
                    print("\n✅ 8K option found!")
                else:
                    print("\n❌ No 8K option found")
                    print("💡 This video may not have 8K streams available")
                    
            else:
                print("❌ Failed to load video")
                
        except Exception as e:
            print(f"❌ Error: {e}")
        
        print("\n" + "=" * 50)

if __name__ == "__main__":
    test_8k_video()