from django.contrib import admin

from django.contrib import admin
from User.models import *


class UserAdmin(admin.ModelAdmin):
    # 使用 list_display 定义管理系统显示的数据表列
    list_display = ('id', 'name', 'email', 'password', 'portrait', 'identity')


admin.site.register(User, UserAdmin)
