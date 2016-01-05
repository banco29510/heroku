from django.db import models

class Instrument(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return u"%s" % self.name
