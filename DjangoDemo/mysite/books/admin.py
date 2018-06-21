from django.contrib import admin
from . import models
# Register your models here.


class PublisherAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'city', 'state_provice', 'country', 'website')


class AuthorAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email')
    search_fields = ('first_name', 'last_name')


class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'publisher', 'publication_date')
    list_filter = ('publication_date', )  # 列表右边的日期过滤框
    date_hierarchy = 'publication_date'   # 列表顶端的导航条,仅接受字符串
    ordering = ('-publication_date', )
    fields = ('title', 'authors', 'publisher', 'publication_date')  # 编辑model时显示的字段和顺序
    filter_horizontal = ('authors', )  # 一个js过滤器，显示一个多选框添加和删除多对多的model
    raw_id_fields = ('publisher', )  # 因为外键是ID，将下拉框改为点击放大镜可以model的弹窗


admin.site.register(models.Publisher, PublisherAdmin)
admin.site.register(models.Author, AuthorAdmin)
admin.site.register(models.Book, BookAdmin)
