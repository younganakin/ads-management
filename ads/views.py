from django.http import HttpResponseRedirect
from django.conf import settings
from django.shortcuts import render
from django.views import View
from django.utils import timezone
from django.views.generic.detail import SingleObjectMixin

from ads.models import Ad, Click, Impression
from ads.utils import get_client_ip


class AdClickView(SingleObjectMixin, View):
    def get_queryset(self):
        return Ad.objects.all()

    def get(self, request, *args, **kwargs):
        ad = self.get_object()
        if request.session.session_key:
            click, created = Click.objects.get_or_create(
                ad=ad,
                session_id=request.session.session_key,
                defaults={
                    'click_date': timezone.now(),
                    'source_ip': get_client_ip(request),
                })
        return HttpResponseRedirect(ad.url)


def random_ad(request, zone, group):
    # Retrieve random ad for the zone based on weight
    ad = Ad.objects.random_ad(zone, group)

    if ad is not None:
        if request.session.session_key:
            impression, created = Impression.objects.get_or_create(
                ad=ad,
                session_id=request.session.session_key,
                defaults={
                    'impression_date': timezone.now(),
                    'source_ip': get_client_ip(request),
                })

    context = {
        'ad': ad,
        'zone': settings.ADS_ZONES.get(zone, None)
    }
    return render(request, 'ads/random-ad.html', context)


def static_ad(request, title, zone):
    # Retrieve random ad for the zone based on weight
    ad = Ad.objects.static_ad(title, zone)

    if ad is not None:
        if request.session.session_key:
            impression, created = Impression.objects.get_or_create(
                ad=ad,
                session_id=request.session.session_key,
                defaults={
                    'impression_date': timezone.now(),
                    'source_ip': get_client_ip(request),
                })

    context = {
        'ad': ad,
        'zone': settings.ADS_ZONES.get(zone, None)
    }
    return render(request, 'ads/static-ad.html', context)
