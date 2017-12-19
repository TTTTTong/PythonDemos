from django.contrib import admin
from . import models


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'create_time', 'modified_time')  # Post列表页面显示的参数
    fields = ('title', 'body', 'excerpt', 'category', 'tags', 'author')  # 可编辑的参数列表


admin.site.register(models.Category)
admin.site.register(models.Tag)
admin.site.register(models.Post, PostAdmin)
