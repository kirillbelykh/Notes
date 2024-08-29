from django.contrib import admin
from .models import Note

@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'updated_at')  # Поля, отображаемые в списке
    search_fields = ('title', 'content')  # Поля для поиска