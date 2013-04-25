from django.contrib import admin
from core.models import Pasty

class PastyAdmin(admin.ModelAdmin):
    list_display = ('date', 'source', 'short_text', 'votes')
    list_filter = ('date', 'source')
    search_fields = ['text']
    date_hierarchy = 'date'
    fields = ('date', 'source', 'text', 'votes')

admin.site.register(Pasty, PastyAdmin)
