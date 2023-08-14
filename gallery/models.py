from django.db import models
from modelcluster.fields import ParentalKey

from wagtail.models import Page, Orderable
from wagtail.admin.panels import FieldPanel, InlinePanel
from django.utils.functional import cached_property
from cloudinary.models import CloudinaryField
# Create your models here.

class GalleryYearPage(Page):
    template = 'gallery/gallery.html'
    year = models.CharField(max_length=4)

    content_panels = Page.content_panels + [
        FieldPanel('year'),
        InlinePanel('gallery_images', label="Gallery images"),
    ]

    @cached_property
    def home_page(self):
        return self.get_parent().specific

    def get_context(self, request, *args, **kwargs):
        context = super(GalleryYearPage, self).get_context(request, *args, **kwargs)
        context["home_page"] = self.home_page
        return context

class ConferenceGalleryImage(Orderable):
    page = ParentalKey(GalleryYearPage, on_delete=models.CASCADE, related_name='gallery_images')
    image = CloudinaryField('image', null=True)
    caption = models.CharField(blank=True, max_length=250)

    panels = [
        FieldPanel('image'),
        FieldPanel('caption'),
    ]