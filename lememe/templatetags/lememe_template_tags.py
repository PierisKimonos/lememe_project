from django import template
from django.core.paginator import Paginator
from lememe.models import Category, Comment

register = template.Library()


@register.inclusion_tag('lememe/cats.html')
def get_category_list(cat=None):
    return {'cats': sorted(Category.objects.all()),
            'act_cat': cat,
            }