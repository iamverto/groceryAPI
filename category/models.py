from django.db import models


class Category(models.Model):
    title = models.CharField(max_length=64)
    poster = models.ImageField(upload_to='category/posters')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.title
