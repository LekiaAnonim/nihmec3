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
from wagtail.contrib.routable_page.models import RoutablePageMixin, path
# from paystack.resource import TransactionResource
from django.conf import settings
import random
import string
import os

from datetime import date
from django.core.mail import send_mail
# from django.core.mail import EmailMessage
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
# from wagtail.admin.mail import send_mail


from registration.resource import TransactionResource
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

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)

        return context

    def process_form_submission(self, form):
        

        return self.get_submission_class().objects.create(
            form_data=form.cleaned_data,
            page=self
        )

    def serve(self, request, *args, **kwargs):
        if request.method == 'POST':
            form = self.get_form(request.POST, page=self)

            if form.is_valid():
                self.process_form_submission(form)


                addresses = [x.strip() for x in self.to_address.split(',')]
                

                # Subject can be adjusted (adding submitted date), be sure to include the form's defined subject field
                submitted_date_str = date.today().strftime('%x')
                subject = f"{self.subject} - {submitted_date_str}"

                
                # Update the original landing page context with other data
                context = self.get_context(request)

                text_content  = '\n' + '\n' + 'Hi,' + '\t' + str(form.cleaned_data['first_name']) + '\n' + '\n' +'\n'
                html_content = render_to_string('registration/email_header.html', context, request=request)+text_content+render_to_string('registration/registration_email_template.html', context, request=request)

                msg = EmailMultiAlternatives(subject, text_content, self.from_address, [address for address in addresses]+[form.cleaned_data['email_address']])
                # msg.content_subtype = "html"  # Main content is now text/html
                msg.attach_alternative(html_content, "text/html")
                msg.send()
                rand = ''.join(
                [random.choice(
                    string.ascii_letters + string.digits) for n in range(16)])
                # secret_key = os.getenv('PAYSTACK_SECRET_KEY')
                secret_key = 'sk_live_41506a1dec474fb59359be2f05dc354d0c64d429'
                random_ref = rand
                test_email = form.cleaned_data['email_address']
                test_amount = str(form.cleaned_data['total_cost']*100)
                plan = 'Basic'
                client = TransactionResource(secret_key, random_ref)
                response = client.initialize(test_amount,
                                            test_email)
                client.authorize() # Will open a browser window for client to enter card details
                # print(client.authorize())
                client.verify() # Verify client credentials
                # client.charge() # Charge an already exsiting client
                
                landing_page_context = self.get_context(request, *args, **kwargs)
                auth_url = client.authorize()
                
                landing_page_context['auth_url'] = client.authorize()
                landing_page_context['first_name'] = form.cleaned_data['first_name']
                landing_page_context['surname'] = form.cleaned_data['surname']
                landing_page_context['total_cost'] = form.cleaned_data['total_cost']
                landing_page_context['email_address'] = form.cleaned_data['email_address']
                landing_page_context['workshop'] = form.cleaned_data['workshop']
                landing_page_context['number_of_registrants'] = form.cleaned_data['number_of_registrants']
                landing_page_context["home_page"] = self.home_page

                return render(
                    request,
                    self.get_landing_page_template(request),
                    landing_page_context
                )
        else:
            form = self.get_form(page=self)

        context = self.get_context(request)
        context['form'] = form
        context["home_page"] = self.home_page
        return render(
            request,
            self.get_template(request),
            context
        )

    # def send_mail(self, form):
    #     # `self` is the FormPage, `form` is the form's POST data on submit

    #     # Email addresses are parsed from the FormPage's addresses field
    #     addresses = [x.strip() for x in self.to_address.split(',')]
    #     print(addresses)
    #     print(form.cleaned_data['email_address'])

    #     # Subject can be adjusted (adding submitted date), be sure to include the form's defined subject field
    #     submitted_date_str = date.today().strftime('%x')
    #     subject = f"{self.subject} - {submitted_date_str}"

    #     send_mail(subject, self.render_email(form), [addresses, form.cleaned_data['email_address']], self.from_address, fail_silently=False)