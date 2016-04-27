from stream_django.conf import ACTIVITY_MODEL_CLASS
from stream_django.conf import DJANGO_MAJOR_VERSION
from django.db.models.signals import class_prepared
from stream_django.utils import get_class_from_string


StreamActivity = get_class_from_string(ACTIVITY_MODEL_CLASS)
