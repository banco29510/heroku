from django.db import models

class Instrument(models.Model):
    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to = 'media', null=True)

    def __str__(self):
        return u"%s" % self.name
