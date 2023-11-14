from django.db import models

# Create your models here.
from wagtail.models import Page, Orderable
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel, InlinePanel, PageChooserPanel
# from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.snippets.models import register_snippet
from modelcluster.fields import ParentalKey, ParentalManyToManyField
from django.utils.functional import cached_property
from website.models import Speakers, TechnicalAdvisoryCommittee, Attendees
from cloudinary.models import CloudinaryField


class HomePage(Page):
    parent_page_types = ['wagtailcore.Page']
    template = 'home/home_page.html'
    max_count = 1

    conference_name = models.CharField(max_length=500, null=True)
    short_name = models.CharField(max_length=500, null=True)
    year = models.IntegerField(unique=True, null=True)
    theme = models.CharField(max_length=1000, null=True)
    venue = models.CharField(max_length=1000, null=True, blank=True)
    start_date = models.DateField(null=True)
    end_date = models.DateField(null=True)
    short_description = RichTextField(blank = True, null=True)
    contact_email = models.EmailField(null=True)
    contact_phone_number = models.CharField(max_length=20, null=True)
    dollar_payment_link = models.URLField(null=True, blank=True)
    # feature_conference_on_site = models.BooleanField(default=True)

    slider1 = CloudinaryField('image', null=True)
    slider1_text = RichTextField(blank = True, null=True)
    slider2 = CloudinaryField('image', null=True)
    slider2_text = RichTextField(blank = True, null=True)
    slider3 = CloudinaryField('image', null=True)
    slider3_text = RichTextField(blank = True, null=True)
    slider4 = CloudinaryField('image', null=True)
    slider4_text = RichTextField(blank = True, null=True)
    register_cta = models.ForeignKey("wagtailcore.Page", null=True, blank=True, on_delete=models.SET_NULL, related_name="+")
    about_cta = models.ForeignKey("wagtailcore.Page", null=True, blank=True, on_delete=models.SET_NULL, related_name="+")
    sponsor_cta = models.ForeignKey("wagtailcore.Page", null=True, blank=True, on_delete=models.SET_NULL, related_name="+")

    content_panels = Page.content_panels + [
        FieldPanel('conference_name'),
        FieldPanel('short_name'),
        FieldPanel('year'),
        FieldPanel('theme'),
        FieldPanel('venue'),
        FieldPanel('start_date'),
        FieldPanel('end_date'),
        FieldPanel('short_description'),
        FieldPanel('contact_email'),
        FieldPanel('contact_phone_number'),
        FieldPanel('dollar_payment_link'),
        FieldPanel("slider1"),
        FieldPanel("slider1_text"),
        FieldPanel("slider2"),
        FieldPanel("slider2_text"),
        FieldPanel("slider3"),
        FieldPanel("slider3_text"),
        FieldPanel("slider4"),
        FieldPanel("slider4_text"),
        PageChooserPanel("register_cta"),
        PageChooserPanel("about_cta"),
        PageChooserPanel("sponsor_cta"),
    ]

    def __str__(self):
        return self.short_name

    class Meta:
        verbose_name = 'Conference Page'
        verbose_name_plural = 'Conference Pages'

    @cached_property
    def home_page(self):
        return self.specific

    def get_context(self, request, *args, **kwargs):
        context = super(HomePage, self).get_context(request, *args, **kwargs)

        speakers = Speakers.objects.all()
        committees = TechnicalAdvisoryCommittee.objects.all()
        attendees = Attendees.objects.all()
        sponsors = Sponsors.objects.all()


        context["home_page"] = self.home_page
        context["speakers"] = speakers
        context["committees"] = committees
        context["attendees"] = attendees
        context["sponsors"] = sponsors
        return context


