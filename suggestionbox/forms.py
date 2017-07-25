from django.forms.forms import Form

from suggestionbox.models import Suggestion


class SuggestionBoxSubmitForm(ModelForm):
    class Meta:
        model = Suggestion
        fields = ('message',)
