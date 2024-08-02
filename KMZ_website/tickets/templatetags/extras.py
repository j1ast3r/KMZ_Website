from django import template

register = template.Library()

@register.filter
def to_letter(index):
    return chr(65 + index)