from django.db import models
from modelcluster.fields import ParentalKey

from wagtail.models import Page, Orderable
from wagtail.admin.panels import FieldPanel, InlinePanel, PageChooserPanel, FieldRowPanel, MultiFieldPanel
from django.utils.functional import cached_property
from wagtail.fields import RichTextField
from wagtail.contrib.forms.panels import FormSubmissionsPanel
from wagtail.contrib.forms.models import AbstractEmailForm, AbstractFormField
# Create your models here.


class FormField(AbstractFormField):
    page = ParentalKey('DownloadReportForm', on_delete=models.CASCADE, related_name='form_fields')


class DownloadReportForm(AbstractEmailForm):
    template = 'reports/report.html'
    year = models.CharField(max_length=4, blank=True, null=True)
    report_title = models.CharField(max_length=500, blank=True, null=True)
    report_summary = RichTextField(blank = True, null=True)
    report_cover_image = models.ForeignKey("wagtailimages.Image", null=True, blank=True, on_delete=models.SET_NULL, related_name="+")
    thank_you_text = RichTextField(blank=True)
    content_panels = AbstractEmailForm.content_panels + [
        FormSubmissionsPanel(),
        FieldPanel('year'),
        FieldPanel('report_title'),
        FieldPanel('report_summary'),
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