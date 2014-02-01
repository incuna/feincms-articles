from feincms.content.richtext.models import RichTextContent
from ..models import Article

Article.register_extensions(
    'articles.extensions.tags',
)

Article.register_templates({
    'title': 'Test template',
    'path': 'base.html',
    'regions': (('main', 'Main content area'),),
})

Article.create_content_type(RichTextContent)
