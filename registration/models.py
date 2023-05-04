from django.db import models
from wagtail.models import Page, Orderable
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel, InlinePanel, FieldRowPanel, MultiFieldPanel
from wagtail.snippets.models import register_snippet
from modelcluster.fields import ParentalKey, ParentalManyToManyField
from modelcluster.models import ClusterableModel
from django.utils.functional import cached_property
from wagtail.contrib.forms.panels import FormSubmissionsPanel
from wagtail.contrib.forms.models import AbstractEmailForm, AbstractFormField
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render
from paystack.resource import TransactionResource

import random
import string
import os

import environ
env = environ.Env()
environ.Env.read_env()
# Create your models here.

# @register_snippet
# class Registration(models.Model):
#     registration_package = models.ForeignKey(RegistrationPackage, on_delete=models.SET_NULL, related_name='registration_package', null=True)
#     first_name = models.CharField(max_length = 500, null=True, blank=True)
#     surname = models.CharField(max_length=500, null=True, blank=True)
#     SEX_CHOICES =( 
#         ('Male', 'Male'),
#         ('Female', 'Female'),
#     )
#     sex = models.CharField(max_length=20, null=True, choices=SEX_CHOICES)
#     company = models.CharField(max_length=500, null=True)
#     position = models.CharField(max_length=500, null=True, blank=True)
#     email = models.EmailField(null=True)
#     phone = models.CharField(max_length=20)
#     city = models.CharField(max_length=500, null=True, blank=True)
#     state = models.CharField(max_length=500, null=True)
#     country = models.CharField(max_length=500, null=True, blank=True)

#     number_of_registrants = models.IntegerField(null=True, blank=True, default=1)

#     panels = [
#         FieldPanel('registration_package'),
#         FieldPanel('first_name'),
#         FieldPanel('surname'),
#         FieldPanel('sex'),
#         FieldPanel('company'),
#         FieldPanel('position'),
#         FieldPanel('email'),
#         FieldPanel('phone'),
#         FieldPanel('city'),
#         FieldPanel('state'),
#         FieldPanel('country'),
#         FieldPanel('number_of_registrants'),
#     ]

class RegistrationPage(Page):
    template = 'registration/registration.html'




class FormField(AbstractFormField):
    page = ParentalKey('RegistrationFormPage', on_delete=models.CASCADE, related_name='form_fields')


class RegistrationFormPage(AbstractEmailForm):
    template = 'registration/registration.html'
    intro = RichTextField(blank=True)
    thank_you_text = RichTextField(blank=True)

    content_panels = AbstractEmailForm.content_panels + [
        FormSubmissionsPanel(),
        FieldPanel('intro'),
        # FieldPanel('registration_package'),
        InlinePanel('form_fields', label="Form fields"),
        FieldPanel('thank_you_text'),
        MultiFieldPanel([
            FieldRowPanel([
                FieldPanel('from_address', classname="col6"),
                FieldPanel('to_address', classname="col6"),
            ]),
            FieldPanel('subject'),
        ], "Email"),
    ]

    @cached_property
    def home_page(self):
        return self.get_parent().specific

    def get_context(self, request, *args, **kwargs):
        context = super(RegistrationFormPage, self).get_context(request, *args, **kwargs)
        context["home_page"] = self.home_page
        return context

    def get_form_fields(self):
        
        return self.form_fields.all()

    def process_form_submission(self, form):
        print(form.cleaned_data)
        rand = ''.join(
        [random.choice(
            string.ascii_letters + string.digits) for n in range(16)])
        secret_key = os.getenv('PAYSTACK_SECRET_KEY')
        
        random_ref = rand
        test_email = form.cleaned_data['email_address']
        test_amount = str(form.cleaned_data['total_cost'])
        plan = 'Basic'
        client = TransactionResource(secret_key, random_ref)
        response = client.initialize(test_amount,
                                    test_email)
        print(response)
        client.authorize() # Will open a browser window for client to enter card details
        verify = client.verify() # Verify client credentials
        print(verify)
        print(client.charge()) # Charge an already exsiting client
        return self.get_submission_class().objects.create(
            form_data=form.cleaned_data,
            page=self
        )

    