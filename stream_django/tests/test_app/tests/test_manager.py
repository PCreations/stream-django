import httpretty
import re
import unittest

from django.test import (
    TestCase,
    override_settings
)

from stream_django.feed_manager import feed_manager

from test_app.models import Tweet


api_url = re.compile(r'https://us-east-api.getstream.io/api/*.')


class ManagerTestCase(unittest.TestCase):

    def setUp(self):
        feed_manager.enable_model_tracking()

    def test_get_user_feed(self):
        feed = feed_manager.get_user_feed(42)
        self.assertEqual(feed.id, 'user:42')

    def test_get_user_feed_by_feed_type(self):
        feed = feed_manager.get_user_feed(42, 'personal')
        self.assertEqual(feed.id, 'personal:42')

    def test_get_notification_feed(self):
        feed = feed_manager.get_notification_feed(42)
        self.assertEqual(feed.id, 'notification:42')

    def test_get_actor_feed(self):
        tweet = Tweet()
        tweet.actor = 42
        feed = feed_manager.get_actor_feed(tweet)
        self.assertEqual(feed, 'user')

    @httpretty.activate
    def test_follow_user(self):
        httpretty.register_uri(httpretty.POST, api_url,
              body='{}', status=200,
              content_type='application/json')
        feed_manager.follow_user(1, 2)
        last_req = httpretty.last_request()
        self.assertTrue(last_req.path.split('?')[0].endswith('1/follows/'))

    @httpretty.activate
    def test_unfollow_user(self):
        httpretty.register_uri(httpretty.DELETE, api_url,
              body='{}', status=200,
              content_type='application/json')
        feed_manager.unfollow_user(1, 2)
        last_req = httpretty.last_request()
        self.assertEqual(last_req.method, 'DELETE')
        self.assertTrue(last_req.path.split('?')[0].endswith('1/follows/user:2/'))

    def test_get_feed(self):
        feed = feed_manager.get_feed('flat', 42)
        self.assertEqual(feed.id, 'flat:42')

    def test_get_news_feeds(self):
        feeds = feed_manager.get_news_feeds(42)
        self.assertIn('flat', feeds)
        self.assertIn('aggregated', feeds)
        self.assertEqual(feeds['flat'].id, 'flat:42')
        self.assertEqual(feeds['aggregated'].id, 'aggregated:42')
