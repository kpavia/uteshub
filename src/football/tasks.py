import requests
from django.conf import settings
from datetime import datetime
from video.models import Video
import pytz


def parse_youtube_datetime(value):
    """
    Parse a YouTube API timestamp like '2024-09-25T13:00:26Z'.

    Returns:
        datetime: timezone-aware UTC datetime, or None if missing/unparseable
    """
    if not value:
        return None
    try:
        return datetime.fromisoformat(value.replace('Z', '+00:00'))
    except ValueError:
        return None


def get_latest_youtube_video(channel_id):
    """
    Get the newest video on a youtube channel

    Args:
        channel_id (str): youtube channel ID

    Returns:
        tuple: (video ID, publish datetime). (None, None) if no usable video.
            The publish datetime can be None if YouTube didn't send one.
    """
    search_url = settings.YT_SEARCH_URL
    api_key = settings.YT_API_KEY
    params = {
        'channelId': channel_id,
        'order': 'date',
        'part': 'snippet',
        'key': api_key
    }

    request = requests.request('GET', url=search_url, params=params)
    item = (request.json().get('items') or [{}])[0]
    video_id = item.get('id', {}).get('videoId', {})
    snippet = item.get('snippet', {})
    video_title = snippet.get('title', '')
    video_description = snippet.get('description', '')
    published_at = parse_youtube_datetime(snippet.get('publishedAt'))
    if video_id:
        if channel_id == settings.YT_CHANNEL_IDS.get('utah_blockcast'):
            if 'Utah Blockcast' in video_title or 'Utah Blockcast' in video_description:
                return (video_id, published_at)
            return (None, None)
        return (video_id, published_at)
    print(f'YT GET request failed to get video ID for channel {channel_id}')
    return (None, None)


def get_youtube_video_id(channel_id):
    """
    Get the video ID of a youtube video from the channel

    Args:
        channel_id (str): youtube channel ID

    Returns:
        str: video ID
    """
    return get_latest_youtube_video(channel_id)[0]


def build_embed_link(video_id):
    embed_url = settings.YT_EMBED_URL
    return embed_url + f'/{video_id}'


def save_video_db(channel_name, video_link, published_at=None):
    """
    Save a video if its link isn't already stored.

    air_date is the YouTube publish time when given, otherwise the time of
    this fetch. Videos that already exist are left unchanged.
    """
    channels = {
        'locked_on_utes': 'locked_on_utes',
        'utah_utes_football_digest': 'utes_digest',
        'utah_football_fans': 'utah_football_fans',
        'rising_report': 'rising_report',
        'game_highlights': 'game_highlights',
        'athletics': 'u_of_u_athletics',
        'utah_blockcast': 'utah_blockcast'
    }
    mst = pytz.timezone('US/Mountain')
    channel = channels.get(channel_name)
    if not channel:
        return (None, False)
    video, created = Video.objects.get_or_create(
        link=video_link,
        defaults={
            'channel': channel,
            'air_date': published_at or datetime.now(mst)
        }
    )
    return (video, created)


def update_video_db():
    channel_ids = settings.YT_CHANNEL_IDS
    for channel_name, channel_id in channel_ids.items():
        print(f'Fetching new video for {channel_name}')
        video_id, published_at = get_latest_youtube_video(channel_id)
        if video_id:
            embed_link = build_embed_link(video_id)
            result = save_video_db(channel_name, embed_link, published_at)
            print(f'New video built for {channel_name}: {result[0]}, {result[1]}')
