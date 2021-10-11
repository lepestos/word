from django.db import models


class Text(models.Model):
    name = models.CharField(max_length=128)
    content = models.TextField()

    def __str__(self):
        return self.name
