from pytube import YouTube
from pathlib import Path

videos_dir = Path(__file__).parent / "videos"


def download_youtube_video(video_url, save_path="."):
    """Downloads a YouTube video to the specified path.

    Args:
        video_url: The URL of the YouTube video.
        save_path: The directory to save the downloaded video.
    """
    yt = YouTube(video_url)
    # Create a YouTube object

    # Display video details
    print("Title:", yt.title)
    print("Length (seconds):", yt.length)
    print("Views:", yt.views)

    # Get the highest resolution stream
    stream = yt.streams.get_highest_resolution()
    print(f"Downloading: {yt.title}")
    stream.download(output_path=save_path)
    print("Download complete!")


if __name__ == "__main__":
    video_url = "https://www.youtube.com/watch?v=k9KgyVaKDjw"
    save_path = videos_dir / "k9KgyVaKDjw.mp4"
    download_youtube_video(video_url, save_path)
