from django.contrib import admin
from .models import *


# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'price', 'time_create')
    list_display_links = ('id', 'title')
    search_fields = ('title', 'content')
    list_filter = ('time_create',)

    prepopulated_fields = {"slug": ("title",)}


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('name',)
    prepopulated_fields = {"slug": ("name",)}


admin.site.register(Product, ProductAdmin)

admin.site.register(Category, CategoryAdmin)
