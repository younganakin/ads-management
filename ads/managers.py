import random

from ads.querysets import AdQuerySet
from django.db.models import Manager, Count


class AdManager(Manager):
    def get_queryset(self):
        return AdQuerySet(self.model)

    def public(self):
        return self.get_queryset().public()

    def zone_ads(self, zone):
        return self.get_queryset().zone_ads(zone)

    def random_ad(self, zone, group):
        ads = []
        for ad in self.zone_ads(zone).public().filter(venues__group=group):
            ads += [ad] * ad.weight
        if not ads:
            return None
        return random.choice(ads)

    def static_ad(self, title, zone):
        ad = self.get_queryset().get(title=title, zone=zone)
        return ad
