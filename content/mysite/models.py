from wagtail.admin.panels import FieldPanel
from wagtail.api import APIField
from wagtail.fields import StreamField
from wagtail.models import Page
from wagtail_headless_preview.models import HeadlessPreviewMixin

from django.http import Http404

from . import blocks

# TO DO:
# differenciate basic blocks from content blocks
# basic blocks are used in multiple places/gathering
# content blocks are used in one place/refinement


class HeadlessMixin(HeadlessPreviewMixin):
    def serve(self, request):
        raise Http404


class BasicSite(HeadlessMixin, Page):
    body = StreamField(
        [
            ("title_block", blocks.TitleBlock()),
            ("generic_text_block", blocks.GenericTextBlock()),
            ("image_block", blocks.ImageBlock()),
        ],
        use_json_field=True,
    )

    content_panels = [
        *Page.content_panels,
        FieldPanel("body"),
    ]

    api_fields = [
        APIField("body"),
    ]
