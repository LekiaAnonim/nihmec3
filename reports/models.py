from django.db import models
from modelcluster.fields import ParentalKey

from wagtail.models import Page, Orderable
from wagtail.admin.panels import FieldPanel, InlinePanel, PageChooserPanel, FieldRowPanel, MultiFieldPanel
from django.utils.functional import cached_property
from wagtail.fields import RichTextField
from wagtail.contrib.forms.panels import FormSubmissionsPanel
from wagtail.contrib.forms.models import AbstractEmailForm, AbstractFormField
# Create your models here.

from datetime import date
from django.core.mail import send_mail
# from django.core.mail import EmailMessage
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.shortcuts import render


class FormField(AbstractFormField):
    page = ParentalKey('DownloadReportForm', on_delete=models.CASCADE, related_name='form_fields')


class DownloadReportForm(AbstractEmailForm):
    template = 'reports/report.html'
    year = models.CharField(max_length=4, blank=True, null=True)
    report_title = models.CharField(max_length=500, blank=True, null=True)
    report_summary = RichTextField(blank = True, null=True)
    report_download_link = models.URLField(blank=True, null=True)
    report_cover_image = models.ForeignKey("wagtailimages.Image", null=True, blank=True, on_delete=models.SET_NULL, related_name="+")
    thank_you_text = RichTextField(blank=True)
    content_panels = AbstractEmailForm.content_panels + [
        FormSubmissionsPanel(),
        FieldPanel('year'),
        FieldPanel('report_title'),
        FieldPanel('report_summary'),
        FieldPanel('report_download_link'),
        FieldPanel("report_cover_image"),

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
        context = super(DownloadReportForm, self).get_context(request, *args, **kwargs)
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

                text_content  = '\n' + '\n' + 'Dear,' + '\t' + str(form.cleaned_data['full_name']) + '\n' + '\n' +'\n'
                download_link = '<a href="{}" style="padding:10px; background:green; margin-top: 20px; color: white;">Download report</a>'.format(self.report_download_link)
                html_content = render_to_string('reports/email_header.html', context, request=request)+text_content+render_to_string('reports/registration_email_template.html', context, request=request)+download_link

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
    
