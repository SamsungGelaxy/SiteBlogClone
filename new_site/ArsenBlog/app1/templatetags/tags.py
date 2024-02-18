from django.template import Library
from django.template.defaultfilters import stringfilter
from django.utils.html import escape, conditional_escape

from app1 import views as v


register=Library()


@register.filter("plus")
def plus(value, p):
    return value+p

@register.filter("minus")
def minus(value, p):
    return value-p




@register.simple_tag(name="get_name", takes_context=True)
def f1(context):
    return "Arsen"

@register.inclusion_tag(filename="includes/name.html", takes_context=True)
def get_hname(context):
    return {"name":"Arsen Golovanev"}


