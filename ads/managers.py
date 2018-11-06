import random

from ads.querysets import AdQuerySet
from django.db.models import Manager, Count


class AdManager(Manager):
    def get_queryset(self):
        return AdQuerySet(self.model)

    def public(self):
        return self.get_queryset().public()

    def random_ad(self, zone, venue_title):
        ads = []
        for ad in self.public().filter(
                venues__title=venue_title, images__zone=zone):
            ads += [ad] * ad.weight
        if not ads:
            return None
        return random.choice(ads)

    def static_ad(self, title, zone):
        ad = self.get_queryset().get(title=title, images__zone=zone)
        return ad
