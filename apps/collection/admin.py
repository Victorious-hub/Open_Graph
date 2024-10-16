from django.contrib import admin

from apps.collection.models import Collection, LinkCollection

admin.site.register(Collection)
admin.site.register(LinkCollection)
