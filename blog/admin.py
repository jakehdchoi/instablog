from django.contrib import admin
from .models import *


class CommentInlineAdmin(admin.StackedInline):
    model = Comment
    extra = 1


class PostAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title','created_at','category',)
    list_display_links = ('pk', 'title',)
    ordering = ('-id',)
    inlines = [CommentInlineAdmin]
    search_fields = ('title', 'content',)
    list_filter = ('title', 'created_at', 'category',)
    date_hierarchy = 'created_at' # 날짜를 다루기 때문에 pytz를 설치해야 한다. (에러가 뜰 경우: pip install pytz)


admin.site.register(Post, PostAdmin)
admin.site.register(Comment)
admin.site.register(Tag)
admin.site.register(Category)
