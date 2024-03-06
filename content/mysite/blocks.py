from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock as DefaultImageChooserBlock


class ImageChooserBlock(DefaultImageChooserBlock):
    def get_api_representation(self, value, context=None):
        if value:
            return {
                "id": value.id,
                "title": value.title,
                "details": value.get_rendition("width-1000").attrs_dict,
            }


class GenericTextBlock(blocks.StructBlock):
    text = blocks.TextBlock(required=True)

    class Meta:
        icon = "edit"
        label = "Generic Text"


class TitleBlock(blocks.StructBlock):
    title = blocks.CharBlock(required=True)
    type = blocks.ChoiceBlock(
        choices=[
            ("h1", "h1"),
            ("h2", "h2"),
            ("h3", "h3"),
            ("h4", "h4"),
            ("h5", "h5"),
            ("h6", "h6"),
        ],
        required=True,
    )

    class Meta:
        icon = "edit"
        label = "Title"


class ImageBlock(blocks.StructBlock):
    image = ImageChooserBlock(required=True)

    class Meta:
        icon = "edit"
        label = "Image"
