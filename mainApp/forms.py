from django import forms
from django.contrib.auth.forms import UserChangeForm, User
from .models import regions, firms, security_object, category, dogovor


class RegionForm(forms.ModelForm):
    class Meta:
        model = regions
        fields = ('name', 'director', 'telephone')


class FirmForm(forms.ModelForm):
    class Meta:
        model = firms
        fields = ('name', 'director', 'yur_address', 'fiz_address', 'telephone1',
                  'telephone2')


class UserProfileForm(UserChangeForm):
    class Meta:
        model = User
        exclude = ('password', 'user_permissions', 'groups', 'is_superuser',
                   'is_staff', 'date_joined', 'is_active')


class AddObjectForm(forms.ModelForm):
    class Meta:
        model = security_object
        fields = ('name', 'region', 'firm', 'address', 'dogovor', 'document',
                  'state', 'category')


class SearchObjectForm(forms.Form):
    object_name = forms.CharField(required=False,
                                  label="Назва:",
                                  max_length=50)

    object_address = forms.CharField(required=False,
                                     label="Адреса:",
                                     max_length=50)

    object_category = forms.ModelChoiceField(required=False,
                                             label="Виберіть категорію",
                                             queryset=category.objects.all().order_by('name'),
                                             widget=forms.Select())

    object_firm = forms.ModelChoiceField(required=False,
                                         label="Виберіть назву фірми",
                                         queryset=firms.objects.all().order_by('name'),
                                         widget=forms.Select())
    object_region = forms.ModelChoiceField(required=False,
                                          label="Виберіть район",
                                          queryset=regions.objects.all().order_by('name'),
                                          widget=forms.Select())

class AddDocumentForm(forms.ModelForm):
    class Meta:
        model = dogovor
        fields = ('firm', 'name', 'state',  'date_start', 'date_finish', 'dogovor_file')
