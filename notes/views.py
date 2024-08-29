from django.shortcuts import render, get_object_or_404, redirect
from .models import Note
from .forms import NoteForm
from django.http import JsonResponse
from django.utils.html import escape
from django.views.decorators.csrf import csrf_exempt
import json

def note_list(request):
    query = request.GET.get('q')
    if query:
        notes = Note.objects.filter(title__icontains=query)
    else:
        notes = Note.objects.all()
    return render(request, 'notes/note_list.html', {'notes': notes})

def highlight_text(text, query):
    """Возвращает текст с выделенным ключевым словом."""
    if not query:
        return text
    query = escape(query)
    text = escape(text)
    highlighted = text.replace(query, f'<mark>{query}</mark>')
    return highlighted

def search_notes(request):
    query = request.GET.get('q', '')
    if query:
        notes = Note.objects.filter(title__icontains=query) | Note.objects.filter(content__icontains=query)
        results = [
            {
                'id': note.id,
                'title': note.title,
                'content': highlight_text(note.content, query)  # Подсвечиваем ключевое слово в содержимом
            } for note in notes
        ]
    else:
        # Если запрос пустой, возвращаем все заметки
        notes = Note.objects.all()
        results = [
            {
                'id': note.id,
                'title': note.title,
                'content': note.content  # Возвращаем все заметки, без подсветки
            } for note in notes
        ]

    return JsonResponse({'results': results})

def note_detail(request, pk):
    note = get_object_or_404(Note, pk=pk)
    return render(request, 'notes/note_detail.html', {'note': note})

@csrf_exempt
def note_create(request, pk=None):
    if request.method == "POST":
        data = json.loads(request.body)
        title = data.get("title", "Untitled")
        content = data.get("content", "")

        if pk:
            # Редактирование существующей заметки
            note = get_object_or_404(Note, pk=pk)
            note.title = title
            note.content = content
            note.save()
        else:
            # Создание новой заметки
            Note.objects.create(title=title, content=content)

        return JsonResponse({"message": "Note saved successfully"})

    # Получение заметки для редактирования (если pk предоставлен)
    note = None
    if pk:
        note = get_object_or_404(Note, pk=pk)

    return render(request, 'notes/note_form.html', {'note': note})

@csrf_exempt
def note_edit(request, pk):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            note = Note.objects.get(pk=pk)
            note.content = data.get('content', note.content)
            note.save()
            return JsonResponse({'status': 'success'})
        except Note.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Note not found'})
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON'})
    else:
        # Обработка GET запроса, если требуется
        note = Note.objects.get(pk=pk)
        form = NoteForm(instance=note)
        return render(request, 'notes/note_form.html', {'form': form})

def note_delete(request, pk):
    note = get_object_or_404(Note, pk=pk)
    if request.method == "POST":
        note.delete()
        return redirect('note_list')
    return render(request, 'notes/note_confirm_delete.html', {'note': note})