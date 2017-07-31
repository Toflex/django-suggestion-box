from django.views.generic.edit import FormView, UpdateView

from suggestionbox.forms import SuggestionBoxSubmitForm
from suggestionbox.models import Suggestion


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[-1]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


class CreateSuggestionView(UpdateView):
    form_class = SuggestionBoxSubmitForm

    def get_initial(self):
        self.ip_address = get_client_ip(self.request)
        return Suggestion.get_unread(ip_address)

    def form_valid(self, form):
        user = form.save()
        user = utils.authenticate_without_password(user)
        auth.login(self.request, user)
        return super(CreateUserView, self).form_valid(form)
