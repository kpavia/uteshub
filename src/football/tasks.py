import requests
from django.conf import settings
from datetime import datetime
from football.models import Video
import pytz


def get_youtube_video_id(channel_id):
    """
    Get the video ID of a youtube video from the channel

    Args:
        channel_id (str): youtube channel ID

    Returns:
        str: video ID
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
    video_id = request.json().get('items', [{}])[0].get('id', {}).get('videoId', {})
    if video_id:
        return video_id
    print(f'YT GET request failed to get video ID for channel {channel_id}')
    return None


def build_embed_link(video_id):
    embed_url = settings.YT_EMBED_URL
    return embed_url + f'/{video_id}'


def save_video_db(channel_name, video_link):
    channels = {
        'locked_on_utes': 'locked_on_utes',
        'utah_utes_football_digest': 'utes_digest',
        'utah_football_fans': 'utah_football_fans',
        'rising_report': 'rising_report',
        'game_highlights': 'game_highlights',
        'athletics': 'u_of_u_athletics'
    }
    mst = pytz.timezone('US/Mountain')
    channel = channels.get(channel_name)
    if not channel:
        return (None, False)
    video, created = Video.objects.get_or_create(
        link=video_link,
        defaults={
            'channel': channel,
            'air_date': datetime.now(mst)
        }
    )
    return (video, created)


def update_video_db():
    channel_ids = settings.YT_CHANNEL_IDS
    for channel_name, channel_id in channel_ids.items():
        print(f'Fetching new video for {channel_name}')
        video_id = get_youtube_video_id(channel_id)
        if video_id:
            embed_link = build_embed_link(video_id)
            result = save_video_db(channel_name, embed_link)
            print(f'New video built for {channel_name}: {result[0]}, {result[1]}')
