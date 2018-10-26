from __future__ import unicode_literals

from django import forms
from django.contrib import admin

from ads.forms import *
from ads.models import *
from ads.utils import get_zones_choices

# Register your models here.


class AdvertiserAdmin(admin.ModelAdmin):
    search_fields = ['company_name', 'website']
    list_display = ['company_name', 'website', 'created_by']
    raw_id_fields = ['created_by']

    def get_changeform_initial_data(self, request):
        """
        Provide initial datas when creating an advertiser.
        """
        get_data = super(
            AdvertiserAdmin, self).get_changeform_initial_data(request)
        return get_data or {
            'created_by': request.user.pk
        }


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_by']
    raw_id_fields = ['created_by']

    def get_changeform_initial_data(self, request):
        """
        Provide initial datas when creating a category.
        """
        get_data = super(CategoryAdmin, self). \
            get_changeform_initial_data(request)
        return get_data or {
            'created_by': request.user.pk
        }


class VenueAdmin(admin.ModelAdmin):
    form = VenueForm
    list_display = ['title', 'location', 'group', 'created_by']
    raw_id_fields = ['created_by']

    def get_changeform_initial_data(self, request):
        """
        Provide initial datas when creating a category.
        """
        get_data = super(VenueAdmin, self). \
            get_changeform_initial_data(request)
        return get_data or {
            'created_by': request.user.pk
        }


class AdAdminForm(forms.ModelForm):
    class Meta:
        exclude = ('venues',)
        widgets = {
            'zone': forms.Select(choices=get_zones_choices())
        }


class AdImageInline(admin.TabularInline):
    model = AdImage
    form = AdImageInlineForm
    fields = ('image',)


class VenueInline(admin.TabularInline):
    model = Ad.venues.through


class AdAdmin(admin.ModelAdmin):
    form = AdAdminForm
    list_display = [
        'title', 'url', 'zone', 'advertiser', 'weight',
        'publication_date', 'publication_date_end']
    list_filter = [
        'publication_date', 'publication_date_end',
        'created_at', 'modified_at']
    search_fields = ['title', 'url']
    raw_id_fields = ['advertiser', 'created_by']
    inlines = (AdImageInline, VenueInline, )

    def get_changeform_initial_data(self, request):
        """
        Provide initial datas when creating an Ad.
        """
        get_data = super(AdAdmin, self).get_changeform_initial_data(request)
        return get_data or {
            'created_by': request.user.pk
        }


admin.site.register(Advertiser, AdvertiserAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Venue, VenueAdmin)
admin.site.register(Ad, AdAdmin)
