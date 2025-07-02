#!/usr/bin/env python3
# /// script
# dependencies = [
#   "feedparser>=6.0.10",
#   "requests>=2.31.0",
#   "urllib3>=2.0.7",
# ]
# ///

"""
Test script to verify that the RSS downloader dependencies are working correctly.
"""


def test_imports():
    """Test that all required modules can be imported."""
    try:
        import feedparser

        print("✓ feedparser imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import feedparser: {e}")
        return False

    try:
        import requests

        print("✓ requests imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import requests: {e}")
        return False

    try:
        import urllib3

        print("✓ urllib3 imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import urllib3: {e}")
        return False

    return True


def test_rss_downloader():
    """Test that the RSSDownloader class can be imported."""
    try:
        from rss_downloader import RSSDownloader

        print("✓ RSSDownloader class imported successfully")

        # Test creating an instance
        downloader = RSSDownloader("test_downloads")
        print("✓ RSSDownloader instance created successfully")

        return True
    except Exception as e:
        print(f"✗ Failed to import RSSDownloader: {e}")
        return False


def main():
    """Run all tests."""
    print("Testing RSS MP3 Downloader with uv inline metadata...\n")

    all_passed = True

    # Test imports
    if not test_imports():
        all_passed = False

    print()

    # Test RSSDownloader
    if not test_rss_downloader():
        all_passed = False

    print()

    if all_passed:
        print("🎉 All tests passed! The RSS MP3 Downloader is ready to use.")
        print("\nYou can now run:")
        print("  uv run rss_downloader.py <RSS_FEED_URL>")
    else:
        print("❌ Some tests failed. Please check the error messages above.")


if __name__ == "__main__":
    main()
