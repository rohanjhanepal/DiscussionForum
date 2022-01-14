from django.contrib import admin
from django.contrib.auth.models import Group
from . import models

admin.site.header = 'Discussion App Admin'
admin.site.site_title = 'Discussion App Admin'

admin.site.unregister(Group)

admin.site.register(models.Category)
admin.site.register(models.SubCategory)
admin.site.register(models.Post)
admin.site.register(models.Tag)
admin.site.register(models.Answer)
admin.site.register(models.Upvote)

