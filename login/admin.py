from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User
from content.models import Content, Comment

# Register your models here.
class ContentInline(admin.StackedInline):
    model = Content
    can_delete = False
    verbose_name = 'content'

class CommentInline(admin.StackedInline):
    model = Comment
    can_delete = False
    verbose_name = 'comment'

class UserAdmin(BaseUserAdmin):
    inlines = (ContentInline, CommentInline)

#admin.site.unregister(User) # 관리자 페이지에 등록된 모델 해제
admin.site.register(User, UserAdmin)

