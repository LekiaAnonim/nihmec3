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
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    company = models.CharField(verbose_name='company', max_length=255, blank=True)
    position = models.CharField(verbose_name='position', max_length=255, blank=True)
    country = models.CharField(verbose_name='country', max_length=255, blank=True)
    phone = models.CharField(verbose_name='phone', max_length=255, blank=True)

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
                landing_page_context = self.get_context(request, *args, **kwargs)
                currency = form.cleaned_data['currency']
                if currency == 'Naira(NGN)':
                    test_email = form.cleaned_data['email_address']
                    test_amount = str(form.cleaned_data['total_cost']*100)
                    plan = 'Basic'
                    client = TransactionResource(secret_key, random_ref)
                    response = client.initialize(test_amount,
                                                test_email)
                        

                    client.authorize() # Will open a browser window for client to enter card details
                    # print(client.authorize())
                    client.verify() # Verify client credentials
                    landing_page_context['auth_url'] = client.authorize()
                    # client.charge() # Charge an already exsiting client
                
                # auth_url = client.authorize()
                
                
                landing_page_context['first_name'] = form.cleaned_data['first_name']
                landing_page_context['surname'] = form.cleaned_data['surname']
                landing_page_context['total_cost'] = form.cleaned_data['total_cost']
                landing_page_context['email_address'] = form.cleaned_data['email_address']
                landing_page_context['workshop'] = form.cleaned_data['workshop']
                landing_page_context['currency'] = form.cleaned_data['currency']
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
    


class VisitorRegistrationPage(Page):
    template = 'registration/visitor_registration.html'


class VisitorFormField(AbstractFormField):
    page = ParentalKey('VisitorRegistrationFormPage', on_delete=models.CASCADE, related_name='form_fields')

class VisitorRegistrationFormPage(AbstractEmailForm):
    template = 'registration/visitor_registration.html'
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
        context = super(VisitorRegistrationFormPage, self).get_context(request, *args, **kwargs)
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

                contact = {
                    'First name': form.cleaned_data['first_name'],
                    'Surname': form.cleaned_data['surname'],
                    'Company': form.cleaned_data['company'],
                    'Position': form.cleaned_data['position'],
                }
                context['first_name'] = form.cleaned_data['first_name']
                context['surname'] = form.cleaned_data['surname']
                context['company'] = form.cleaned_data['company']
                context['position'] = form.cleaned_data['position']
                context['contact'] = form.cleaned_data['contact']

                text_content  = '\n' + '\n' + 'Hi,' + '\t' + str(form.cleaned_data['first_name']) + '\n' + '\n' +'\n'
                html_content = render_to_string('registration/email_header.html', context, request=request)+text_content+render_to_string('registration/registration_email_template.html', context, request=request)

                msg = EmailMultiAlternatives(subject, text_content, self.from_address, [address for address in addresses]+[form.cleaned_data['email_address']])
                # msg.content_subtype = "html"  # Main content is now text/html
                msg.attach_alternative(html_content, "text/html")
                msg.send()
                
                landing_page_context = self.get_context(request, *args, **kwargs)
                
                
                landing_page_context['first_name'] = form.cleaned_data['first_name']
                landing_page_context['surname'] = form.cleaned_data['surname']
                landing_page_context['email_address'] = form.cleaned_data['email_address']
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

@register_snippet
class RegistrationType(models.Model):
    type = models.CharField(max_length=500, null=True, help_text="Enter the category the registrant belongs to, e.g. Visitor")
    cost = models.DecimalField(max_digits=100, decimal_places=2, null=True, blank=True)
    panels = [
        FieldPanel('type'),
        FieldPanel('cost'),
    ]
    def __str__(self):
        return f'{self.type}'
    
@register_snippet
class CurrencyType(models.Model):
    type = models.CharField(max_length=500, null=True, help_text="Enter the currency type, e.g. Naira(NGN)")
    symbol = models.CharField(max_length=500, null=True, blank=True, help_text="Enter the currency symbol, e.g. $")
    panels = [
        FieldPanel('type'),
        FieldPanel('symbol'),
    ]
    def __str__(self):
        return f'{self.type}'
    
def random_alphanumeric_string():
    return ''.join(
        random.choices(
            string.ascii_letters + string.digits,
            k=12
        )
    )

class Attendant(models.Model):
    user_unique_id = models.CharField(max_length=500, unique=True)
    first_name = models.CharField(verbose_name='first name', max_length=255)
    last_name = models.CharField(verbose_name='last name', max_length=255)
    email = models.EmailField(null=True, blank=True)
    company = models.CharField(verbose_name='company', max_length=255, null=True, blank=True)
    position = models.CharField(verbose_name='position', max_length=255, null=True, blank=True)
    country = models.CharField(verbose_name='country', max_length=255, null=True, blank=True)
    phone = models.CharField(verbose_name='phone', max_length=255, null=True, blank=True)
    # registration_type = models.ForeignKey(RegistrationType, on_delete=models.DO_NOTHING, null=True)
    # total_cost = models.DecimalField(max_digits=100, decimal_places=2, null=True, blank=True)
    # number_of_registrant = models.IntegerField(default=1)
    # currency = models.ForeignKey(CurrencyType, on_delete=models.DO_NOTHING, null=True)

    panels = [
        FieldPanel('user_unique_id'),
        FieldPanel('first_name'),
        FieldPanel('last_name'),
        FieldPanel('email'),
        FieldPanel('company'),
        FieldPanel('position'),
        FieldPanel('country'),
        FieldPanel('phone'),
        # FieldPanel('registration_type'),
        # FieldPanel('total_cost'),
        # FieldPanel('number_of_registrant'),
        # FieldPanel('currency'),
    ]

    def __str__(self):
        return f'{self.first_name}'


    def save(self, *args, **kwargs):
        self.user_unique_id = random_alphanumeric_string() + 'NIHMEC' + self.first_name
        super(Attendant, self).save(*args, **kwargs)