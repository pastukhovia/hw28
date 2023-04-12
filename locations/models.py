from django.db import models


class Location(models.Model):
    class Meta:
        verbose_name = 'Местоположение'
        verbose_name_plural = 'Местоположения'

    name = models.CharField(max_length=50, null=True)
    lat = models.FloatField(null=True)
    lng = models.FloatField(null=True)

    def __str__(self):
        return self.name
