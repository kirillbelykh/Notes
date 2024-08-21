from django.test import TestCase
from .models import Note
from django.core.management import call_command
from django.urls import reverse
from .forms import NoteForm

class NoteModelTest(TestCase):
    def setUp(self):
        Note.objects.create(title="Test Note", content="This is a test note")

    def test_note_content(self):
        note = Note.objects.get(title="Test Note")
        self.assertEqual(note.content, "This is a test note")

class NoteViewTest(TestCase):
    def setUp(self):
        self.note = Note.objects.create(title="Test Note", content="This is a test note")

    def test_note_list_view(self):
        response = self.client.get(reverse('note_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Note")

    def test_note_detail_view(self):
        response = self.client.get(reverse('note_detail', kwargs={'pk': self.note.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "This is a test note")

class NoteFormTest(TestCase):
    def test_valid_form(self):
        data = {'title': 'Test Note', 'content': 'This is a test note'}
        form = NoteForm(data=data)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        data = {'title': '', 'content': 'This is a test note'}
        form = NoteForm(data=data)
        self.assertFalse(form.is_valid())