from incunafein.content import BaseFkeyContent

class ArticleFkeyContent(BaseFkeyContent):
    
    class Meta:
        abstract = True
            
    def template_hierarchy(self):
        return ['content/articles/category_%s.html' % self.category.slug,
                'content/articles/default.html',
               ]