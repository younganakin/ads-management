from django import forms
from django.conf import settings
from django.core.files.images import get_image_dimensions
from django.utils.translation import ugettext as _


class AdImageInlineForm(forms.ModelForm):

    def clean(self):
        super(AdImageInlineForm, self).clean()
        device = self.cleaned_data.get('device', None)
        zone = self.cleaned_data.get('zone', None)
        image = self.cleaned_data.get('image', None)
        ad = self.cleaned_data.get('ad', None)
        if image and device and zone:
            allowed_size = settings.ADS_ZONES.get(zone, {}). \
                get('ad_size', {}). \
                get(device, settings.ADS_DEFAULT_AD_SIZE)
            allowed_w, allowed_h = [int(d) for d in allowed_size.split('x')]
            w, h = get_image_dimensions(image)
            if w != allowed_w or h != allowed_h:
                self.add_error(
                    'image', _('Image size must be %(size)s') % {
                        'size': allowed_size, })


class VenueForm(forms.ModelForm):
    VENUE_GROUPS = (
        ('high', 'High End'),
        ('low', 'Low End'),
    )

    group = forms.ChoiceField(choices=VENUE_GROUPS)
