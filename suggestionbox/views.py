from django.views.generic.edit import FormView, UpdateView

from suggestionbox.forms import SuggestionBoxSubmitForm
from suggestionbox.models import Suggestion


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR', None)
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[-1]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


class EditSuggestionView(UpdateView):
    form_class = SuggestionBoxSubmitForm
    model = Suggestion
#    success_url = '/feedback'
#    template_name = 'feedback.html'

    def get_object(self):
        self.ip_address = get_client_ip(self.request)
        return Suggestion.objects.get_unread(self.ip_address)
