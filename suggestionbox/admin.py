from django import http
from django.contrib import admin

from suggestionbox.models import Suggestion


class SuggestionAdmin(admin.ModelAdmin):
    list_display = ('created', 'ip_address', 'read', 'deleted')
    readonly_fields=('created',)


class SuggestionRaw(Suggestion):
    class Meta:
        proxy = True


class SuggestionInbox(admin.ModelAdmin):
    list_display = ('created', 'ip_address', 'message_start')
    readonly_fields=('created', 'ip_address', 'message')

    def get_queryset(self, request):
        return Suggestion.objects.filter(read=False)

    def response_change(self, request, obj):
        inbox = self.get_queryset(request)
        if inbox.exists():
            return http.HttpResponseRedirect(inbox[0].get_admin_url())
        else:
            return http.HttpResponseRedirect(Suggestion.objects.get_admin_url())


admin.site.register(Suggestion, SuggestionInbox)
admin.site.register(SuggestionRaw, SuggestionAdmin)
