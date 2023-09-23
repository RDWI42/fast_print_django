from django.contrib import admin

from .models import Product, Status

admin.site.register(Product)
admin.site.register(Status)