from django.contrib import admin
from django.contrib.admin import ModelAdmin
from .models import Shouhin,Size


class A_shouhin(ModelAdmin):
    model=Shouhin
    list_display=["team","shouhin_num","shouhin_name","color","size","size_num","tana","joutai"]

class A_size(ModelAdmin):
    model=Size
    list_display=["size_num","size"]


admin.site.register(Shouhin,A_shouhin)
admin.site.register(Size,A_size)