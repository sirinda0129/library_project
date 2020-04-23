from django.contrib import admin
from .models import Post, Group


class PostAdmin(admin.ModelAdmin):
    list_display = ("pk", "title", "description", "url", "pub_date", "approved", "language")
    search_fields = ("title", "description")
    list_filter = ("approved", "pub_date", "group")
    empty_value_display = "-пусто-"


class GroupAdmin(admin.ModelAdmin):
    list_display = ("pk", "title", "slug", "description")
    search_fields = ("title",)
    prepopulated_fields = {"slug": ("title",)}


admin.site.register(Post, PostAdmin)
admin.site.register(Group, GroupAdmin)
# Register your models here.
