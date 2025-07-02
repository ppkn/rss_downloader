# RSS MP3 Downloader

A Python script to download the 10 most recent episodes from an RSS feed URL using [uv](https://docs.astral.sh/uv/) for dependency management. This tool is perfect for downloading podcast episodes, audio content, or any media files distributed via RSS feeds.

## Features

- Downloads the 10 most recent episodes from any RSS feed
- Supports various audio formats (MP3, M4A, WAV, etc.)
- Creates organized filenames with dates
- Shows download progress
- Skips already downloaded files
- Handles various RSS feed formats
- Uses uv for automatic dependency management
- No manual environment setup required
- Can be run as an executable

## Prerequisites

- [uv](https://docs.astral.sh/uv/getting-started/installation/) installed on your system

## Installation

1. Clone or download this repository
2. Make the script executable: `chmod +x rss_downloader.py`. (This may not be necessary.)
3. No additional setup required! The script uses inline metadata to declare its dependencies

## Usage

### Basic Usage

Download the 10 most recent episodes from an RSS feed:

```bash
./rss_downloader.py https://feeds.example.com/podcast.xml
```

Or using uv run (alternative method):
```bash
uv run rss_downloader.py https://feeds.example.com/podcast.xml
```

### Advanced Usage

Download to a custom directory:
```bash
./rss_downloader.py https://feeds.example.com/podcast.xml --output my_podcasts
```

Download only 5 episodes:
```bash
./rss_downloader.py https://feeds.example.com/podcast.xml --episodes 5
```

### Command Line Options

- `feed_url`: The RSS feed URL to download from (required)
- `--output, -o`: Output directory for downloaded files (default: downloads)
- `--episodes, -e`: Number of most recent episodes to download (default: 10)

## Examples

```bash
# Download from a popular podcast
./rss_downloader.py https://feeds.npr.org/510313/podcast.xml

# Download to a specific folder
./rss_downloader.py https://feeds.example.com/podcast.xml --output ~/Music/Podcasts

# Download only the 3 most recent episodes
./rss_downloader.py https://feeds.example.com/podcast.xml --episodes 3
```

## How It Works

The script uses [uv's inline script metadata](https://docs.astral.sh/uv/guides/scripts/#declaring-script-dependencies) to declare its dependencies:

```python
# /// script
# dependencies = [
#   "feedparser>=6.0.10",
#   "requests>=2.31.0",
#   "urllib3>=2.0.7",
# ]
# ///
```

The script has a shebang line `#!/usr/bin/env -S uv run --script` that allows it to be run as an executable. When you run `./rss_downloader.py`, uv automatically:
1. Creates a virtual environment
2. Installs the required dependencies
3. Runs the script with those dependencies
4. Cleans up the environment afterward

## Testing

You can test that everything is working correctly:

```bash
uv run test_script.py
```

## Supported RSS Formats

The script supports various RSS feed formats including:
- Standard RSS 2.0 with enclosures
- RSS with media content
- Atom feeds with audio links
- Custom RSS formats with audio attachments

## Dependencies

The script automatically manages these dependencies:
- `feedparser` - for parsing RSS feeds
- `requests` - for downloading files
- `urllib3` - for URL handling

## Notes

- Files are saved with the original file extension from the URL
- If no extension is found, files are saved as `.mp3`
- Invalid characters in filenames are replaced with underscores
- The script creates the output directory if it doesn't exist
- Download progress is shown for each file
- No manual virtual environment management required

## Troubleshooting

If you encounter issues:

1. **No audio URLs found**: Some RSS feeds may not include direct audio links. Check if the feed URL is correct.
2. **Download errors**: Check your internet connection and ensure the audio URLs are accessible.
3. **Permission errors**: Make sure you have write permissions in the output directory.
4. **uv not found**: Install uv following the [official installation guide](https://docs.astral.sh/uv/getting-started/installation/).

## Advantages of Using uv

- **No manual environment setup**: Dependencies are managed automatically
- **Reproducible**: Same dependencies every time
- **Fast**: uv is significantly faster than pip
- **Clean**: No leftover virtual environments
- **Portable**: Works the same way across different systems

## License

This script is provided as-is for educational and personal use. 