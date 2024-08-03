from django import forms
from django.utils.translation import gettext_lazy as _

from wagtail.users.forms import UserEditForm, UserCreationForm
from registration.models import Attendant


class AttendantForm(forms.ModelForm):
    class Meta:
        model = Attendant
        fields =("first_name", "last_name", "email", "company", "position","country", "phone")


class CustomUserEditForm(UserEditForm):
    country = forms.CharField(required=True, label=_("Country"))
    position = forms.CharField(required=True, label=_("Position"))
    phone = forms.CharField(required=True, label=_("Phone"))
    company = forms.CharField(required=True, label=_("Company"))

    class Meta(UserEditForm.Meta):
        fields = UserEditForm.Meta.fields | {"country", 'company', 'phone', 'position'}


class CustomUserCreationForm(UserCreationForm):
    country = forms.CharField(required=True, label=_("Country"))
    position = forms.CharField(required=True, label=_("Position"))
    phone = forms.CharField(required=True, label=_("Phone"))
    company = forms.CharField(required=True, label=_("Company"))

    class Meta(UserCreationForm.Meta):
        fields = UserEditForm.Meta.fields | {"country", 'company', 'phone', 'position'}