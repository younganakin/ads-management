from __future__ import unicode_literals

from django.core.validators import MinValueValidator
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.encoding import python_2_unicode_compatible, force_text
from django.utils.translation import ugettext_lazy as _

from ads.managers import AdManager


@python_2_unicode_compatible
class Advertiser(models.Model):
    """ A Model for our Advertiser.  """
    company_name = models.CharField(
        verbose_name=_(u'Company Name'), max_length=255)
    website = models.URLField(verbose_name=_(u'Company Site'))
    created_by = models.ForeignKey(
        User, null=True, on_delete=models.SET_NULL,
        verbose_name=_('Created By'))

    class Meta:
        verbose_name = _('Advertiser')
        verbose_name_plural = _('Advertisers')
        ordering = ('company_name',)

    def __str__(self):
        return self.company_name

    def get_website_url(self):
        return self.website


@python_2_unicode_compatible
class Category(models.Model):
    """ a Model to hold the different Categories for adverts """
    title = models.CharField(
        verbose_name=_('Title'), max_length=255)
    description = models.TextField(
        verbose_name=_('Description'), blank=True)
    created_by = models.ForeignKey(
        User, null=True, on_delete=models.SET_NULL,
        verbose_name=_('Created By'))

    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')
        ordering = ('title',)

    def __str__(self):
        return self.title


def now_plus_1_day():
    return timezone.now() + timezone.timedelta(days=1)


@python_2_unicode_compatible
class Venue(models.Model):
    """ a Model to hold the different Venues for splash page adverts """
    title = models.CharField(
        verbose_name=_('Title'), max_length=255)
    location = models.CharField(
        verbose_name=_('Location'), max_length=255)
    group = models.CharField(
        verbose_name=_('Venue Group'), max_length=255, blank=True, null=True)
    created_by = models.ForeignKey(
        User, null=True, on_delete=models.SET_NULL,
        verbose_name=_('Created By'))

    class Meta:
        verbose_name = _('Venue')
        verbose_name_plural = _('Venues')
        ordering = ('title',)

    def __str__(self):
        return self.title


@python_2_unicode_compatible
class Ad(models.Model):
    """
    This is our base model, from which all ads will inherit.
    The manager methods for this model will determine which ads to
    display return etc.
    """
    title = models.CharField(verbose_name=_('Title'), max_length=255)
    url = models.URLField(verbose_name=_('Advertised URL'))
    publication_date = models.DateTimeField(
        verbose_name=_('Start showing'),
        default=timezone.now)
    publication_date_end = models.DateTimeField(
        verbose_name=_('Stop showing'),
        default=now_plus_1_day)

    # Relations
    advertiser = models.ForeignKey(
        Advertiser, on_delete=models.CASCADE, verbose_name=_("Ad Provider"))
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE,
        verbose_name=_("Category"), blank=True, null=True)
    venues = models.ManyToManyField(
        Venue,
        verbose_name=_("Venues"))
    zone = models.CharField(
        verbose_name=_('Zone'), max_length=100)
    weight = models.IntegerField(
        verbose_name=_('Weight'),
        help_text=_('Weight of the ad relative to other ads '
                    'in the same zone.<br />'
                    'Ad with higher weight will be '
                    'displayed more frequently.'),
        default=1,
        validators=[MinValueValidator(1)])
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        User, null=True, on_delete=models.SET_NULL,
        verbose_name=_('Created By'))

    objects = AdManager()

    class Meta:
        verbose_name = _('Ad')
        verbose_name_plural = _('Ads')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('ads:ad-click', kwargs={
            'pk': self.id})


@python_2_unicode_compatible
class AdImage(models.Model):
    ad = models.ForeignKey(
        Ad,
        on_delete=models.CASCADE,
        verbose_name=_('Ad'),
        related_name='images')
    image = models.ImageField(
        upload_to='ad-images',
        verbose_name=_('Image'),
        max_length=255)
