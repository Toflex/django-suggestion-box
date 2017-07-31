from django.forms.models import ModelForm

from suggestionbox.models import Suggestion


class SuggestionBoxSubmitForm(ModelForm):
    class Meta:
        model = Suggestion
        fields = ('message',)
