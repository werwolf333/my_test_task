from django.db import models


class Application(models.Model):
    name = models.CharField(max_length=40, blank=True, null=True)
    company = models.CharField(max_length=40, blank=True, null=True)
    released = models.IntegerField(blank=True, null=True)
    mail = models.CharField(max_length=40, blank=True, null=True)

    def __str__(self):
        return self.name
