from random import randint
from django import template
from django.core.paginator import Paginator
from lememe.models import Category, Comment

register = template.Library()


@register.inclusion_tag('lememe/cats.html')
def get_category_list(cat=None):
    return {'cats': Category.objects.all().extra(select={'lower_name':'lower(name)'}).order_by('lower_name'),
            'act_cat': cat,
            }

# this tag can be used when we want to force the browser to re-download an image
# ie. src=".../filename.jpg?v=2452" passing a dummy key in get method will reload the image
@register.assignment_tag()
def random_number(length=3):
    """
    Create a random integer with given length.
    For a length of 3 it will be between 100 and 999.
    For a length of 4 it will be between 1000 and 9999.
    """
    return randint(10**(length-1), (10**length-1))
