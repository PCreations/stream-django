from django.db import models
from django.conf import settings
from stream_django.activity import Activity


class Pin(models.Model, Activity):
    author = models.ForeignKey(settings.AUTH_USER_MODEL)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def activity_object_attr(self):
        return self

    @property
    def activity_actor_attr(self):
        return self.author


class Tweet(Activity, models.Model):

    @property
    def activity_time(self):
        return None

    @property
    def activity_object_attr(self):
        return self

    @property
    def activity_actor(self):
        return self.actor

    @property
    def activity_notify(self):
        from stream_django.feed_manager import feed_manager
        return [feed_manager.get_notification_feed('thierry')]
