from django.db import models

from apps.links.models import Link
from apps.users.models import UserAccount


class Collection(models.Model):
    name = models.CharField(max_length=255, null=False)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"Collection: {self.name}"

    class Meta:
        verbose_name = "collection"
        verbose_name_plural = "collections"

class LinkCollection(models.Model):
    link = models.ForeignKey(Link, on_delete=models.CASCADE)
    collection = models.ForeignKey(Collection, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"LinkCollection: {self.link} - {self.collection}"

    class Meta:
        unique_together = ('link', 'collection')
        verbose_name = "link collection"
        verbose_name_plural = "link collections"
