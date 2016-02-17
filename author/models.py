from django.db import models

class Author(models.Model):
    name = models.CharField(max_length=75)
    birthDate = models.DateField(auto_now_add=False, auto_now=False,
                                verbose_name="Date de naissance", null=True, blank=True)
    deathDate = models.DateField(auto_now_add=False, auto_now=False,
                                verbose_name="Date de décès", null=True, blank=True)
    nationality = models.TextField(max_length=100, null=True, blank=True)

    def __str__(self):
        return u"%s" % self.name
