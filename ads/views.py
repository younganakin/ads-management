from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import View
from django.views.generic.detail import SingleObjectMixin

from ads.models import Ad


class AdClickView(SingleObjectMixin, View):
    def get_queryset(self):
        return Ad.objects.all()

    def get(self, request, *args, **kwargs):
        ad = self.get_object()
        return HttpResponseRedirect(ad.url)


def random_ad(request, zone, group):
    # Retrieve random ad for the zone based on weight
    ad = Ad.objects.random_ad(zone, group)
    context = {
        'ad': ad,
    }
    return render(request, 'ads/random-ad.html', context)


def static_ad(request, title, zone):
    # Retrieve random ad for the zone based on weight
    ad = Ad.objects.static_ad(title, zone)
    context = {
        'ad': ad,
    }
    return render(request, 'ads/static-ad.html', context)
