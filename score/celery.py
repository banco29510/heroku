from __future__ import absolute_import
import os
from celery import Celery

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'score.settings')

from django.conf import settings

app = Celery('score', broker='amqp://qkmnjppx:ELBOrLJanL8BMor2GqYYeaKjhxyhDDAI@spotted-monkey.rmq.cloudamqp.com/qkmnjppx')
app.conf.TASK_SERIALIZER="json"

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

app.conf.update(
    CELERY_RESULT_BACKEND='djcelery.backends.database:DatabaseBackend',
)
app.conf.update(
    CELERY_RESULT_BACKEND='djcelery.backends.cache:CacheBackend',
)

app.conf.CELERY_TIMEZONE = 'Europe/Paris'

@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))


#