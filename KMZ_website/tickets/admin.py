from django.contrib import admin
from .models import Event, Seat


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'date', 'venue', 'price')  # Заменено 'location' на 'venue'
    list_filter = ('date', 'venue')  # Заменено 'location' на 'venue'
    search_fields = ('name', 'description', 'venue')  # Добавлено 'venue' в поиск

    fieldsets = (
        (None, {
            'fields': ('name', 'description', 'image')
        }),
        ('Event Details', {
            'fields': ('date', 'time', 'venue', 'price')
        }),
    )


@admin.register(Seat)
class SeatAdmin(admin.ModelAdmin):
    list_display = ('event', 'row', 'number', 'price', 'is_reserved', 'is_purchased')
    list_filter = ('event', 'is_reserved', 'is_purchased')
    search_fields = ('event__name', 'row', 'number')
