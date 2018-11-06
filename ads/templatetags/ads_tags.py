from __future__ import unicode_literals

from django import template
from django.conf import settings
from django.utils import timezone

from ads.models import Ad, Impression
from ads.utils import get_client_ip


register = template.Library()


@register.inclusion_tag('ads/tags/render_ads_zone.html', takes_context=True)
def render_ads_zone(context, zone, venue_title):
    """
    Returns an advertise for a ``zone``.
    Tag usage:
    {% load ads_tags %}
    {% render_zone 'zone' %}
    """

    # Retrieve random ad for the zone based on weight
    ad = Ad.objects.random_ad(zone, venue_title)

    if ad is not None:
        request = context['request']
        if request.session.session_key:
            impression, created = Impression.objects.get_or_create(
                ad=ad,
                session_id=request.session.session_key,
                defaults={
                    'impression_date': timezone.now(),
                    'source_ip': get_client_ip(request),
                })
    context.update({
        'ad': ad,
        'zone': settings.ADS_ZONES.get(zone, None)
    })
    return context


@register.inclusion_tag('ads/tags/render_static_zone.html', takes_context=True)
def render_static_zone(context, title, zone):
    # Retrieve static ad for the zone based on weight and ad title
    ad = Ad.objects.static_ad(title, zone)

    if ad is not None:
        request = context['request']
        if request.session.session_key:
            impression, created = Impression.objects.get_or_create(
                ad=ad,
                session_id=request.session.session_key,
                defaults={
                    'impression_date': timezone.now(),
                    'source_ip': get_client_ip(request),
                })
    context.update({
        'ad': ad,
        'zone': settings.ADS_ZONES.get(zone, None)
    })
    return context
