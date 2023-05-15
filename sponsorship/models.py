from django.db import models
from wagtail.models import Page, Orderable
from wagtail.fields import RichTextField
from wagtail.snippets.models import register_snippet
from modelcluster.fields import ParentalKey, ParentalManyToManyField
from modelcluster.models import ClusterableModel
from django.utils.functional import cached_property
from wagtail.contrib.forms.panels import FormSubmissionsPanel
from wagtail.contrib.forms.models import AbstractEmailForm, AbstractFormField
from wagtail.admin.panels import FieldPanel, InlinePanel, FieldRowPanel, MultiFieldPanel

from datetime import date
from django.core.mail import send_mail
# from django.core.mail import EmailMessage
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.shortcuts import render
# Create your models here.
@register_snippet
class SponsorshipPackageFeatures(models.Model):
    feature = models.CharField(max_length=1000, null=True)

    def __str__(self):
        return self.feature

@register_snippet   
class SponsorshipPackage(ClusterableModel):
    sponsorship_type = models.CharField(max_length=100, help_text="e.g. Premium")
    price = models.DecimalField(decimal_places=2, null=True, max_digits=100)
    features = ParentalManyToManyField(SponsorshipPackageFeatures, related_name="package_features")

    panels = [
        FieldPanel('sponsorship_type'),
        FieldPanel('price'),
        FieldPanel('features'),
    ]

class SponsorshipPage(Page):
    template = 'sponsorship/sponsor.html'
    intro = RichTextField(blank=True)
    sponsorship_package = ParentalManyToManyField(SponsorshipPackage, blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('intro'),
        FieldPanel('sponsorship_package'),
        
    ]

    @cached_property
    def home_page(self):
        return self.get_parent().specific

    def get_context(self, request, *args, **kwargs):
        context = super(SponsorshipPage, self).get_context(request, *args, **kwargs)
        package_features = SponsorshipPackageFeatures.objects.all()
        context["package_features"] = package_features
        # home_page = HomePage.objects.live()
        context["home_page"] = self.home_page
        return context


class FormField(AbstractFormField):
    page = ParentalKey('SponsorFormPage', on_delete=models.CASCADE, related_name='form_fields')


class SponsorFormPage(AbstractEmailForm):
    template = 'sponsorship/sponsor_detail.html'
    intro = RichTextField(blank=True)
    package = ParentalKey('SponsorshipPackage', on_delete=models.SET_NULL, related_name='sponsor_form_package', null=True)
    thank_you_text = RichTextField(blank=True)

    content_panels = AbstractEmailForm.content_panels + [
        FormSubmissionsPanel(),
        FieldPanel('package'),
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
        return self.get_parent().specific.get_parent().specific

    def get_context(self, request, *args, **kwargs):
        context = super(SponsorFormPage, self).get_context(request, *args, **kwargs)
        context["home_page"] = self.home_page
        return context

    def get_form_fields(self):
        return self.form_fields.all()

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

                text_content  = '\n' + '\n' + 'Dear,' + '\t' + str(form.cleaned_data['first_name']) + '\n' + '\n' +'\n'
                html_content = render_to_string('sponsorship/email_header.html', context, request=request)+text_content+render_to_string('sponsorship/registration_email_template.html', context, request=request)

                msg = EmailMultiAlternatives(subject, text_content, self.from_address, [address for address in addresses]+[form.cleaned_data['email_address']])
                # msg.content_subtype = "html"  # Main content is now text/html
                msg.attach_alternative(html_content, "text/html")
                msg.send()
                landing_page_context = self.get_context(request, *args, **kwargs)
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
    
