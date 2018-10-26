from django import forms
from django.conf import settings
from django.core.files.images import get_image_dimensions


class AdImageInlineForm(forms.ModelForm):
    def clean(self):
        super(AdImageInlineForm, self).clean()
        image = self.cleaned_data.get('image', None)
        ad = self.cleaned_data.get('ad', None)


class VenueForm(forms.ModelForm):
    VENUE_GROUPS = (
        ('high', 'High End'),
        ('low', 'Low End'),
    )

    group = forms.ChoiceField(choices=VENUE_GROUPS)
