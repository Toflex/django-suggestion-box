from django.core.exceptions import ValidationError
from django.test import TestCase
from django.test.client import RequestFactory
import mox

from models import Box, Suggestion
from views import EditSuggestionView
import views


class ModelTests(TestCase):

    def setUp(self):
        self.ip = '127.0.0.1'
        Suggestion.objects.create(ip_address='10.10.10.10')

    def test_suggestion_unicode(self):
        mod = Suggestion(ip_address=self.ip)
        self.assertTrue(self.ip in '%s' % mod)

    def test_suggestion_property(self):
        mod = Suggestion(ip_address=self.ip, message='x'*90)
        self.assertTrue(mod.message_start, 'x'*80)

    def test_suggestion_unread_filter(self):
        new = Suggestion.objects.get_or_create(ip_address=self.ip)[0]
        Suggestion.objects.create(ip_address=self.ip, read=True)
        self.assertEqual(Suggestion.objects.get_unread(self.ip).id, new.id)

    def test_suggestion_unread_filter_empty(self):
        Suggestion.objects.create(ip_address=self.ip, read=True)
        self.assertEqual(Suggestion.objects.get_unread(self.ip).id, None)

    def test_suggestion_clean_delete(self):
        new = Suggestion.objects.get_or_create(ip_address=self.ip)[0]
        new.deleted = True
        self.assertFalse(new.read)
        new.clean()
        self.assertTrue(new.read)

    def test_suggestion_clean_raise(self):
        Suggestion.objects.create(ip_address=self.ip)
        mod = Suggestion(ip_address=self.ip)
        self.assertRaises(ValidationError, mod.clean)


class ViewTests(TestCase):

    def setUp(self):
        self.ip = '127.0.0.1'
        Suggestion.objects.create(ip_address='10.10.10.10')
        self.moxx = mox.Mox()

    def tearDown(self):
        self.moxx.UnsetStubs()

    def test_edit_get_objet(self):
        view = EditSuggestionView()
        request = RequestFactory()
        view.request = request
        self.moxx.StubOutWithMock(views, 'get_client_ip')
        views.get_client_ip(request).AndReturn(self.ip)
        self.moxx.StubOutWithMock(Box, 'get_unread')
        Box.get_unread(self.ip).AndReturn(Suggestion(ip_address=self.ip))

        self.moxx.ReplayAll()
        view.get_object()
        self.moxx.VerifyAll()
