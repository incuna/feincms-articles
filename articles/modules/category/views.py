from django.conf import settings
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404

from .models import Category
from articles.views import ArticleDetail, ArticleList


class CategoryAccesssGroupsMixin(object):
    def has_access_groups_permission(self, category):
        """
        Check that the current user has (access_group) permission to access the category.
        Return a (redirect) request object if the user does not have permission.
        Return none if the user has permissions
        """
        if category:
            access_groups = category.access_groups.all()
            user = self.request.user
            if access_groups and (user is None or not user.is_authenticated() or not user in access_groups):
                return False

        return True


class CategoryArticleDetail(ArticleDetail, CategoryAccesssGroupsMixin):
    template_name = "articles/category_article_detail.html"
    def get_queryset(self):
        return super(CategoryArticleDetail, self).get_queryset().filter(category__local_url=self.kwargs['category_url'])

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)

        if not self.has_access_groups_permission(self.object.category):
            return HttpResponseRedirect("%s?next=%s" % (settings.LOGIN_URL, self.request.path))

        return self.render_to_response(context)


class CategoryArticleList(ArticleList, CategoryAccesssGroupsMixin):
    template_name = "articles/category_article_list.html"
    category = None

    def get(self, request, *args, **kwargs):

        if 'category_url' in self.kwargs:
            self.category = get_object_or_404(Category, local_url=self.kwargs['category_url'])
            if not self.has_access_groups_permission(self.category):
                return HttpResponseRedirect("%s?next=%s" % (settings.LOGIN_URL, self.request.path))

        elif getattr(settings, 'ARTICLE_SHOW_FIRST_CATEGORY', False):
            # Redirect to the first category
            try:
                return HttpResponseRedirect(Category.objects.active(user=self.request.user)[0].get_absolute_url())
            except IndexError as e:
                pass


        return super(CategoryArticleList, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(CategoryArticleList, self).get_context_data(**kwargs)
        context['category'] = self.category

        return context

    def get_queryset(self):

        articles = super(CategoryArticleList, self).get_queryset()
        user = self.request.user

        # Limit the articles based on the category access_group permission
        if user is not None and user.is_authenticated():
            query = Q(category__access_groups__isnull=True) | Q(category__access_groups__in=user.groups.all())
        else:
            query = Q(category__access_groups__isnull=True)
        articles = articles.filter(query)

        if self.category:
            if getattr(settings, 'ARTICLE_SHOW_DESCENDANTS', False):
                articles = articles.filter(category__in=self.category.get_descendants(include_self=True)).order_by(self.category.order_by)
            else:
                articles = articles.filter(category=self.category).order_by(self.category.order_by)

        return articles.select_related('category')
