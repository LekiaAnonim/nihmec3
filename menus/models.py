from django.db import models

# Create your models here.
from django_extensions.db.fields import AutoSlugField
from modelcluster.models import ClusterableModel
from wagtail.admin.panels import FieldPanel, InlinePanel, PageChooserPanel, MultiFieldPanel
from wagtail.models import Orderable
from wagtail.snippets.models import register_snippet
from modelcluster.fields import ParentalKey, ParentalManyToManyField
from wagtailcloudinary.fields import CloudinaryField, CloudinaryWidget

class MenuItem(Orderable):
    link_text = models.CharField(blank=True, null=True, max_length=100)
    link_url = models.CharField(max_length=500, blank=True, null=True)
    link_page = models.ForeignKey("wagtailcore.Page", null=True, blank=True, related_name="+", on_delete=models.CASCADE)
    open_in_new_tab = models.BooleanField(default=False, blank=True)
    page = ParentalKey("Menu", related_name="menu_items")

    panels = [
        FieldPanel("link_text"),
        FieldPanel("link_url"),
        PageChooserPanel("link_page"),
        FieldPanel("open_in_new_tab"),
    ]

    @property
    def link(self):
        if self.link_page:
            return self.link_page.url
        elif self.link_url:
            return self.link_url
        return "#"
    
    @property
    def title(self):
        if self.link_page and not self.link_text:
            return self.link_page.title
        elif self.link_text:
            return self.link_text
        return "Missing Title"
    

@register_snippet
class Menu(ClusterableModel):
    title = models.CharField(max_length=100, null=True)
    slug = AutoSlugField(populate_from = "title", editable=True)

    panels = [
        MultiFieldPanel([
            FieldPanel("title"),
            FieldPanel("slug"),
        ], heading = "Menu"),
        InlinePanel("menu_items", label = "Menus Item")
    ]

    def __str__(self):
        return self.title