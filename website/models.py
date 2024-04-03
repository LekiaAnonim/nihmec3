from django.db import models

# Create your models here.
from wagtail.models import Page, Orderable
from wagtail.fields import RichTextField
from wagtail.snippets.models import register_snippet
from modelcluster.fields import ParentalKey, ParentalManyToManyField
from modelcluster.models import ClusterableModel
from django.utils.functional import cached_property
from wagtail.contrib.forms.panels import FormSubmissionsPanel
from wagtail.contrib.forms.models import AbstractEmailForm, AbstractFormField
from wagtail.admin.panels import FieldPanel, InlinePanel, FieldRowPanel, MultiFieldPanel, PageChooserPanel
# from wagtailcloudinary.fields import CloudinaryField, CloudinaryWidget
from cloudinary.models import CloudinaryField
from datetime import date
from django.core.mail import send_mail
# from django.core.mail import EmailMessage
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.shortcuts import render

class AboutPage(Page):
    template = 'website/about.html'
    max_count = 1
    body = RichTextField()

    content_panels = Page.content_panels + [
        FieldPanel('body'),
    ]
    @cached_property
    def home_page(self):
        return self.get_parent().specific

    def get_context(self, request, *args, **kwargs):
        context = super(AboutPage, self).get_context(request, *args, **kwargs)
        context["home_page"] = self.home_page
        return context
    
    class Meta:
        verbose_name = 'About Page'
        verbose_name_plural = 'About Page'

class TechnicalProgramPage(Page):
    template = 'website/technical_program.html'
    max_count = 1
    body = RichTextField()

    content_panels = Page.content_panels + [
        FieldPanel('body'),
    ]


    @cached_property
    def home_page(self):
        return self.get_parent().specific

    def get_context(self, request, *args, **kwargs):
        context = super(TechnicalProgramPage, self).get_context(request, *args, **kwargs)
        context["home_page"] = self.home_page
        return context
    
    class Meta:
        verbose_name = 'Technical Program Page'
        verbose_name_plural = 'Technical Program Page'

class MeteringTechnologyNightPage(Page):
    template = 'website/metering_technology_night.html'
    max_count = 1
    body = RichTextField()

    content_panels = Page.content_panels + [
        FieldPanel('body'),
    ]


    @cached_property
    def home_page(self):
        return self.get_parent().specific

    def get_context(self, request, *args, **kwargs):
        context = super(MeteringTechnologyNightPage, self).get_context(request, *args, **kwargs)
        context["home_page"] = self.home_page
        return context
    
    class Meta:
        verbose_name = 'Metering Technology Night Page'
        verbose_name_plural = 'Metering Technology Night Page'

class PreConference(Page):
    template = 'website/pre_conference.html'
    max_count = 1
    body = RichTextField()

    content_panels = Page.content_panels + [
        FieldPanel('body'),
    ]


    @cached_property
    def home_page(self):
        return self.get_parent().specific

    def get_context(self, request, *args, **kwargs):
        context = super(PreConference, self).get_context(request, *args, **kwargs)
        context["home_page"] = self.home_page
        return context
    
    class Meta:
        verbose_name = 'Pre-Conference Page'
        verbose_name_plural = 'Pre-Conference Page'

class FormField(AbstractFormField):
    page = ParentalKey('CallForAbstractPage', on_delete=models.CASCADE, related_name='form_fields')
class CallForAbstractPage(AbstractEmailForm):
    template = 'website/call_for_abstract.html'
    max_count = 1
    body = RichTextField()
    intro = RichTextField(blank=True)
    thank_you_text = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FormSubmissionsPanel(),
         FieldPanel('body'),
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
        context = super(CallForAbstractPage, self).get_context(request, *args, **kwargs)
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

                text_content  = '\n' + '\n' + 'Dear,' + '\t' + str(form.cleaned_data['name_of_authors']) + '\n' + '\n' +'\n'
                html_content = render_to_string('website/email_header.html', context, request=request)+text_content+render_to_string('website/registration_email_template.html', context, request=request)

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


class SpeakerPage(Page):
    template = 'website/speaker.html'
    # max_count = 1
    speaker_category = models.CharField(max_length=500, null=True)

    content_panels = Page.content_panels + [
        FieldPanel('speaker_category'),
    ]


    @cached_property
    def home_page(self):
        return self.get_parent().specific

    def get_context(self, request, *args, **kwargs):
        context = super(SpeakerPage, self).get_context(request, *args, **kwargs)
        speakers = Speakers.objects.all()
        context["home_page"] = self.home_page
        context["speakers"] = speakers
        return context
    
    class Meta:
        verbose_name = 'Speaker Page'
        verbose_name_plural = 'Speaker Pages'

