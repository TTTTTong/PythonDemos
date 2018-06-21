from django.contrib import admin
from . import models
from django.contrib.sites.models import Site


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'create_time', 'modified_time')  # Post列表页面显示的参数
    fields = ('title', 'body', 'excerpt', 'category', 'tags')  # 可编辑的参数列表


# 重写site，使admin页面显示SITE_ID
admin.site.unregister(Site)


class SiteAdmin(admin.ModelAdmin):
    fields = ('id', 'name', 'domain')
    readonly_fields = ('id',)
    list_display = ('id', 'name', 'domain')
    list_display_links = ('name',)
    search_fields = ('name', 'domain')


admin.site.register(Site, SiteAdmin)
admin.site.register(models.Category)
admin.site.register(models.Tag)
admin.site.register(models.Post, PostAdmin)


