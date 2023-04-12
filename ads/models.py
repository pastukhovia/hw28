from django.db import models

from categories.models import Category
from users.models import User


class Ad(models.Model):
    class Meta:
        verbose_name = 'Объявление'
        verbose_name_plural = 'Объявления'

    name = models.CharField(max_length=50, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    price = models.FloatField(null=True)
    desc = models.CharField(max_length=1000, null=True)
    is_published = models.BooleanField(default=False)
    image = models.ImageField(upload_to='images', null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name