@register_snippet
class Speakers(models.Model):
    speaker_category = ParentalKey('SpeakerPage', on_delete=models.SET_NULL, related_name='speaker_type', null=True)
    first_name = models.CharField(max_length = 500, null=True, blank=True)
    surname = models.CharField(max_length=500, null=True, blank=True)
    company = models.CharField(max_length=500, null=True)
    position = models.CharField(max_length=500, null=True, blank=True)
    short_introduction = RichTextField(blank=True)
    photo = CloudinaryField('image', null=True)

    panels = [
        FieldPanel('speaker_category'),
        FieldPanel('first_name'),
        FieldPanel('surname'),
        FieldPanel('company'),
        FieldPanel('position'),
        FieldPanel('short_introduction'),
        FieldPanel('photo'),
    ]

    def __str__(self):
        return self.first_name

    class Meta:
        verbose_name = 'Speaker'
        verbose_name_plural = 'Speakers'


@register_snippet
class Attendees(models.Model):
    company_name = models.CharField(max_length = 500, null=True, blank=True)
    company_logo = CloudinaryField('image', null=True)
    company_url = models.URLField(max_length=500, null=True)

    panels = [
        FieldPanel('company_name'),
        FieldPanel('company_logo'),
        FieldPanel('company_url'),
    ]

    def __str__(self):
        return self.company_name
    class Meta:
        verbose_name = 'Attendees'
        verbose_name_plural = 'Attendees'


@register_snippet
class Sponsors(models.Model):
    company_name = models.CharField(max_length = 500, null=True, blank=True)
    company_logo = CloudinaryField('image', null=True)
    company_url = models.URLField(max_length=500, null=True)

    panels = [
        FieldPanel('company_name'),
        FieldPanel('company_logo'),
        FieldPanel('company_url'),
    ]

    def __str__(self):
        return self.company_name
    class Meta:
        verbose_name = 'Sponsors'
        verbose_name_plural = 'Sponsors'

@register_snippet
class TechnicalAdvisoryCommittee(models.Model):
    first_name = models.CharField(max_length = 500, null=True, blank=True)
    surname = models.CharField(max_length=500, null=True, blank=True)
    company = models.CharField(max_length=500, null=True)
    position_in_company = models.CharField(max_length=500, null=True, blank=True)
    position_in_conference = models.CharField(max_length=500, null=True, blank=True)
    photo = CloudinaryField('image', null=True)

    panels = [
        FieldPanel('first_name'),
        FieldPanel('surname'),
        FieldPanel('company'),
        FieldPanel('position_in_company'),
        FieldPanel('position_in_conference'),
        FieldPanel('photo'),
    ]

    def __str__(self):
        return self.first_name

    class Meta:
        verbose_name = 'Tecnical Advisory Committee'
        verbose_name_plural = 'Tecnical Advisory Committees'

from wagtail.contrib.settings.models import BaseSiteSetting, register_setting

@register_setting
class SocialMediaSettings(BaseSiteSetting):
    facebook = models.URLField(
        help_text='Your Facebook page URL', null=True, blank=True)
    instagram = models.CharField(
        max_length=255, help_text='Your Instagram account URL', null=True, blank=True)
    youtube = models.URLField(
        help_text='Your YouTube channel or user account URL', null=True, blank=True)
    twitter = models.URLField(
        help_text='Your Twitter account URL', null=True, blank=True)

    linkedin = models.URLField(help_text='Your LinkedIn account URL', null=True, blank=True)
    website = models.URLField(help_text='Your Website URL', null=True, blank=True)
    email = models.EmailField(help_text='Your Email address', null=True, blank=True)
    phone = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        verbose_name = 'social media accounts'

@register_setting
class ImportantPages(BaseSiteSetting):
    # Fetch these pages when looking up ImportantPages for or a site
    select_related = ["register_page", "exhibit_page", "sponsor_page", "submit_abstract_page"]

    register_page = models.ForeignKey(
        'wagtailcore.Page', null=True, on_delete=models.SET_NULL, related_name='+')
    exhibit_page = models.ForeignKey(
        'wagtailcore.Page', null=True, on_delete=models.SET_NULL, related_name='+')
    sponsor_page = models.ForeignKey(
        'wagtailcore.Page', null=True, on_delete=models.SET_NULL, related_name='+')
    submit_abstract_page = models.ForeignKey(
        'wagtailcore.Page', null=True, on_delete=models.SET_NULL, related_name='+')

    panels = [
        PageChooserPanel('register_page'),
        PageChooserPanel('exhibit_page'),
        PageChooserPanel('sponsor_page'),
        PageChooserPanel('submit_abstract_page'),
    ]
