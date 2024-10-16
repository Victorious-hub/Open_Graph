from django.db import models

from apps.users.models import UserAccount


class Link(models.Model):
    class LinkType(models.TextChoices):
        WEBSITE = "website", "Website"
        BOOK = "book", "Book"
        ARTICLE = "article", "Article"
        MUSIC = "music", "Music"
        VIDEO = "video", "Video"

    link_url = models.URLField(max_length=255, null=True)
    title = models.CharField(max_length=255, null=True)
    description = models.TextField(null=True)
    image = models.URLField(max_length=255, blank=True, null=True)
    link_type = models.CharField(
        max_length=50, choices=LinkType.choices, default=LinkType.WEBSITE
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"Link: {self.link_url}"

    class Meta:
        verbose_name = "link"
        verbose_name_plural = "links"
