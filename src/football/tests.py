from django.test import TestCase
from unittest.mock import (patch, Mock)
from django.conf import settings
from football.mocks import yt_channel_response
from datetime import datetime, timezone
from football.tasks import (
    get_youtube_video_id, get_latest_youtube_video,
    build_embed_link, save_video_db
)
from video.models import Video


class YTVideoTest(TestCase):

    def setUp(self):
        self.video_id = 'test-video-id'
        self.channel_id = 'test-channel'
        self.embed_url = settings.YT_EMBED_URL
    

    @patch('football.tasks.requests.request')
    def test_get_video_id(self, mock_get):
        mock_response = Mock()
        mock_response.json.return_value = yt_channel_response
        mock_get.return_value = mock_response

        video_id = get_youtube_video_id(self.channel_id)
        mock_get.assert_called()
        self.assertEqual(video_id, self.video_id)


    def test_build_embed_url(self):
        final_embed_link = build_embed_link(self.video_id)
        test_embed_link = self.embed_url + f'/{self.video_id}'

        self.assertEqual(final_embed_link, test_embed_link)
    

    def test_save_video_to_db(self):
        test_video_url = 'this-should-be-saved.com'
        update_db = save_video_db('locked_on_utes', test_video_url)

        self.assertTrue(update_db[1])

        # negative test
        failed_update = save_video_db('bad_channel_name', test_video_url)
        self.assertFalse(failed_update[1])


    @patch('football.tasks.requests.request')
    def test_get_latest_video_publish_date(self, mock_get):
        mock_response = Mock()
        mock_response.json.return_value = yt_channel_response
        mock_get.return_value = mock_response

        video_id, published_at = get_latest_youtube_video(self.channel_id)
        self.assertEqual(video_id, self.video_id)
        # publishedAt of the first item in football/mocks.py
        self.assertEqual(published_at, datetime(2024, 9, 25, 13, 0, 26, tzinfo=timezone.utc))


    def test_save_video_uses_publish_date(self):
        published_at = datetime(2024, 9, 25, 13, 0, 26, tzinfo=timezone.utc)
        video, created = save_video_db('locked_on_utes', 'published-date-test.com', published_at)

        self.assertTrue(created)
        self.assertEqual(video.air_date, published_at)
