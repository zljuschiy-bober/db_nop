from django import forms
from django.contrib.auth.forms import UserChangeForm, User
from .models import Regions, Firms, Security_object, Category


class RegionForm(forms.ModelForm):
    class Meta:
        model = Regions
        fields = ('name', 'director', 'telephone')


class FirmForm(forms.ModelForm):
    class Meta:
        model = Firms
        fields = ('name', 'director', 'yur_address', 'fiz_address', 'telephone1',
                  'telephone2', 'dogovor', 'dogovor_file')


class UserProfileForm(UserChangeForm):
    class Meta:
        model = User
        exclude = ('password', 'user_permissions', 'groups', 'is_superuser',
                   'is_staff', 'date_joined', 'is_active')


class AddObjectForm(forms.ModelForm):
    class Meta:
        model = Security_object
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
                                             queryset=Category.objects.all(),
                                             widget=forms.Select())

    object_firm = forms.ModelChoiceField(required=False,
                                         label="Виберіть назву фірми",
                                         queryset=Firms.objects.all(),
                                         widget=forms.Select())
    object_rayon = forms.ModelChoiceField(required=False,
                                          label="Виберіть район",
                                          queryset=Regions.objects.all(),
                                          widget=forms.Select())
