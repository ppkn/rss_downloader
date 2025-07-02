#!/usr/bin/env -S uv run --script
#
# /// script
# dependencies = [
#   "feedparser>=6.0.10",
#   "requests>=2.31.0",
#   "urllib3>=2.0.7",
# ]
# ///

"""
RSS Feed MP3 Downloader

This script downloads the 10 most recent episodes from a given RSS feed URL.
It supports various audio formats and creates organized directories for downloads.

Usage:
    uv run rss_downloader.py <RSS_FEED_URL>
    uv run rss_downloader.py <RSS_FEED_URL> --output my_podcasts
    uv run rss_downloader.py <RSS_FEED_URL> --episodes 5
"""

import os
import sys
import argparse
import feedparser
import requests
from urllib.parse import urlparse, unquote
from pathlib import Path
import re
from datetime import datetime


class RSSDownloader:
    def __init__(self, output_dir="downloads"):
        """Initialize the RSS downloader with output directory."""
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)

    def clean_filename(self, filename):
        """Clean filename by removing invalid characters."""
        # Remove or replace invalid characters for filesystem
        filename = re.sub(r'[<>:"/\\|?*]', "_", filename)
        # Remove extra spaces and dashes
        filename = re.sub(r"\s+", " ", filename).strip()
        filename = re.sub(r"-+", "-", filename)
        return filename

    def get_file_extension(self, url):
        """Extract file extension from URL."""
        parsed_url = urlparse(url)
        path = parsed_url.path
        if "." in path:
            return path.split(".")[-1].lower()
        return "mp3"  # Default to mp3 if no extension found

    def download_file(self, url, filepath):
        """Download a file from URL to the specified filepath."""
        try:
            print(f"Downloading: {url}")
            response = requests.get(url, stream=True, timeout=30)
            response.raise_for_status()

            total_size = int(response.headers.get("content-length", 0))
            downloaded = 0

            with open(filepath, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)
                        if total_size > 0:
                            percent = (downloaded / total_size) * 100
                            print(f"\rProgress: {percent:.1f}%", end="", flush=True)

            print(f"\nDownloaded: {filepath}")
            return True

        except requests.exceptions.RequestException as e:
            print(f"Error downloading {url}: {e}")
            return False

    def parse_rss_feed(self, feed_url):
        """Parse RSS feed and return entries."""
        try:
            print(f"Parsing RSS feed: {feed_url}")
            feed = feedparser.parse(feed_url)

            if feed.bozo:
                print(f"Warning: Feed parsing issues detected: {feed.bozo_exception}")

            if not feed.entries:
                print("No entries found in the RSS feed.")
                return []

            print(f"Found {len(feed.entries)} entries in the feed.")
            return feed.entries

        except Exception as e:
            print(f"Error parsing RSS feed: {e}")
            return []

    def extract_audio_url(self, entry):
        """Extract audio URL from RSS entry."""
        # Check for enclosures (most common for audio podcasts)
        if hasattr(entry, "enclosures") and entry.enclosures:
            for enclosure in entry.enclosures:
                if enclosure.get("type", "").startswith("audio/"):
                    return enclosure.get("href")

        # Check for media content
        if hasattr(entry, "media_content") and entry.media_content:
            for media in entry.media_content:
                if media.get("type", "").startswith("audio/"):
                    return media.get("url")

        # Check for links
        if hasattr(entry, "links") and entry.links:
            for link in entry.links:
                if link.get("type", "").startswith("audio/"):
                    return link.get("href")

        return None

    def download_episodes(self, feed_url, max_episodes=10):
        """Download the most recent episodes from the RSS feed."""
        entries = self.parse_rss_feed(feed_url)

        if not entries:
            print("No entries found. Exiting.")
            return

        # Limit to the most recent episodes
        recent_entries = entries[:max_episodes]

        print(f"\nDownloading {len(recent_entries)} most recent episodes...")

        successful_downloads = 0

        for i, entry in enumerate(recent_entries, 1):
            print(f"\n--- Episode {i}/{len(recent_entries)} ---")

            # Extract title and date
            title = getattr(entry, "title", f"Episode_{i}")
            published = getattr(entry, "published", "")

            # Clean title for filename
            clean_title = self.clean_filename(title)

            # Extract audio URL
            audio_url = self.extract_audio_url(entry)

            if not audio_url:
                print(f"No audio URL found for episode: {title}")
                continue

            # Determine file extension
            file_ext = self.get_file_extension(audio_url)

            # Create filename with date if available
            if published:
                try:
                    # Try to parse the date
                    date_obj = datetime.strptime(published, "%a, %d %b %Y %H:%M:%S %z")
                    date_str = date_obj.strftime("%Y-%m-%d")
                    filename = f"{date_str}_{clean_title}.{file_ext}"
                except:
                    filename = f"{clean_title}.{file_ext}"
            else:
                filename = f"{clean_title}.{file_ext}"

            # Create filepath
            filepath = self.output_dir / filename

            # Skip if file already exists
            if filepath.exists():
                print(f"File already exists, skipping: {filename}")
                successful_downloads += 1
                continue

            # Download the file
            if self.download_file(audio_url, filepath):
                successful_downloads += 1

        print(
            f"\nDownload complete! {successful_downloads}/{len(recent_entries)} episodes downloaded successfully."
        )
        print(f"Files saved to: {self.output_dir.absolute()}")


def main():
    """Main function to handle command line arguments and run the downloader."""
    parser = argparse.ArgumentParser(
        description="Download the 10 most recent episodes from an RSS feed",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  uv run rss_downloader.py https://feeds.example.com/podcast.xml
  uv run rss_downloader.py https://feeds.example.com/podcast.xml --output my_podcasts
  uv run rss_downloader.py https://feeds.example.com/podcast.xml --episodes 5
        """,
    )

    parser.add_argument("feed_url", help="URL of the RSS feed to download from")

    parser.add_argument(
        "--output",
        "-o",
        default="downloads",
        help="Output directory for downloaded files (default: downloads)",
    )

    parser.add_argument(
        "--episodes",
        "-e",
        type=int,
        default=10,
        help="Number of most recent episodes to download (default: 10)",
    )

    args = parser.parse_args()

    # Validate URL
    if not args.feed_url.startswith(("http://", "https://")):
        print("Error: Please provide a valid HTTP/HTTPS URL")
        sys.exit(1)

    # Create downloader and start downloading
    downloader = RSSDownloader(args.output)
    downloader.download_episodes(args.feed_url, args.episodes)


if __name__ == "__main__":
    main()
