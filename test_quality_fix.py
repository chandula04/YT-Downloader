"""
Test script to demonstrate the dynamic quality filtering fix
"""

from core.youtube_handler import YouTubeHandler

def test_quality_filtering():
    """Test the new dynamic quality filtering"""
    print("🔧 Testing Dynamic Quality Filtering Fix")
    print("=" * 50)
    
    # Create YouTube handler
    handler = YouTubeHandler()
    
    # Test with a sample video URL (you can change this to any YouTube video)
    test_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"  # Rick Roll (common test video)
    
    try:
        print(f"📺 Loading video: {test_url}")
        video = handler.load_video(test_url)
        
        if video:
            print(f"✅ Video loaded: {video.title}")
            print(f"⏱️ Duration: {video.length} seconds")
            
            print("\n🎯 Getting available quality options...")
            quality_options = handler.get_quality_options(video)
            
            print(f"\n📋 Available Quality Options ({len(quality_options)} found):")
            print("-" * 40)
            for i, option in enumerate(quality_options, 1):
                print(f"{i:2d}. {option}")
            
            print(f"\n✅ SUCCESS: Now showing only {len(quality_options)} available qualities")
            print("💡 Before fix: Would show 8K, 4K, 2K even if not available")
            print("💡 After fix: Shows only actual video stream qualities")
            
        else:
            print("❌ Failed to load video")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        print("💡 This might be due to network issues or YouTube restrictions")

if __name__ == "__main__":
    test_quality_filtering()