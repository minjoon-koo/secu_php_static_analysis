from django.contrib import admin
from .models import Tiket

# Register your models here.

#admin.site.register(Tiket)

class TiketAdmin(admin.ModelAdmin):
    search_fields = ['subject']

admin.site.register(Tiket, TiketAdmin)