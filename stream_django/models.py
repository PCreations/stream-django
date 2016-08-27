from stream.serializer import (
    dumps as json_dumps,
    loads as json_loads
)

try:
    from django.apps import apps
    get_model = apps.get_model
except ImportError:
    from django.db.models.loading import get_model

from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


class StreamActivityManager(models.Manager):

    def _build_activity_data(self, stream_activity, activity_data):
        from stream_django.activity import create_reference
        data = activity_data.copy()
        data.update({
            'original_foreign_id': data['foreign_id'],
            'original_object': data['object']
        })
        data['foreign_id'] = create_reference(stream_activity)
        data['object'] = create_reference(stream_activity)

        return data

    def create_activity(self, activity_data, activity_author_feed=None, activity_actor_id=None):
        '''
        activity_data is intended to be the dict returned by
        Activity.create_activity() method
        '''
        f_ct, f_id = activity_data['foreign_id'].split(':')
        model = get_model(*f_ct.split('.'))
        ct = ContentType.objects.get_for_model(model)
        stream_activity = self.model(
            original_foreign_id=activity_data['foreign_id'],
            actor=activity_data['actor'],
            verb=activity_data['verb'],
            activity_author_feed=activity_author_feed,
            activity_actor_id=activity_actor_id,
            content_type=ct,
            object_pk=f_id
        )
        stream_activity.save()
        stream_activity.data = self._build_activity_data(
            stream_activity,
            activity_data
        )
        stream_activity.save()
        return stream_activity

    def update_or_create_activity(self, activity_data, activity_author_feed=None, activity_actor_id=None):
        try:
            stream_activity = self.get_queryset().get(
                actor=activity_data['actor'],
                verb=activity_data['verb'],
                original_foreign_id=activity_data['foreign_id']
            )
            stream_activity.data = self._build_activity_data(
                stream_activity,
                activity_data
            )
            stream_activity.save()
            return stream_activity
        except self.model.DoesNotExist:
            return self.create_activity(activity_data, activity_author_feed, activity_actor_id)

    def get_from_activity_data(self, activity_data):
        try:
            return self.get_queryset().get(
                actor=activity_data['actor'],
                verb=activity_data['verb'],
                original_foreign_id=activity_data['foreign_id']
            )
        except (self.model.DoesNotExist, self.model.MultipleObjectsReturned) as e:
            raise e

    def get_for_original_object(self, model):
        ct = ContentType.objects.get_for_model(model)
        try:
            return self.get_queryset().get(content_type=ct, object_pk=model.pk)
        except self.model.DoesNotExist:
            return self.get_queryset().none()


class StreamActivity(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    actor = models.CharField(max_length=100, null=True, blank=True)
    verb = models.CharField(max_length=100, null=True, blank=True)
    original_foreign_id = models.CharField(max_length=100, null=True, blank=True)
    activity_author_feed = models.CharField(max_length=100, null=True, blank=True)
    activity_actor_id = models.CharField(max_length=100, null=True, blank=True)

    content_type = models.ForeignKey(ContentType, null=True, blank=True)
    object_pk = models.TextField(null=True, blank=True)
    content_object = GenericForeignKey('content_type', 'object_pk')

    _data = models.TextField(db_column='data', default='')


    objects = StreamActivityManager()

    def rehydrate_data(self):
        self.data = StreamActivity.objects._build_activity_data(
            self,
            self.content_object.create_activity()
        )
        self.save()

    @property
    def data(self):
        return json_loads(self._data)

    @data.setter
    def data(self, data):
        self._data = json_dumps(data)
