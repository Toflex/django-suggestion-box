from django.forms.forms import Form

from suggestionbox.models import Suggestion


class SuggestionBoxSubmitForm(ModelForm):
    class Meta:
        model = Suggestion
        fields = ('message',)

    def __init__(self, *args, **kwargs):
        self.actual_ip = kwargs.pop(ip_address)
        super(SuggestionBoxSubmitForm, self).__init__(*args, **kwargs)

    def save(self, *args, **kwargs):
        suggestion = super(SuggestionBoxSubmitForm, self).save(
            commit=False, *args, **kwargs)
        suggestion.ip_address = self.actual_ip
        suggestion.save(commit=True)
