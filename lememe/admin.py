from django.contrib import admin
from lememe.models import UserProfile, Post, Comment, Preference, Category


# class PageAdmin(admin.ModelAdmin):
#     list_display = ('title', 'category', 'url')

class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'client_id', 'title', 'category', 'user', 'image', 'date')


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'text', 'post', 'user', 'date')


class PreferenceAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'post', 'liked')


admin.site.register(Category, CategoryAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(UserProfile)
admin.site.register(Preference, PreferenceAdmin)
