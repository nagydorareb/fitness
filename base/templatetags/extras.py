from django.templatetags.static import static
from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.simple_tag
def get_type_icon(type):
    """ 
    Add icons to HTML according to workout training type
    """
    switcher = {
        "ST": '<i class="fas fa-dumbbell lilpadding"></i>',
        "HI": '<i class="fas fa-heartbeat lilpadding"></i>',
        "CA": '<i class="fas fa-running lilpadding"></i>',
        "YO": '<i class="fas fa-spa lilpadding"></i>',
        "PA": '<i class="fas fa-leaf lilpadding"></i>',
    }
    return mark_safe(switcher.get(type))

@register.simple_tag
def get_type_big_icon(type):
    switcher = {
        "ST": '<i class="fas fa-dumbbell fa-3x lilpadding"></i>',
        "HI": '<i class="fas fa-heartbeat fa-3x lilpadding"></i>',
        "CA": '<i class="fas fa-running fa-3x lilpadding"></i>',
        "YO": '<i class="fas fa-spa fa-3x lilpadding"></i>',
        "PA": '<i class="fas fa-leaf fa-3x lilpadding"></i>',
    }
    return mark_safe(switcher.get(type))

@register.simple_tag(takes_context=True)
def param_replace(context, **kwargs):
    """
    Pagination with filter
    """
    d = context['request'].GET.copy()
    for k, v in kwargs.items():
        d[k] = v
    for k in [k for k, v in d.items() if not v]:
        del d[k]
        
    return d.urlencode()