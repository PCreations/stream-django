import unittest
import json
import datetime
import uuid

from stream.serializer import (
    dumps as json_dumps,
    loads as json_loads
)
from stream_django.activity import (
    Activity,
    create_reference
)
from stream_django.feed_manager import feed_manager
from django.test import TestCase as DjangoTestCase

from stream_django.models import (
    StreamActivityManager,
    StreamActivity
)

class StreamActivityManagerTestCase(DjangoTestCase):

    def setUp(self):
        feed_manager.disable_model_tracking()

    def test_create_activity(self):
        time = datetime.datetime.now()
        activity_data = {
            'actor': 'auth.User:42',
            'foo': 'Foobar',
            'baz': ['foo', 'bar'],
            'foreign_id': 'foos.Foo:42',
            'object': 'foos.Foo:42',
            'time': time,
            'verb': 'fooed'
        }

        stream_activity = StreamActivity.objects.create_activity(activity_data)

        self.assertEqual(stream_activity.data, {
            'actor': 'auth.User:42',
            'foo': 'Foobar',
            'baz': ['foo', 'bar'],
            'original_foreign_id': 'foos.Foo:42',
            'original_object': 'foos.Foo:42',
            'foreign_id': create_reference(stream_activity),
            'object': create_reference(stream_activity),
            'time': time,
            'verb': 'fooed'
        })

        self.assertEqual(stream_activity.actor, 'auth.User:42')
        self.assertEqual(stream_activity.verb, 'fooed')
        self.assertEqual(stream_activity.original_foreign_id, 'foos.Foo:42')

    def test_build_activity_data_does_not_modify_original_dict(self):
        time = datetime.datetime.now()
        activity_data = {
            'actor': 'auth.User:42',
            'foo': 'Foobar',
            'baz': ['foo', 'bar'],
            'foreign_id': 'foos.Foo:42',
            'object': 'foos.Foo:42',
            'time': time,
            'verb': 'fooed'
        }
        stream_activity = StreamActivity.objects.create_activity(activity_data)

        self.assertEqual(activity_data, {
            'actor': 'auth.User:42',
            'foo': 'Foobar',
            'baz': ['foo', 'bar'],
            'foreign_id': 'foos.Foo:42',
            'object': 'foos.Foo:42',
            'time': time,
            'verb': 'fooed'
        })

    def test_get_stream_activity_from_activity_data(self):
        time = datetime.datetime.now()
        activity_data = {
            'actor': 'auth.User:42',
            'foo': 'Foobar',
            'baz': ['foo', 'bar'],
            'foreign_id': 'foos.Foo:42',
            'object': 'foos.Foo:42',
            'time': time,
            'verb': 'fooed'
        }
        stream_activity = StreamActivity.objects.create_activity(activity_data)

        self.assertEqual(StreamActivity.objects.get_from_activity_data(activity_data), stream_activity)

    def test_update_or_create_activity_returns_updated_existing_activity(self):
        time = datetime.datetime.now()
        activity_data = {
            'actor': 'auth.User:42',
            'foo': 'Foobar',
            'baz': ['foo', 'bar'],
            'foreign_id': 'foos.Foo:42',
            'object': 'foos.Foo:42',
            'time': time,
            'verb': 'fooed'
        }

        stream_activity = StreamActivity.objects.create_activity(activity_data)

        new_time = datetime.datetime.now()

        new_activity_data = {
            'actor': 'auth.User:42',
            'foo': 'Foobar',
            'baz': ['foo', 'bar', 'baz'],
            'foreign_id': 'foos.Foo:42',
            'object': 'foos.Foo:42',
            'time': new_time,
            'verb': 'fooed'
        }

        updated_stream_activity = StreamActivity.objects.update_or_create_activity(new_activity_data)

        self.assertEqual(stream_activity.pk, updated_stream_activity.pk)
        self.assertEqual(updated_stream_activity.data, {
            'actor': 'auth.User:42',
            'foo': 'Foobar',
            'baz': ['foo', 'bar', 'baz'],
            'original_foreign_id': 'foos.Foo:42',
            'original_object': 'foos.Foo:42',
            'foreign_id': create_reference(updated_stream_activity),
            'object': create_reference(updated_stream_activity),
            'time': new_time,
            'verb': 'fooed'
        })

    def test_update_or_create_returns_new_activity_if_verb_and_original_foreign_id_are_the_same_but_actor_is_different(self):
        time = datetime.datetime.now()
        activity_data = {
            'actor': 'auth.User:42',
            'foo': 'Foobar',
            'baz': ['foo', 'bar'],
            'foreign_id': 'foos.Foo:42',
            'object': 'foos.Foo:42',
            'time': time,
            'verb': 'fooed'
        }

        stream_activity = StreamActivity.objects.create_activity(activity_data)

        new_time = datetime.datetime.now()

        new_activity_data = {
            'actor': 'auth.User:43',
            'foo': 'Foobar',
            'baz': ['foo', 'bar', 'baz'],
            'foreign_id': 'foos.Foo:42',
            'object': 'foos.Foo:42',
            'time': new_time,
            'verb': 'fooed'
        }

        new_stream_activity = StreamActivity.objects.update_or_create_activity(new_activity_data)

        self.assertTrue(stream_activity.pk != new_stream_activity.pk)

    def test_update_or_create_returns_new_activity_if_actor_and_original_foreign_id_are_the_same_but_verb_is_different(self):
        time = datetime.datetime.now()
        activity_data = {
            'actor': 'auth.User:42',
            'foo': 'Foobar',
            'baz': ['foo', 'bar'],
            'foreign_id': 'foos.Foo:42',
            'object': 'foos.Foo:42',
            'time': time,
            'verb': 'fooed'
        }

        stream_activity = StreamActivity.objects.create_activity(activity_data)

        new_time = datetime.datetime.now()

        new_activity_data = {
            'actor': 'auth.User:42',
            'foo': 'Foobar',
            'baz': ['foo', 'bar', 'baz'],
            'foreign_id': 'foos.Foo:42',
            'object': 'foos.Foo:42',
            'time': new_time,
            'verb': 'bared'
        }

        new_stream_activity = StreamActivity.objects.update_or_create_activity(new_activity_data)

        self.assertTrue(stream_activity.pk != new_stream_activity.pk)

    def test_update_or_create_returns_new_activity_if_actor_and_verb_are_the_same_but_original_foreign_id_is_different(self):
        time = datetime.datetime.now()
        activity_data = {
            'actor': 'auth.User:42',
            'foo': 'Foobar',
            'baz': ['foo', 'bar'],
            'foreign_id': 'foos.Foo:42',
            'object': 'foos.Foo:42',
            'time': time,
            'verb': 'fooed'
        }

        stream_activity = StreamActivity.objects.create_activity(activity_data)

        new_time = datetime.datetime.now()

        new_activity_data = {
            'actor': 'auth.User:42',
            'foo': 'Foobar',
            'baz': ['foo', 'bar', 'baz'],
            'foreign_id': 'foos.Foo:43',
            'object': 'foos.Foo:42',
            'time': new_time,
            'verb': 'bared'
        }

        new_stream_activity = StreamActivity.objects.update_or_create_activity(new_activity_data)

        self.assertTrue(stream_activity.pk != new_stream_activity.pk)


class StreamActivityModelTestCase(unittest.TestCase):

    def setUp(self):
        feed_manager.disable_model_tracking()

    def test_stream_activity_data_setter_correctly_set_field_value_to_json_string_repr(self):
        activity = StreamActivity()
        data = {
            'foo': 'bar',
            'bar': {
                'baz': 'foo',
                'bar': datetime.datetime.now()
            }
        }
        json_data_str = json_dumps(data)
        try:
            activity.data = data
        except ValueError:
            pass

        self.assertEqual(activity._data, json_data_str)

    def test_stream_activity_data_getter_correctly_returns_python_object_from_json_string_repr(self):
        activity = StreamActivity()
        json_data_str = '{"foo": "bar", "bar": {"bar": "2016-04-10T15:06:57.081233", "baz": "foo"}}'
        activity._data = json_data_str

        self.assertEqual(activity.data, json_loads(json_data_str))
