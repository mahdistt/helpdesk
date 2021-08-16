from django.contrib import admin

# Register your models here.

class History(admin.ModelAdmin):
    list_display = (
        'replay_message',)
