from django.db import models

from licence.models import Licence


class Software(models.Model):
    name = models.CharField(max_length=100)
    extension = models.CharField(max_length=100, null=True,)
    licence = models.OneToOneField(Licence, null=True)


    def __str__(self):
        return u"%s" % self.name
