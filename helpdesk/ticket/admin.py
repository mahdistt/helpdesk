from django.contrib import admin

# Register your models here.
from ticket import models


@admin.register(models.Category)
class RelatedProduct(admin.ModelAdmin):
    list_display = (
        'category_name',
    )


@admin.register(models.Query)
class RelatedProduct(admin.ModelAdmin):
    list_display = (
        'pk',
        'subject',
        'message',
        'message',
        'status',
        'create_info',
        'user_related',
        'category_related',
    )
    list_display_links = (
        'pk',
    )


@admin.register(models.Replay)
class RelatedProduct(admin.ModelAdmin):
    list_display = (
        'replay_message',
        'query_related',
        'operator_related',

    )

    # list_display_links = (
    #     'pk',
    # )
