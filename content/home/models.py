from wagtail.admin.panels import FieldPanel
from wagtail.api import APIField
from wagtail.fields import RichTextField
from wagtail.images.api.fields import ImageRenditionField
from wagtail.models import Page

from django.db import models


class HomePage(Page):
    body = RichTextField(blank=True)
    image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    content_panels = [
        *Page.content_panels,
        FieldPanel("body"),
        FieldPanel("image"),
    ]

    api_fields = [
        APIField("body"),
        APIField(
            "image_thumbnail",
            serializer=ImageRenditionField("fill-400x400", source="image"),
        ),
    ]
